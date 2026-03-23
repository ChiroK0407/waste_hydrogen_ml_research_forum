"""
5_Dataset_Viewer.py
────────────────────
Dedicated page for browsing simulation-ready datasets extracted from
the reviewed papers. Shows:
  - Paper metadata and data availability status
  - All split table CSVs as interactive searchable dataframes
  - Download button per table
  - Drive links for both the original paper and its dataset file
"""

import streamlit as st
import pandas as pd
import os
import re


# ── Config ────────────────────────────────────────────────────────────────────
DATASETS_ROOT = "database/datasets"
MASTER_CSV    = "database/papers_cleaned.csv"

THERMO_KW = ["gasification", "scwg", "pyrolysis", "htl", "reforming",
             "electrolysis", "methanation", "biofuel"]
BIO_KW    = ["biological", "fermentation", "biophotolysis",
             "photocatalytic", "algal"]
# ─────────────────────────────────────────────────────────────────────────────


# ── Load master CSV ───────────────────────────────────────────────────────────
@st.cache_data
def load_master() -> pd.DataFrame:
    df = pd.read_csv(MASTER_CSV, encoding="utf-8-sig", dtype=str)
    df["Serial"] = df["Serial"].str.strip()
    return df


# ── Folder helpers ────────────────────────────────────────────────────────────

def get_category(route: str) -> str:
    r = route.lower()
    if any(k in r for k in THERMO_KW):
        return "thermochemical"
    if any(k in r for k in BIO_KW):
        return "biochemical"
    return "other"


def find_paper_folder(serial: str, category: str) -> str | None:
    """
    Find the subfolder for a paper inside the category folder.
    Matches any folder whose name starts with the zero-padded serial.
    Handles both:
      - Direct paper folders:  thermochemical/04_gasification_wang_25/
      - Sub-source folders:    thermochemical/03_scwg_khandelwal/
    """
    category_path = os.path.join(DATASETS_ROOT, category)
    if not os.path.isdir(category_path):
        return None

    padded = serial.zfill(2)

    # First check: direct subfolder matching serial
    for item in os.listdir(category_path):
        item_path = os.path.join(category_path, item)
        if os.path.isdir(item_path) and item.startswith(padded + "_"):
            return item_path

    # Second check: nested sub-source folder (e.g. 03_scwg_khandelwal)
    # These contain further subfolders of reference CSVs
    for item in os.listdir(category_path):
        item_path = os.path.join(category_path, item)
        if os.path.isdir(item_path):
            for sub in os.listdir(item_path):
                sub_path = os.path.join(item_path, sub)
                if os.path.isdir(sub_path) and sub.startswith(padded + "_"):
                    return sub_path

    return None


def get_table_files(folder_path: str) -> list[tuple[str, str]]:
    """
    Return list of (display_name, full_path) for all table CSVs in a folder.
    Excludes table_index.csv (not a data table).
    Sorts by filename so table_01, table_02 etc. appear in order.
    """
    if not folder_path or not os.path.isdir(folder_path):
        return []

    files = []
    for fname in sorted(os.listdir(folder_path)):
        if fname.endswith(".csv") and fname != "table_index.csv":
            full_path = os.path.join(folder_path, fname)
            # Build a readable display name from the filename
            display = fname.replace(".csv", "")
            # e.g. table_01_ultimate_analysis_of_biomass
            # → Table 01 — Ultimate analysis of biomass
            m = re.match(r"table_([S\d]+)_(.*)", display)
            if m:
                num  = m.group(1).lstrip("0") or "0"
                desc = m.group(2).replace("_", " ").strip().capitalize()
                display = f"Table {num} — {desc}"
            files.append((display, full_path))

    return files


def has_table_index(folder_path: str) -> bool:
    if not folder_path:
        return False
    return os.path.isfile(os.path.join(folder_path, "table_index.csv"))


# ── Status badge helpers ──────────────────────────────────────────────────────

def _status_chip(label: str, value: str) -> str:
    """Return a coloured markdown badge for a Yes/No status value."""
    v = str(value).strip()
    if v == "Yes":
        colour, icon = "#2A9D8F", "✅"
    elif v == "No":
        colour, icon = "#E76F51", "❌"
    else:
        colour, icon = "#aaaaaa", "❓"
    return (
        f'<span style="background:{colour}22; border:1px solid {colour}; '
        f'border-radius:100px; padding:3px 10px; font-size:0.78rem; '
        f'color:{colour}; white-space:nowrap;">{icon} {label}</span>'
    )


# ── Main page ─────────────────────────────────────────────────────────────────

