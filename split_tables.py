"""
split_tables.py
───────────────
Recursively processes ALL CSV files across the entire datasets/ folder tree.

ROOT CAUSE FIXES:
  1. pandas read_csv with on_bad_lines='skip' silently discards data rows
     whenever a 1-column caption row sets the column count. Fixed by using
     Python's native csv module which handles variable column counts natively.

  2. Captions with an embedded comma get split across two CSV cells, e.g.:
       "# Table 1: Results for biomass (dry basis" | "wt.%)"
     Fixed by detecting the Table N pattern in the first cell only, then
     accepting multi-cell rows as captions if the extra cells contain no
     numeric data (text continuation, not data values).

Decision logic driven by master CSV column "Data useful for simulations":
  Yes  → Always process — create split CSVs regardless of data source
  No   → Skip entirely
  NaN  → Not yet assessed — process normally

File type handling:
  multi_table   → one CSV per table in a subfolder
  single_table  → cleaned copy in a subfolder as stem_data.csv
  caption_only  → save table_index.csv (fallback — should be rare now)

Caption patterns supported:
  "Table 1."      paper 03 reference sheets  (dot separator)
  "# Table 1:"    direct paper CSVs          (hash + colon)
  "# Table S1"    supplementary tables       (hash, no separator)
  "# Table 1: ... (dry basis" | "wt.%)"      split across two cells

Run from project root:
    python split_tables.py
"""

import csv
import os
import re
import pandas as pd


# ── Config ────────────────────────────────────────────────────────────────────
DATASETS_ROOT = "database/datasets"
MASTER_CSV    = "database/papers_cleaned.csv"
# ─────────────────────────────────────────────────────────────────────────────


# ── Load master CSV ───────────────────────────────────────────────────────────
try:
    _master = pd.read_csv(MASTER_CSV, encoding="utf-8-sig", dtype=str)
    _master["Serial"] = _master["Serial"].str.strip()
    _MASTER_LOADED = True
except Exception as e:
    print(f"⚠️  Could not load master CSV ({e}) — simulation checks disabled.")
    _master = pd.DataFrame()
    _MASTER_LOADED = False


def get_simulation_status(csv_stem: str) -> str:
    """
    Look up 'Data useful for simulations' from master CSV.
    Serial number extracted from filename prefix: '04_something' → serial 4.
    Returns 'Yes', 'No', or 'nan'.
    """
    if not _MASTER_LOADED:
        return "nan"
    m = re.match(r"^(\d+)_", csv_stem)
    if not m:
        return "nan"
    serial = str(int(m.group(1)))
    row = _master[_master["Serial"] == serial]
    if row.empty or "Data useful for simulations" not in _master.columns:
        return "nan"
    return str(row["Data useful for simulations"].values[0]).strip()


def get_full_status(csv_stem: str) -> dict:
    """Return all three data-availability flags for logging."""
    default = {"provided": "nan", "from_tables": "nan", "useful": "nan"}
    if not _MASTER_LOADED:
        return default
    m = re.match(r"^(\d+)_", csv_stem)
    if not m:
        return default
    serial = str(int(m.group(1)))
    row = _master[_master["Serial"] == serial]
    if row.empty:
        return default
    def _v(col):
        return str(row[col].values[0]).strip() if col in row.columns else "nan"
    return {
        "provided":    _v("Data provided"),
        "from_tables": _v("Data from tables"),
        "useful":      _v("Data useful for simulations"),
    }


# ── CSV reading ───────────────────────────────────────────────────────────────

def read_csv_raw(filepath: str) -> list:
    """
    Read a CSV using Python's csv module.
    Returns list of rows; each row is a list of stripped strings.
    Handles variable column counts per row — no rows are dropped.
    """
    rows = []
    with open(filepath, encoding="utf-8", newline="", errors="replace") as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append([cell.strip() for cell in row])
    return rows


# ── Caption helpers ───────────────────────────────────────────────────────────

def is_caption_row(cells: list) -> bool:
    """
    Detect table caption rows. Handles all known split patterns:

      Single cell:
        '# Table 1: description'

      Split by embedded comma in title text:
        '# Table 1: Biomass analysis (dry basis' | 'wt.%)'
        '# Table 14: Parameters for points A'    | 'B and C.'

      Split by comma inside a citation list:
        '# Table 3: Characterization of biomass [27' | '33' | '34].'

    Strategy: first cell must start with Table N pattern. Row is rejected
    as a caption only if a secondary cell looks like a decimal/float data
    value. Pure integers (e.g. citation numbers like 33, 34) are allowed.
    """
    non_empty = [c for c in cells if c]
    if not non_empty:
        return False

    # First cell must start with the Table N pattern
    v = non_empty[0].lstrip('"').lstrip("#").strip()
    if not re.match(r"^[Tt]able\s+[S\d]", v):
        return False

    # Single non-empty cell — unambiguous caption
    if len(non_empty) == 1:
        return True

    # Multiple cells — reject only if a secondary cell is a decimal/float
    # (e.g. '8.00', '-0.97') which signals a numeric data column.
    # Pure integers like '33' are allowed — they are citation numbers.
    for extra in non_empty[1:]:
        e = extra.strip()
        if re.match(r"^[+\-]?\d+\.\d+([eE][+\-]?\d+)?$", e):
            return False
    return True


