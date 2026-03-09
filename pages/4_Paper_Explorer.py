import streamlit as st
import pandas as pd
import re

# ── Load & merge data ────────────────────────────────────────────────────────
papers    = pd.read_csv("database/papers_cleaned.csv")
summaries = pd.read_csv("database/technical_summaries.csv")
papers    = papers.merge(summaries, on="Serial", how="left")

# ── Text cleaning helpers ────────────────────────────────────────────────────

# Fix corrupted subscript/superscript characters that appear as "?"
# Pattern: letter immediately followed by ? where the ? is a garbled unicode subscript
_CHEM_FIX = [
    # ── Specific compounds first (before generic single-letter rules) ──────
    (r'Na\?CO\?',          "Na₂CO₃"),
    (r'K\?CO\?',           "K₂CO₃"),
    (r'Fe\?O\?',           "Fe₃O₄"),
    (r'ZrO\?',             "ZrO₂"),
    (r'CeO\?',             "CeO₂"),
    (r'H\?O\b',            "H₂O"),
    (r'H\?S\b',            "H₂S"),
    (r'NH\?',              "NH₃"),
    (r'bioH\?',            "bioH₂"),
    (r'CH\?',              "CH₄"),
    # ── Unit separators: digit?° → digit °  |  digit?[UNIT] → digit UNIT ──
    (r'(\d)\?°',           r"\1 °"),
    (r'(\d)\?([A-Z])',     r"\1 \2"),
    # ── Generic chemical subscripts ────────────────────────────────────────
    (r'\bH\?',             "H₂"),
    (r'\bCO\?',            "CO₂"),
    (r'CO\?\b',            "CO₂"),
    (r'\bN\?\b',           "N₂"),
    (r'\bO\?\b',           "O₂"),
    # ── Arrow: word <space> ? <space> word ─────────────────────────────────
    (r'(?<=\w)\s\?\s(?=\w)',  " → "),
]


def _fix_chemistry(text: str) -> str:
    """Replace garbled chemistry symbols and arrows."""
    if not isinstance(text, str):
        return text
    for pattern, replacement in _CHEM_FIX:
        text = re.sub(pattern, replacement, text)
    return text


def _bullet_to_markdown(text: str) -> str:
    """
    Convert the raw CSV bullet format into clean Markdown.

    Raw format uses:
      •\\t  — top-level bullet
      o\\t  — sub-bullet (indented)
      \\n   — line break

    Output: proper Markdown bullet list with sub-items indented.
    """
    if not isinstance(text, str):
        return ""

    text = _fix_chemistry(text)

    lines = []
    for raw_line in text.split("\n"):
        line = raw_line.strip()
        if not line or line in (" ", "\t"):
            continue

        if line.startswith("•\t") or line.startswith("•"):
            content = line.lstrip("•").lstrip("\t").strip()
            if content:
                lines.append(f"- {content}")

        elif line.startswith("o\t") or line.startswith("o "):
            content = line[1:].lstrip("\t").strip()
            if content:
                lines.append(f"  - {content}")   # 2-space indent = sub-bullet

        else:
            # Plain prose line (some fields have paragraph text, not bullets)
            if lines and not lines[-1].endswith("\n"):
                # Append to previous line if it's prose continuation
                if not lines[-1].startswith("-") and not lines[-1].startswith("  -"):
                    lines[-1] += " " + line
                else:
                    lines.append(line)
            else:
                lines.append(line)

    return "\n".join(lines)


def _parse_basic_info(text: str) -> dict:
    """
    Parse the 'Basic Information' bullet field into a clean dict.
    Keys extracted: Title, Authors, Journal, Year, Country, Type.
    Falls back to the merged papers columns if parsing fails.
    """
    info = {}
    if not isinstance(text, str):
        return info

    text = _fix_chemistry(text)
    for line in text.split("\n"):
        line = line.strip().lstrip("•").lstrip("\t").strip()
        for key in ["Title", "Authors", "Journal", "Year", "Country", "Type",
                    "Country of study", "Country/Region"]:
            if line.lower().startswith(key.lower() + ":"):
                value = line[len(key) + 1:].strip()
                canonical = (
                    "Country" if "country" in key.lower()
                    else key.split()[0].title()
                )
                info[canonical] = value
                break
    return info


