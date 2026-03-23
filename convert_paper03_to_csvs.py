"""
convert_paper03_to_csvs.py
──────────────────────────
Converts every data sheet in the Khandelwal et al. 2025 multi-sheet Excel
file into a single stacked CSV per sheet.

Header row detection (automatic):
  - Row 0  : Paper title  (always skipped)
  - Row 1  : Either blank OR contains Table 1 caption (Reddy sheet only)
  - If row 1 is blank  → Table 1 caption is on row 2, column headers on row 3 → header=3
  - If row 1 has text  → Table 1 caption IS row 1, column headers on row 2  → header=2

Run from project root:
    python convert_paper03_to_csvs.py
"""

import pandas as pd
import os

# ── Config ────────────────────────────────────────────────────────────────────
EXCEL_FILE    = "database/datasets/thermochemical/Khandelwal_et_al_2025_datasets_updated.xlsx"
OUTPUT_FOLDER = "database/datasets/thermochemical/03_scwg_khandelwal"
# ─────────────────────────────────────────────────────────────────────────────

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

xl = pd.ExcelFile(EXCEL_FILE)

# Sheet 0 ('Khandelwal et al. (2025)') is the index — skip it
DATA_SHEETS = xl.sheet_names[1:]

print(f"Found {len(DATA_SHEETS)} data sheets (index sheet skipped)\n")

for i, sheet in enumerate(DATA_SHEETS, start=1):

    # ── Step 1: read raw (no header) to detect structure ─────────────────────
    raw = pd.read_excel(EXCEL_FILE, sheet_name=sheet, header=None)

    # Check whether row 1 is blank (all NaN or empty strings)
    row1_vals = [
        v for v in raw.iloc[1].tolist()
        if str(v).strip() and str(v).lower() != "nan"
    ]
    row1_is_blank = len(row1_vals) == 0

    # Choose header row:
    #   row 1 blank  → Table 1 caption on row 2, headers on row 3 → header=3
    #   row 1 filled → Table 1 caption on row 1, headers on row 2 → header=2
    header_row = 3 if row1_is_blank else 2

    # ── Step 2: re-read with correct header row ───────────────────────────────
    df = pd.read_excel(EXCEL_FILE, sheet_name=sheet, header=header_row)

    # ── Step 3: prepend the Table 1 caption as a proper caption row ───────────
    # It lives one row above the header row in the raw sheet
    caption_row_idx = header_row - 1
    table1_caption  = str(raw.iloc[caption_row_idx, 0]).strip()

    # Build a caption row with the same columns as df, caption in first cell
    caption_series = pd.Series(
        [table1_caption] + [""] * (len(df.columns) - 1),
        index=df.columns
    )
    df = pd.concat(
        [caption_series.to_frame().T, df],
        ignore_index=True
    )

    # ── Step 4: drop fully empty columns ─────────────────────────────────────
    df = df.dropna(axis=1, how="all")
    df = df.loc[:, ~df.apply(
        lambda c: c.astype(str).str.strip().isin(["", "nan"]).all()
    )]

    # ── Step 5: build clean filename from sheet name ──────────────────────────
    safe_name = (
        sheet.strip()
             .lower()
             .replace(" ", "_")
             .replace("/", "_")
             .replace("\\", "_")
             .replace("(", "")
             .replace(")", "")
             .replace(".", "")
             .replace(",", "")
             .replace("&", "and")
             .replace("—", "")
             .replace("-", "_")
    )
    while "__" in safe_name:
        safe_name = safe_name.replace("__", "_")
    safe_name = safe_name.strip("_")

    filename = f"{i:02d}_{safe_name}.csv"
    out_path  = os.path.join(OUTPUT_FOLDER, filename)

    df.to_csv(out_path, index=False)

    print(f"  ✅  {filename}")
    print(f"      {len(df)} rows × {len(df.columns)} cols")
    print(f"      Header row used: {header_row}  |  Table 1 caption: '{table1_caption[:60]}'")
    print()

print(f"Done — {len(DATA_SHEETS)} CSVs saved to '{OUTPUT_FOLDER}/'")