def clean_caption(cells: list) -> str:
    """
    Return clean caption text, joining all cells back together.
    Handles split captions caused by embedded commas in the title.
    """
    non_empty = [c for c in cells if c]
    if not non_empty:
        return ""
    joined = ", ".join(non_empty)
    return joined.lstrip('"').lstrip("#").strip()


def is_empty_row(cells: list) -> bool:
    return not any(c for c in cells)


def slugify(caption: str) -> str:
    """Convert caption text to a safe filename slug."""
    text = re.sub(r"^[Tt]able\s+[S\d]+[\.\:\s]+", "", caption.strip())
    text = re.sub(r"[^a-z0-9\s]", " ", text.lower())
    return re.sub(r"\s+", "_", text.strip())[:55].strip("_")


def get_table_number(caption: str) -> str:
    """Extract zero-padded table number from caption. 'Table 12' → '12'."""
    v = caption.strip().lstrip('"').lstrip("#").strip()
    m = re.match(r"[Tt]able\s+([S\d]+)", v)
    return m.group(1).zfill(2) if m else "00"


# ── File classification ───────────────────────────────────────────────────────

def classify_file(rows: list) -> str:
    """Returns 'caption_only', 'multi_table', or 'single_table'."""
    caption_count  = 0
    data_row_count = 0
    for cells in rows:
        if is_empty_row(cells):
            continue
        if is_caption_row(cells):
            caption_count += 1
        else:
            data_row_count += 1
    if caption_count > 0 and data_row_count == 0:
        return "caption_only"
    elif caption_count >= 1:
        return "multi_table"
    else:
        return "single_table"


# ── Processing functions ──────────────────────────────────────────────────────

def save_table_index(rows: list, out_dir: str):
    """Fallback for caption-only files: save table titles as table_index.csv."""
    os.makedirs(out_dir, exist_ok=True)
    titles = [clean_caption(cells) for cells in rows if is_caption_row(cells)]
    pd.DataFrame({"Table": titles}).to_csv(
        os.path.join(out_dir, "table_index.csv"), index=False
    )


def split_multi_table(rows: list, out_dir: str) -> list:
    """
    Split a stacked multi-table file into one CSV per table.

    Structure per table:
      Row N     caption row   ("# Table N: description" — 1 or 2 cells)
      Row N+1   header row    (column names)
      Row N+2+  data rows     (until next caption row or end of file)
      Empty rows are skipped.

    Returns list of (filename, n_rows, n_cols, caption) tuples.
    """
    # Locate all caption row indices
    caption_positions = [i for i, cells in enumerate(rows) if is_caption_row(cells)]

    os.makedirs(out_dir, exist_ok=True)
    saved = []

    for idx, cap_i in enumerate(caption_positions):
        caption_text = clean_caption(rows[cap_i])
        tnum_str     = get_table_number(caption_text)

        # Header row immediately follows the caption
        header_i = cap_i + 1
        if header_i >= len(rows):
            continue

        # Data runs from header+1 to the next caption (or end)
        next_cap_i = (
            caption_positions[idx + 1]
            if idx + 1 < len(caption_positions)
            else len(rows)
        )
        data_rows = [
            cells for cells in rows[header_i + 1 : next_cap_i]
            if not is_empty_row(cells)
        ]

        if not data_rows:
            continue

        # Pad all rows to uniform column count
        header_cells = rows[header_i]
        n_cols = max(len(header_cells), max(len(r) for r in data_rows))

        def pad(row, width):
            return row + [""] * (width - len(row))

        columns = pad(header_cells, n_cols)
        padded  = [pad(r, n_cols) for r in data_rows]

        df = pd.DataFrame(padded, columns=columns)

        # Drop fully empty columns and rows
        df = df.loc[:, df.apply(lambda c: c.str.strip().ne("").any())]
        df = df[df.apply(lambda r: r.str.strip().ne("").any(), axis=1)]
        df = df.reset_index(drop=True)

        if df.empty:
            continue

        # Filename from caption; fall back to first 3 column names
        slug = slugify(caption_text)
        if not slug:
            col_slug = "_".join(
                re.sub(r"[^a-z0-9]", "_", str(c).lower())
                for c in columns[:3] if str(c).strip()
            )
            slug = re.sub(r"_+", "_", col_slug).strip("_")[:55] or f"table_{tnum_str}"

        filename = f"table_{tnum_str}_{slug}.csv"
        df.to_csv(os.path.join(out_dir, filename), index=False)
        saved.append((filename, len(df), len(df.columns), caption_text[:65]))

    return saved