# ── Badge helpers ────────────────────────────────────────────────────────────

_TYPE_COLOURS = {
    "Review":            ("🔵", "#2E86AB"),
    "Original Research": ("🟢", "#2A9D8F"),
    "Simulation":        ("🟠", "#F4A261"),
}
_ROUTE_ICON = "⚗️"
_ML_ICON    = "🤖"


def _type_badge(study_type: str) -> str:
    icon, _ = _TYPE_COLOURS.get(study_type, ("⚪", "#888"))
    return f"{icon} {study_type}"


def _r2_colour(r2) -> str:
    try:
        v = float(r2)
        if v >= 0.95: return "🟢"
        if v >= 0.85: return "🟡"
        return "🔴"
    except Exception:
        return "⚪"


# ── Render one full paper card ───────────────────────────────────────────────

def _render_paper_card(row: pd.Series):
    """Full expanded view of a single paper."""

    # ── Title bar ──
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
            border-radius: 12px;
            padding: 24px 28px 20px 28px;
            margin-bottom: 8px;
        ">
            <p style="color:#a0c4ff; font-size:0.78rem; margin:0 0 6px 0; letter-spacing:0.08em; text-transform:uppercase;">
                Paper #{int(row['Serial'])} &nbsp;·&nbsp; {row.get('Year','')}
            </p>
            <h2 style="color:#ffffff; font-size:1.25rem; margin:0 0 12px 0; line-height:1.4;">
                {row['Title']}
            </h2>
            <p style="color:#c8d8e8; font-size:0.88rem; margin:0;">
                👤 {row['Author']}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Meta row ──
    c1, c2, c3, c4 = st.columns([2, 2, 1.2, 1])
    c1.markdown(f"📰 **Journal**\n\n{row.get('Journal','—')}")
    c2.markdown(f"🌍 **Country / Region**\n\n{row.get('Country_Region','—')}")
    c3.markdown(f"📋 **Study Type**\n\n{_type_badge(str(row.get('Type','—')))}")

    r2_val = row.get("Best_R2", "")
    r2_display = f"{_r2_colour(r2_val)} **{r2_val}**" if str(r2_val).strip() else "—"
    c4.markdown(f"📈 **Best R²**\n\n{r2_display}")

    st.markdown("---")

    # ── Quick-glance chips ──
    chips_md = ""
    route = str(row.get("Hydrogen_Route", "")).strip()
    if route:
        chips_md += f"**{_ROUTE_ICON} Route:** `{route}`&emsp;"

    feedstock = str(row.get("Feedstock", "")).strip()
    if feedstock:
        chips_md += f"**🌿 Feedstock:** `{feedstock}`&emsp;"

    ds_type = str(row.get("Dataset_Type", "")).strip()
    ds_size = str(row.get("Dataset_Size_Numeric", "")).strip()
    if ds_type:
        size_str = f" ({ds_size} samples)" if ds_size and ds_size.lower() not in ("nan", "") else ""
        chips_md += f"**🗃️ Dataset:** `{ds_type}{size_str}`&emsp;"

    flags = []
    for label, col in [("Integrated System", "Integrated_System"),
                        ("Carbon Capture", "Carbon_Capture"),
                        ("LCA", "LCA"),
                        ("TEA", "TEA")]:
        val = str(row.get(col, "No")).strip().lower()
        if val in ("yes", "partial"):
            flags.append(f"✅ {label}")
    if flags:
        chips_md += "  \n" + " &emsp; ".join(flags)

    if chips_md:
        st.markdown(chips_md, unsafe_allow_html=True)
        st.markdown("")

    # ── Drive link ──
    drive_link = row.get("Drive_Link", "")
    if pd.notna(drive_link) and str(drive_link).strip().startswith("http"):
        st.link_button("📂 Open Paper in Google Drive", str(drive_link).strip())

    st.markdown("---")

    # ── ML snapshot ──
    with st.expander("🤖 ML Snapshot", expanded=True):
        m1, m2, m3 = st.columns(3)

        algos = str(row.get("ML_Algorithms", "")).strip()
        m1.markdown("**Algorithms Used**")
        if algos and algos.lower() != "nan":
            for a in algos.split(";"):
                a = a.strip()
                if a:
                    m1.markdown(f"- `{a}`")
        else:
            m1.markdown("—")

        opt = str(row.get("Optimization_Method_Normalised", "")).strip()
        m2.markdown("**Optimisation Methods**")
        if opt and opt.lower() != "nan":
            for o in opt.split(";"):
                o = o.strip()
                if o:
                    m2.markdown(f"- `{o}`")
        else:
            m2.markdown("—")

        interp = str(row.get("Interpretability_Method_Normalised", "")).strip()
        m3.markdown("**Interpretability**")
        if interp and interp.lower() != "nan":
            for i in interp.split(";"):
                i = i.strip()
                if i:
                    m3.markdown(f"- `{i}`")
        else:
            m3.markdown("—")

        kpm = str(row.get("Key_Performance_Metric", "")).strip()
        if kpm and kpm.lower() != "nan":
            st.markdown(f"**🎯 Key Performance Metric:** {kpm}")

    # ── Technical Summary sections ──────────────────────────────────────────
    _SECTIONS = [
        ("Research Objective",      "🎯", "Research Objective",      True),
        ("System Description",      "⚙️", "System Description",      False),
        ("Modelling Approach",      "🔧", "Modelling Approach",       False),
        ("Machine Learning Component", "🤖", "Machine Learning Component", False),
        ("Key Results",             "📊", "Key Results",              True),
        ("Strengths",               "✅", "Strengths",                False),
        ("Limitations",             "⚠️", "Limitations",              False),
        ("Research Gap Identified", "🔭", "Research Gap Identified",  False),
    ]

    st.markdown("### 📑 Technical Summary")

    for col_name, icon, label, expanded in _SECTIONS:
        raw = row.get(col_name, "")
        if not isinstance(raw, str) or not raw.strip():
            continue

        md_content = _bullet_to_markdown(raw)
        if not md_content.strip():
            continue

        with st.expander(f"{icon} {label}", expanded=expanded):
            st.markdown(md_content)

    # ── Research gaps ──
    gap = str(row.get("Research_Gap_Category", "")).strip()
    if gap and gap.lower() != "nan":
        st.markdown("**🔭 Research Gap Category:**")
        for g in gap.split(";"):
            g = g.strip()
            if g:
                st.markdown(f"- {g}")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE LAYOUT
