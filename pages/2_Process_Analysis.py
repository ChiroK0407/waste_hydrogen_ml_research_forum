import streamlit as st
import altair as alt
import pandas as pd
import importlib.util
import os

# ── Import the process dictionary from database/ ────────────────────────────
_dict_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "process_dictionary.py")
_spec = importlib.util.spec_from_file_location("process_dictionary", _dict_path)
_mod  = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
PROCESS_DICTIONARY = _mod.PROCESS_DICTIONARY

df = pd.read_csv("database/papers_cleaned.csv")

# ── Colour palettes for charts ───────────────────────────────────────────────
ROUTE_PALETTE = [
    "#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#3B1F2B",
    "#44BBA4", "#E94F37", "#393E41", "#F5A623", "#7B2D8B",
    "#1A936F", "#88D498", "#C6DABF", "#F4E9CD", "#114B5F",
    "#E8D5B7", "#9B2335",
]
FEEDSTOCK_PALETTE = [
    "#264653", "#2A9D8F", "#E9C46A", "#F4A261", "#E76F51",
    "#457B9D", "#1D3557", "#A8DADC", "#F1FAEE", "#E63946",
    "#6A0572", "#AB83A1", "#C9CBA3", "#FFE1A8",
]
BOOL_PALETTE    = {"Yes": "#2A9D8F", "No": "#E76F51"}
TYPE_PALETTE    = {"Original Research": "#2E86AB", "Simulation": "#F18F01", "Review": "#A23B72"}
COUNTRY_PALETTE = [
    "#264653","#2A9D8F","#E9C46A","#F4A261","#E76F51",
    "#457B9D","#6A0572","#AB83A1","#C9CBA3","#1D3557",
    "#A8DADC","#F1FAEE","#E63946","#88D498","#44BBA4",
    "#F5A623","#7B2D8B","#1A936F","#C73E1D","#114B5F",
    "#9B2335","#F18F01",
]