def copy_single_table(rows: list, stem: str, out_dir: str) -> list:
    """Clean and save a single-table file into its subfolder."""
    os.makedirs(out_dir, exist_ok=True)

    non_empty = [r for r in rows if not is_empty_row(r)]
    if not non_empty:
        return []

    n_cols = max(len(r) for r in non_empty)
    padded = [r + [""] * (n_cols - len(r)) for r in non_empty]
    df     = pd.DataFrame(padded[1:], columns=padded[0])
    df     = df.loc[:, df.apply(lambda c: c.str.strip().ne("").any())]
    df     = df[df.apply(lambda r: r.str.strip().ne("").any(), axis=1)]
    df     = df.reset_index(drop=True)

    filename = f"{stem}_data.csv"
    df.to_csv(os.path.join(out_dir, filename), index=False)

    return [(filename, len(df), len(df.columns), "Single dataset table")]


# ── Main walk ─────────────────────────────────────────────────────────────────
total_files        = 0
total_tables       = 0
skipped_not_useful = 0
needs_extraction   = 0

print(f"Walking: {DATASETS_ROOT}\n")
print("=" * 70)

for dirpath, dirnames, filenames in os.walk(DATASETS_ROOT):

    # Prune subfolders already created by a previous run of this script
    # (a subfolder whose name matches a CSV stem in the same directory)
    csv_stems_in_dir = {
        os.path.splitext(f)[0]
        for f in filenames if f.endswith(".csv")
    }
    dirnames[:] = [d for d in dirnames if d not in csv_stems_in_dir]

    csv_files = sorted([f for f in filenames if f.endswith(".csv")])
    if not csv_files:
        continue

    print(f"\n📁  {dirpath}  ({len(csv_files)} CSV files)")

    for csv_file in csv_files:
        src_path = os.path.join(dirpath, csv_file)
        stem     = os.path.splitext(csv_file)[0]
        out_dir  = os.path.join(dirpath, stem)

        # ── Gate: check simulation usefulness before reading the file ─────────
        useful = get_simulation_status(stem)
        status = get_full_status(stem)

        if useful == "No":
            print(
                f"  ⏭️   {csv_file}  — not useful for simulations "
                f"(provided={status['provided']}, "
                f"from_tables={status['from_tables']})"
            )
            skipped_not_useful += 1
            continue

        # ── Read file ─────────────────────────────────────────────────────────
        try:
            rows = read_csv_raw(src_path)
        except Exception as e:
            print(f"  ⚠️   {csv_file}  — could not read: {e}")
            continue

        file_type = classify_file(rows)
        total_files += 1

        # ── Caption-only (fallback — rare after the split-caption fix) ────────
        if file_type == "caption_only":
            save_table_index(rows, out_dir)
            n_caps = sum(1 for r in rows if is_caption_row(r))
            print(
                f"  📋  {csv_file}  — data not yet extracted "
                f"({n_caps} tables listed)  →  {stem}/table_index.csv"
            )
            needs_extraction += 1

        # ── Multi-table: split into individual CSVs ───────────────────────────
        elif file_type == "multi_table":
            saved = split_multi_table(rows, out_dir)
            if saved:
                print(f"  📄  {csv_file}  → {len(saved)} tables")
                for fname, nrows, ncols, caption in saved:
                    print(f"      ✅  {fname}  ({nrows}r × {ncols}c)")
                total_tables += len(saved)
            else:
                print(f"  ⚠️   {csv_file}  — multi-table but no extractable data")

        # ── Single-table: clean and copy ──────────────────────────────────────
        else:
            saved = copy_single_table(rows, stem, out_dir)
            if saved:
                fname, nrows, ncols, _ = saved[0]
                print(
                    f"  📊  {csv_file}  → single table "
                    f"({nrows}r × {ncols}c)  →  {fname}"
                )
                total_tables += 1

print(f"\n{'=' * 70}")
print(f"Done.")
print(f"  Files processed             : {total_files}")
print(f"  Table CSVs created          : {total_tables}")
print(f"  Needs extraction (indexed)  : {needs_extraction}")
print(f"  Skipped (not useful)        : {skipped_not_useful}")