def show_dataset_viewer():
    st.header("🧪 Dataset Viewer")
    st.markdown(
        "Browse simulation-ready datasets extracted from the reviewed papers. "
        "Select a paper to explore its tables, check data availability status, "
        "and download individual tables as CSV files."
    )

    master = load_master()

    # ── Filter to simulation-useful papers only ───────────────────────────────
    useful = master[
        master["Data useful for simulations"].str.strip() == "Yes"
    ].copy()
    useful["Serial_int"] = useful["Serial"].astype(int)
    useful = useful.sort_values("Serial_int").reset_index(drop=True)

    if useful.empty:
        st.warning("No papers marked as simulation-useful in the master CSV yet.")
        return

    # ── Paper selector ────────────────────────────────────────────────────────
    st.subheader("📂 Select Paper")

    paper_options = {
        f"#{row['Serial']}  —  {row['Title'][:70]}{'…' if len(row['Title']) > 70 else ''}": row["Serial"]
        for _, row in useful.iterrows()
    }

    selected_label = st.selectbox(
        "Choose a paper:",
        list(paper_options.keys()),
        label_visibility="collapsed",
    )
    selected_serial = paper_options[selected_label]
    row = master[master["Serial"] == selected_serial].iloc[0]

    st.markdown("---")

    # ── Paper metadata card ───────────────────────────────────────────────────
    st.subheader("📋 Paper Information")

    # Title + year
    st.markdown(
        f"<h4 style='margin-bottom:4px;'>{row['Title']}</h4>"
        f"<p style='color:#666; margin-top:0;'>{row['Author']} &nbsp;·&nbsp; "
        f"{row['Year']} &nbsp;·&nbsp; <em>{row['Journal']}</em></p>",
        unsafe_allow_html=True,
    )

    # Metadata chips row
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"**⚗️ Route**\n\n{row.get('Hydrogen_Route', '—')}")
    c2.markdown(f"**🌿 Feedstock**\n\n{row.get('Feedstock', '—')}")
    c3.markdown(f"**🗂️ Dataset Type**\n\n{row.get('Dataset_Type', '—')}")
    ds_size = row.get("Dataset_Size_Numeric", "")
    c4.markdown(f"**📏 Dataset Size**\n\n{ds_size if str(ds_size).strip() not in ['', 'nan'] else 'Not reported'}")

    # ── Data availability status note ─────────────────────────────────────────
    st.markdown("**📊 Data Availability Status**")

    chips = (
        _status_chip("Data Provided by Authors",     row.get("Data provided",                "nan")) + "&emsp;" +
        _status_chip("Data Extractable from Tables", row.get("Data from tables",              "nan")) + "&emsp;" +
        _status_chip("Useful for Simulations",       row.get("Data useful for simulations",   "nan"))
    )
    st.markdown(chips, unsafe_allow_html=True)
    st.markdown("")

    # Dataset notes
    notes = str(row.get("Dataset_Notes", "")).strip()
    if notes and notes.lower() != "nan":
        st.caption(f"📝 {notes}")

    # ── Drive link buttons ────────────────────────────────────────────────────
    btn_col1, btn_col2, _ = st.columns([1, 1, 3])

    paper_link = str(row.get("Drive_Link", "")).strip()
    if paper_link.startswith("http"):
        btn_col1.link_button("📄 Open Paper", paper_link)

    dataset_link = str(row.get("Dataset_Drive_Link", "")).strip()
    if dataset_link.startswith("http"):
        btn_col2.link_button("🗃️ Open Dataset File", dataset_link)

    st.markdown("---")

    # ── Dataset tables ────────────────────────────────────────────────────────
    st.subheader("📊 Dataset Tables")

    category    = get_category(str(row.get("Hydrogen_Route", "")))
    folder_path = find_paper_folder(selected_serial, category)
    table_files = get_table_files(folder_path) if folder_path else []

    # Check for table_index.csv (data exists but not yet extracted)
    if not table_files and has_table_index(folder_path):
        index_df = pd.read_csv(os.path.join(folder_path, "table_index.csv"))
        st.info(
            "📋 This paper's data exists in its tables but has not yet been "
            "extracted into CSV format. The following tables are available in "
            "the paper — open it via the Drive link above to access the data."
        )
        for _, trow in index_df.iterrows():
            st.markdown(f"- {trow['Table']}")
        return

    if not table_files:
        st.info(
            "No dataset CSV files found for this paper yet. "
            "Check the data availability status above — if 'Data Provided' "
            "or 'Data from Tables' is Yes, the files may still need to be "
            "collected and processed."
        )
        return

    st.caption(
        f"Found **{len(table_files)}** table{'s' if len(table_files) != 1 else ''} "
        f"for this paper. Select one to view and download."
    )

    # ── Table selector tabs (up to 8) or dropdown (more than 8) ──────────────
    if len(table_files) <= 8:
        tab_labels  = [display for display, _ in table_files]
        tab_objects = st.tabs(tab_labels)

        for tab, (display, fpath) in zip(tab_objects, table_files):
            with tab:
                _render_table(display, fpath)
    else:
        table_map = {display: fpath for display, fpath in table_files}
        selected_table = st.selectbox(
            "Select table:",
            list(table_map.keys()),
        )
        _render_table(selected_table, table_map[selected_table])


# ── Table renderer ────────────────────────────────────────────────────────────

def _render_table(display_name: str, filepath: str):
    """Load and display one table CSV with search and download."""
    try:
        df = pd.read_csv(filepath, dtype=str)
    except Exception as e:
        st.error(f"Could not load table: {e}")
        return

    # Clean up: replace NaN display with empty string
    df = df.fillna("")

    st.caption(f"**{len(df)}** rows × **{len(df.columns)}** columns")

    # ── Search within table ───────────────────────────────────────────────────
    search = st.text_input(
        "🔍 Search within this table:",
        key=f"search_{os.path.basename(filepath)}",
        placeholder="Type to filter rows…",
    )

    if search.strip():
        mask = df.apply(
            lambda col: col.str.contains(search.strip(), case=False, na=False)
        ).any(axis=1)
        display_df = df[mask].reset_index(drop=True)
        st.caption(f"Showing {len(display_df)} matching rows")
    else:
        display_df = df

    # ── Dataframe ─────────────────────────────────────────────────────────────
    st.dataframe(
        display_df,
        width='stretch',
        height=min(600, 45 + len(display_df) * 35),
        hide_index=True,
    )

    # ── Download button ───────────────────────────────────────────────────────
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    fname     = os.path.basename(filepath)
    st.download_button(
        label=f"⬇️ Download {fname}",
        data=csv_bytes,
        file_name=fname,
        mime="text/csv",
        key=f"dl_{fname}",
    )


# ── Entry point ───────────────────────────────────────────────────────────────
show_dataset_viewer()