# ══════════════════════════════════════════════════════════════════════════════

def show_paper_explorer(df: pd.DataFrame):

    st.header("📚 Paper Explorer")
    st.markdown(
        "Browse all **29 hydrogen ML papers** in the collection. "
        "Search, filter, and select any paper to read its full technical summary."
    )

    # ── SEARCH + FILTER FORM ──────────────────────────────────────────────
    st.subheader("🔍 Search & Filter")

    with st.form(key="explorer_form"):

        search_query = st.text_input(
            "Search by title, author, or journal:",
            placeholder="e.g. dark fermentation, XGBoost, Biomass and Bioenergy …",
        )

        col1, col2 = st.columns(2)

        with col1:
            year_filter = st.multiselect(
                "Year:",
                sorted(df["Year"].dropna().astype(str).unique()),
            )
            route_filter = st.multiselect(
                "Hydrogen Route:",
                sorted(df["Hydrogen_Route"].dropna().str.strip().unique()),
            )
            feedstock_filter = st.multiselect(
                "Feedstock (contains):",
                sorted(
                    df["Feedstock"].dropna()
                    .str.replace(",", ";").str.split(";").explode()
                    .str.strip().dropna().unique()
                ),
            )
            type_filter = st.multiselect(
                "Study Type:",
                sorted(df["Type"].dropna().str.strip().unique()),
            )

        with col2:
            ml_family_filter = st.multiselect(
                "ML Family:",
                sorted(
                    df["ML_Family"].dropna()
                    .str.split(";").explode()
                    .str.strip().dropna().unique()
                ),
            )
            dataset_filter = st.multiselect(
                "Dataset Type:",
                sorted(df["Dataset_Type"].dropna().str.strip().unique()),
            )
            integrated_filter = st.selectbox(
                "Integrated System?", ["Any", "Yes", "No"]
            )
            lca_filter = st.selectbox(
                "LCA Performed?", ["Any", "Yes", "No"]
            )

        submitted = st.form_submit_button("🔎 Apply Filters", width='stretch')

    # ── APPLY FILTERS ────────────────────────────────────────────────────
    if submitted:
        filtered = df.copy()

        if search_query:
            q = search_query.lower()
            filtered = filtered[
                filtered["Title"].str.lower().str.contains(q, na=False)
                | filtered["Author"].str.lower().str.contains(q, na=False)
                | filtered["Journal"].str.lower().str.contains(q, na=False)
            ]
        if year_filter:
            filtered = filtered[filtered["Year"].astype(str).isin(year_filter)]
        if route_filter:
            filtered = filtered[filtered["Hydrogen_Route"].isin(route_filter)]
        if feedstock_filter:
            filtered = filtered[
                filtered["Feedstock"].str.contains(
                    "|".join(feedstock_filter), case=False, na=False
                )
            ]
        if type_filter:
            filtered = filtered[filtered["Type"].isin(type_filter)]
        if ml_family_filter:
            filtered = filtered[
                filtered["ML_Family"].str.contains(
                    "|".join(ml_family_filter), case=False, na=False
                )
            ]
        if dataset_filter:
            filtered = filtered[filtered["Dataset_Type"].isin(dataset_filter)]
        if integrated_filter != "Any":
            filtered = filtered[
                filtered["Integrated_System"].str.strip().str.title()
                == integrated_filter
            ]
        if lca_filter != "Any":
            filtered = filtered[
                filtered["LCA"].str.strip().str.title() == lca_filter
            ]

        st.session_state["explorer_filtered"] = filtered

    filtered = st.session_state.get("explorer_filtered", df)

    # ── RESULTS TABLE ─────────────────────────────────────────────────────
    st.subheader("📋 Results")
    st.caption(f"Showing **{len(filtered)}** of **{len(df)}** papers.")

    table_cols = [
        "Serial", "Title", "Author", "Year", "Journal",
        "Type", "Hydrogen_Route", "Feedstock",
        "Dataset_Type", "ML_Algorithms", "Best_R2",
        "Integrated_System", "LCA",
    ]
    table_cols = [c for c in table_cols if c in filtered.columns]

    st.dataframe(
        filtered[table_cols].reset_index(drop=True),
        width='stretch',
        height=280,
    )

    # ── PAPER SELECTOR ────────────────────────────────────────────────────
    if filtered.empty:
        st.info("No papers match the current filters. Try adjusting your search criteria.")
        return

    st.markdown("---")
    st.subheader("📖 Paper Detail View")

    # Build a nicely labelled selector: "1 — Title of Paper"
    options = {
        f"#{int(r['Serial'])}  —  {r['Title'][:80]}{'…' if len(r['Title']) > 80 else ''}": int(r["Serial"])
        for _, r in filtered.iterrows()
    }

    selected_label = st.selectbox(
        "Select a paper to read its full technical summary:",
        list(options.keys()),
    )

    if selected_label:
        selected_serial = options[selected_label]
        row = df[df["Serial"] == selected_serial].iloc[0]
        st.markdown("")
        _render_paper_card(row)


# ── Entry point ───────────────────────────────────────────────────────────────
show_paper_explorer(papers)