# ── Helper: load a colour scale for Altair ──────────────────────────────────
def _colour_scale(domain: list, palette: list) -> alt.Scale:
    colours = (palette * ((len(domain) // len(palette)) + 1))[: len(domain)]
    return alt.Scale(domain=domain, range=colours)


# ── Helper: explode a semi-colon-separated column ───────────────────────────
def _explode(series: pd.Series, col_name: str) -> pd.DataFrame:
    return (
        series.dropna()
        .str.replace(",", ";")
        .str.split(";")
        .explode()
        .str.strip()
        .reset_index(name=col_name)
    )


# ── Helper: render a process dictionary entry ────────────────────────────────
def _render_route(info: dict):
    # Metadata row
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"**Category:** `{info.get('category', 'N/A')}`")
    c2.markdown(f"**Temp range:** `{info.get('temp_range', 'N/A')}`")
    c3.markdown(f"**Pressure:** `{info.get('pressure_range', 'N/A')}`")

    st.markdown("**Description**")
    st.info(info.get("description", ""))

    h2 = info.get("h2_yield_range", "")
    if h2:
        st.markdown(f"**⚗️ H₂ yield range:** {h2}")

    # Inputs / Outputs
    c1, c2 = st.columns(2)
    ki = info.get("key_inputs", [])
    ko = info.get("key_outputs", [])
    if ki:
        with c1:
            st.markdown("**🔩 Key Inputs**")
            for i in ki:
                st.markdown(f"- {i}")
    if ko:
        with c2:
            st.markdown("**🧪 Key Outputs**")
            for o in ko:
                st.markdown(f"- {o}")

    # Strengths / Limitations
    s = info.get("strengths", [])
    l = info.get("limitations", [])
    if s or l:
        c1, c2 = st.columns(2)
        if s:
            with c1:
                st.markdown("**✅ Strengths**")
                for item in s:
                    st.markdown(f"- {item}")
        if l:
            with c2:
                st.markdown("**⚠️ Limitations**")
                for item in l:
                    st.markdown(f"- {item}")

    ml = info.get("ml_applications", "")
    if ml:
        st.markdown(f"**🤖 ML Applications in literature:** {ml}")


def _render_feedstock(info: dict):
    c1, c2 = st.columns(2)
    c1.markdown(f"**Category:** `{info.get('category', 'N/A')}`")
    c2.markdown(f"**Origin:** {info.get('origin', 'N/A')}")

    comp = info.get("composition", "")
    if comp:
        st.markdown(f"**Composition:** {comp}")

    st.markdown("**Description**")
    st.info(info.get("description", ""))

    routes = info.get("suitable_routes", [])
    h2 = info.get("h2_potential", "")
    if routes or h2:
        c1, c2 = st.columns(2)
        if routes:
            with c1:
                st.markdown("**🔗 Suitable H₂ Routes**")
                for r in routes:
                    st.markdown(f"- {r}")
        if h2:
            c2.markdown(f"**⚗️ H₂ Potential:** {h2}")

    ki = info.get("key_ml_inputs", [])
    s  = info.get("strengths", [])
    lm = info.get("limitations", [])

    if ki:
        st.markdown("**🔢 Key ML Model Inputs**")
        st.markdown("  " + " · ".join([f"`{i}`" for i in ki]))

    if s or lm:
        c1, c2 = st.columns(2)
        if s:
            with c1:
                st.markdown("**✅ Strengths**")
                for item in s:
                    st.markdown(f"- {item}")
        if lm:
            with c2:
                st.markdown("**⚠️ Limitations**")
                for item in lm:
                    st.markdown(f"- {item}")


# ── Main page ────────────────────────────────────────────────────────────────
def show_process_analysis(df: pd.DataFrame):
    st.header("⚗️ Process Analysis Dashboard")
    st.markdown("""
    Explore the **hydrogen production routes, feedstocks, and process characteristics**
    across all reviewed papers. Charts show the full dataset; use the query form below
    to filter papers and drill into specific process combinations.
    """)

    # ════════════════════════════════════════════════════════════════════════
    # 1. DISTRIBUTION CHARTS
    # ════════════════════════════════════════════════════════════════════════
    st.subheader("📊 Dataset Overview")

    # ── Row 1: Hydrogen Routes + Feedstock ──────────────────────────────────
    col_left, col_right = st.columns(2)

    with col_left:
        route_df = _explode(df["Hydrogen_Route"], "Hydrogen_Route")
        domain_r = sorted(route_df["Hydrogen_Route"].unique().tolist())
        chart_route = (
            alt.Chart(route_df)
            .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
            .encode(
                x=alt.X("Hydrogen_Route:N", sort="-y",
                        axis=alt.Axis(labelAngle=-40, labelLimit=160, title="Hydrogen Route")),
                y=alt.Y("count():Q", axis=alt.Axis(title="Number of Papers")),
                color=alt.Color("Hydrogen_Route:N",
                                scale=_colour_scale(domain_r, ROUTE_PALETTE),
                                legend=None),
                tooltip=[
                    alt.Tooltip("Hydrogen_Route:N", title="Route"),
                    alt.Tooltip("count():Q", title="Papers"),
                ],
            )
            .properties(title="Hydrogen Production Routes", height=320)
        )
        st.altair_chart(chart_route, width='stretch')

    with col_right:
        feed_df = _explode(df["Feedstock"], "Feedstock")
        domain_f = sorted(feed_df["Feedstock"].unique().tolist())
        chart_feed = (
            alt.Chart(feed_df)
            .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
            .encode(
                x=alt.X("Feedstock:N", sort="-y",
                        axis=alt.Axis(labelAngle=-40, labelLimit=160, title="Feedstock")),
                y=alt.Y("count():Q", axis=alt.Axis(title="Number of Papers")),
                color=alt.Color("Feedstock:N",
                                scale=_colour_scale(domain_f, FEEDSTOCK_PALETTE),
                                legend=None),
                tooltip=[
                    alt.Tooltip("Feedstock:N", title="Feedstock"),
                    alt.Tooltip("count():Q", title="Papers"),
                ],
            )
            .properties(title="Feedstock Distribution", height=320)
        )
        st.altair_chart(chart_feed, width='stretch')

    # ── Row 2: Paper Type + Country/Region ──────────────────────────────────
    col_left2, col_right2 = st.columns(2)

    with col_left2:
        type_df = _explode(df["Type"], "Type")
        domain_t = sorted(type_df["Type"].unique().tolist())
        chart_type = (
            alt.Chart(type_df)
            .mark_arc(innerRadius=55, outerRadius=110)
            .encode(
                theta=alt.Theta("count():Q"),
                color=alt.Color("Type:N",
                                scale=alt.Scale(
                                    domain=domain_t,
                                    range=[TYPE_PALETTE.get(d, "#888") for d in domain_t]
                                ),
                                legend=alt.Legend(title="Paper Type")),
                tooltip=[
                    alt.Tooltip("Type:N", title="Type"),
                    alt.Tooltip("count():Q", title="Papers"),
                ],
            )
            .properties(title="Study Type Distribution", height=280)
        )
        st.altair_chart(chart_type, width='stretch')

    with col_right2:
        country_df = _explode(df["Country_Region"], "Country_Region")
        domain_c = sorted(country_df["Country_Region"].unique().tolist())
        chart_country = (
            alt.Chart(country_df)
            .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
            .encode(
                x=alt.X("count():Q", axis=alt.Axis(title="Papers")),
                y=alt.Y("Country_Region:N", sort="-x",
                        axis=alt.Axis(title="Country / Region", labelLimit=200)),
                color=alt.Color("Country_Region:N",
                                scale=_colour_scale(domain_c, COUNTRY_PALETTE),
                                legend=None),
                tooltip=[
                    alt.Tooltip("Country_Region:N", title="Country/Region"),
                    alt.Tooltip("count():Q", title="Papers"),
                ],
            )
            .properties(title="Country / Region Distribution", height=380)
        )
        st.altair_chart(chart_country, width='stretch')

    # ── Row 3: Boolean system flags ──────────────────────────────────────────
    st.markdown("**System & Analysis Flags**")

    flag_cols = {
        "Integrated System": "Integrated_System",
        "Carbon Capture": "Carbon_Capture",
        "Surrogate Model": "Surrogate_Model",
        "Dynamic Modelling": "Dynamic_Modelling",
        "LCA": "LCA",
    }
    flag_charts = []
    for label, col in flag_cols.items():
        counts = df[col].fillna("No").str.strip().value_counts().reset_index()
        counts.columns = ["Value", "Count"]
        counts["Flag"] = label
        flag_charts.append(counts)

    flags_df = pd.concat(flag_charts, ignore_index=True)
    domain_v = ["Yes", "No"]

    chart_flags = (
        alt.Chart(flags_df)
        .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
        .encode(
            x=alt.X("Flag:N", axis=alt.Axis(title=None, labelAngle=0)),
            y=alt.Y("Count:Q", axis=alt.Axis(title="Papers")),
            color=alt.Color("Value:N",
                            scale=alt.Scale(
                                domain=domain_v,
                                range=[BOOL_PALETTE["Yes"], BOOL_PALETTE["No"]]
                            ),
                            legend=alt.Legend(title="Present?")),
            xOffset="Value:N",
            tooltip=[
                alt.Tooltip("Flag:N", title="Flag"),
                alt.Tooltip("Value:N", title="Present?"),
                alt.Tooltip("Count:Q", title="Papers"),
            ],
        )
        .properties(title="System & Analysis Feature Flags", height=280)
    )
    st.altair_chart(chart_flags, width='stretch')

    # ── Row 4: Dataset type + Year ───────────────────────────────────────────
    col_l4, col_r4 = st.columns(2)

    with col_l4:
        ds_df = _explode(df["Dataset_Type"], "Dataset_Type")
        domain_ds = sorted(ds_df["Dataset_Type"].unique().tolist())
        chart_ds = (
            alt.Chart(ds_df)
            .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
            .encode(
                x=alt.X("Dataset_Type:N", sort="-y",
                        axis=alt.Axis(labelAngle=-30, title="Dataset Type")),
                y=alt.Y("count():Q", axis=alt.Axis(title="Papers")),
                color=alt.Color("Dataset_Type:N",
                                scale=_colour_scale(domain_ds, ROUTE_PALETTE),
                                legend=None),
                tooltip=[
                    alt.Tooltip("Dataset_Type:N", title="Dataset Type"),
                    alt.Tooltip("count():Q", title="Papers"),
                ],
            )
            .properties(title="Dataset Type Used", height=280)
        )
        st.altair_chart(chart_ds, width='stretch')

    with col_r4:
        year_df = df["Year"].dropna().astype(str).str.strip().value_counts().reset_index()
        year_df.columns = ["Year", "Count"]
        year_df = year_df.sort_values("Year")
        chart_year = (
            alt.Chart(year_df)
            .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4, color="#2E86AB")
            .encode(
                x=alt.X("Year:O", axis=alt.Axis(title="Publication Year")),
                y=alt.Y("Count:Q", axis=alt.Axis(title="Papers")),
                tooltip=[
                    alt.Tooltip("Year:O", title="Year"),
                    alt.Tooltip("Count:Q", title="Papers"),
                ],
            )
            .properties(title="Papers by Publication Year", height=280)
        )
        st.altair_chart(chart_year, width='stretch')

    # ════════════════════════════════════════════════════════════════════════
    # 2. QUERY FORM
    # ════════════════════════════════════════════════════════════════════════
    st.subheader("🔍 Query Papers")

    with st.form(key="process_query_form"):

        col_a, col_b = st.columns(2)

        with col_a:
            route_filter = st.multiselect(
                "Filter by Hydrogen Route:",
                sorted(df["Hydrogen_Route"].dropna().str.strip().unique()),
            )
            feedstock_filter = st.multiselect(
                "Filter by Feedstock:",
                sorted(_explode(df["Feedstock"], "Feedstock")["Feedstock"].unique()),
            )
            type_filter = st.multiselect(
                "Filter by Study Type:",
                sorted(df["Type"].dropna().str.strip().unique()),
            )
            year_filter = st.multiselect(
                "Filter by Year:",
                sorted(df["Year"].dropna().astype(str).str.strip().unique()),
            )

        with col_b:
            country_filter = st.text_input("Search by Country / Region:")
            journal_filter = st.text_input("Search by Journal:")
            integrated_filter = st.selectbox(
                "Integrated System?", options=["Any", "Yes", "No"]
            )
            carbon_filter = st.selectbox(
                "Carbon Capture?", options=["Any", "Yes", "No"]
            )
            lca_filter = st.selectbox(
                "LCA Performed?", options=["Any", "Yes", "No"]
            )
            dataset_filter = st.multiselect(
                "Filter by Dataset Type:",
                sorted(df["Dataset_Type"].dropna().str.strip().unique()),
            )

        submitted = st.form_submit_button("🔎 Apply Filters", width='stretch')

    # ════════════════════════════════════════════════════════════════════════
    # 3. APPLY FILTERS & PERSIST IN SESSION STATE
    # ════════════════════════════════════════════════════════════════════════
    if submitted:
        filtered = df.copy()

        if route_filter:
            filtered = filtered[
                filtered["Hydrogen_Route"].str.contains(
                    "|".join([r.replace("(", r"\(").replace(")", r"\)").replace("+", r"\+")
                              for r in route_filter]),
                    case=False, na=False, regex=True,
                )
            ]
        if feedstock_filter:
            filtered = filtered[
                filtered["Feedstock"].str.contains(
                    "|".join(feedstock_filter), case=False, na=False
                )
            ]
        if type_filter:
            filtered = filtered[filtered["Type"].isin(type_filter)]
        if year_filter:
            filtered = filtered[filtered["Year"].astype(str).isin(year_filter)]
        if country_filter:
            filtered = filtered[
                filtered["Country_Region"].str.contains(country_filter, case=False, na=False)
            ]
        if journal_filter:
            filtered = filtered[
                filtered["Journal"].str.contains(journal_filter, case=False, na=False)
            ]
        if integrated_filter != "Any":
            filtered = filtered[
                filtered["Integrated_System"].str.strip().str.title() == integrated_filter
            ]
        if carbon_filter != "Any":
            filtered = filtered[
                filtered["Carbon_Capture"].str.strip().str.title() == carbon_filter
            ]
        if lca_filter != "Any":
            filtered = filtered[
                filtered["LCA"].str.strip().str.title() == lca_filter
            ]
        if dataset_filter:
            filtered = filtered[filtered["Dataset_Type"].isin(dataset_filter)]

        st.session_state["proc_filtered"] = filtered
        st.session_state["proc_active_routes"] = set(
            filtered["Hydrogen_Route"].dropna().str.strip().unique()
        )
        st.session_state["proc_active_feeds"] = set(
            _explode(filtered["Feedstock"], "Feedstock")["Feedstock"].unique()
        )

    filtered       = st.session_state.get("proc_filtered", df)
    active_routes  = st.session_state.get(
        "proc_active_routes",
        set(df["Hydrogen_Route"].dropna().str.strip().unique()),
    )
    active_feeds   = st.session_state.get(
        "proc_active_feeds",
        set(_explode(df["Feedstock"], "Feedstock")["Feedstock"].unique()),
    )

    # ════════════════════════════════════════════════════════════════════════
    # 4. RESULTS TABLE
    # ════════════════════════════════════════════════════════════════════════
    st.subheader("📚 Filtered Papers")
    st.caption(f"Showing **{len(filtered)}** of **{len(df)}** papers.")

    display_cols = [
        "Serial", "Title", "Author", "Year", "Journal",
        "Hydrogen_Route", "Feedstock", "Type", "Country_Region",
        "Dataset_Type", "Dataset_Size_Numeric",
        "Integrated_System", "Carbon_Capture", "LCA",
        "ML_Algorithms", "Best_R2", "Key_Performance_Metric", "Strengths",
    ]
    # Only include columns that exist in the dataframe
    display_cols = [c for c in display_cols if c in filtered.columns]

    st.dataframe(filtered[display_cols], width='stretch')

    # ════════════════════════════════════════════════════════════════════════
    # 5. TECHNICAL EXPLANATIONS
    # ════════════════════════════════════════════════════════════════════════
    st.subheader("📘 Technical Explanations")
    st.caption(
        "Expand any entry below for a detailed technical explanation including process chemistry, "
        "operating conditions, H₂ yield ranges, strengths, limitations, and ML applications. "
        "Entries marked ⭐ appear in the current filtered view."
    )

    tab_routes, tab_feeds = st.tabs([
        "🔬 Hydrogen Production Routes",
        "🌿 Feedstock Types",
    ])

    with tab_routes:
        st.markdown(
            "Detailed explanations for every hydrogen production route in the dataset. "
            "Methods highlighted with ⭐ appear in the **current filtered view**."
        )
        routes_dict = PROCESS_DICTIONARY["Hydrogen_Routes"]
        sorted_routes = sorted(
            routes_dict.keys(), key=lambda k: (k not in active_routes, k)
        )
        for key in sorted_routes:
            info = routes_dict[key]
            label = f"⭐ {key}" if key in active_routes else key
            full  = info.get("full_name", key)
            cat   = info.get("category", "")
            with st.expander(f"🔬 {label}  —  *{full}*  `{cat}`"):
                _render_route(info)

    with tab_feeds:
        st.markdown(
            "Detailed explanations for every feedstock type in the dataset. "
            "Entries highlighted with ⭐ appear in the **current filtered view**."
        )
        feeds_dict = PROCESS_DICTIONARY["Feedstocks"]
        sorted_feeds = sorted(
            feeds_dict.keys(), key=lambda k: (k not in active_feeds, k)
        )
        for key in sorted_feeds:
            info  = feeds_dict[key]
            label = f"⭐ {key}" if key in active_feeds else key
            full  = info.get("full_name", key)
            cat   = info.get("category", "")
            with st.expander(f"🌿 {label}  —  *{full}*  `{cat}`"):
                _render_feedstock(info)


# ── Entry point ──────────────────────────────────────────────────────────────
show_process_analysis(df)
