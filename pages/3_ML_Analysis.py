import streamlit as st
import altair as alt
import pandas as pd
import importlib.util
import os

# ── Import the dictionary from database/ ────────────────────────────────────
# ml_methods_dictionary.py lives in database/ to keep it off the sidebar.
_dict_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "ml_methods_dictionary.py")
_spec = importlib.util.spec_from_file_location("ml_methods_dictionary", _dict_path)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
ML_METHODS_DICTIONARY = _mod.ML_METHODS_DICTIONARY

df = pd.read_csv("database/papers_cleaned.csv")


# ── Helper: render one method entry as styled markdown ──────────────────────
def _render_entry(info: dict, section: str):
    """Render a dictionary entry inside an st.expander."""

    # --- Header badges ---
    if section == "ML_Algorithms":
        col1, col2 = st.columns(2)
        col1.markdown(f"**Family:** `{info.get('family', 'N/A')}`")
        col2.markdown(f"**Type:** `{info.get('type', 'N/A')}`")
    elif section == "Optimization_Methods":
        col1, col2 = st.columns(2)
        col1.markdown(f"**Category:** `{info.get('category', 'N/A')}`")
        col2.markdown(f"**When to use:** {info.get('when_to_use', 'N/A')}")
    elif section == "Interpretability_Methods":
        col1, col2, col3 = st.columns(3)
        col1.markdown(f"**Category:** `{info.get('category', 'N/A')}`")
        col2.markdown(f"**XAI Type:** `{info.get('xai_type', 'N/A')}`")
        col3.markdown(f"**Scope:** `{info.get('scope', 'N/A')}`")

    # --- Description ---
    st.markdown("**Description**")
    st.info(info.get("description", ""))

    # --- Strengths / Limitations (side by side) ---
    strengths = info.get("strengths", [])
    limitations = info.get("limitations", [])
    if strengths or limitations:
        c1, c2 = st.columns(2)
        if strengths:
            with c1:
                st.markdown("**✅ Strengths**")
                for s in strengths:
                    st.markdown(f"- {s}")
        if limitations:
            with c2:
                st.markdown("**⚠️ Limitations**")
                for lim in limitations:
                    st.markdown(f"- {lim}")

    # --- Domain-specific note ---
    domain_key = "typical_use_in_domain" if section == "ML_Algorithms" else "typical_domain_use"
    domain_note = info.get(domain_key, "")
    if domain_note:
        st.markdown(f"**🔬 Use in hydrogen production:** {domain_note}")


# ── Main page function ───────────────────────────────────────────────────────
def show_ml_analysis(df: pd.DataFrame):
    st.header("🔎 ML Analysis Dashboard")

    st.markdown("""
    This page provides an overview of **ML algorithms, optimization methods, and interpretability techniques**
    used across the papers.  
    Charts below show the overall distribution. You can then query papers using filters and explore
    technical explanations of each method.
    """)

    # ── 1. DISTRIBUTION CHARTS (full dataset, no filter) ────────────────────

    algo_exploded = (
        df["ML_Algorithms"].dropna()
        .str.replace(",", ";")
        .str.split(";")
        .explode()
        .str.strip()
        .reset_index(name="ML_Algorithms")
    )
    chart_algorithms = (
        alt.Chart(algo_exploded)
        .mark_bar()
        .encode(
            x=alt.X("ML_Algorithms", sort="-y", axis=alt.Axis(labelAngle=-45, labelLimit=200)),
            y="count()",
            color=alt.Color("ML_Algorithms", legend=alt.Legend(title="ML Algorithm")),
            tooltip=["ML_Algorithms", "count()"],
        )
        .properties(title="Frequency of ML Algorithms Across Papers", height=400)
    )
    st.altair_chart(chart_algorithms, width='stretch')

    opt_exploded = (
        df["Optimization_Method_Normalised"].dropna()
        .str.replace(",", ";")
        .str.split(";")
        .explode()
        .str.strip()
        .reset_index(name="Optimization_Method_Normalised")
    )
    chart_optimization = (
        alt.Chart(opt_exploded)
        .mark_bar()
        .encode(
            x=alt.X("Optimization_Method_Normalised", sort="-y", axis=alt.Axis(labelAngle=-45, labelLimit=200)),
            y="count()",
            color=alt.Color("Optimization_Method_Normalised", legend=alt.Legend(title="Optimization Method")),
            tooltip=["Optimization_Method_Normalised", "count()"],
        )
        .properties(title="Frequency of Optimization Methods Across Papers", height=400)
    )
    st.altair_chart(chart_optimization, width='stretch')

    interp_exploded = (
        df["Interpretability_Method_Normalised"].dropna()
        .str.replace(",", ";")
        .str.split(";")
        .explode()
        .str.strip()
        .reset_index(name="Interpretability_Method_Normalised")
    )
    chart_interpretability = (
        alt.Chart(interp_exploded)
        .mark_bar()
        .encode(
            x=alt.X("Interpretability_Method_Normalised", sort="-y", axis=alt.Axis(labelAngle=-45, labelLimit=200)),
            y="count()",
            color=alt.Color("Interpretability_Method_Normalised", legend=alt.Legend(title="Interpretability Method")),
            tooltip=["Interpretability_Method_Normalised", "count()"],
        )
        .properties(title="Frequency of Interpretability Methods Across Papers", height=400)
    )
    st.altair_chart(chart_interpretability, width='stretch')

    # ── 2. QUERY FILTERS (wrapped in a form with a Submit button) ───────────
    st.subheader("🔍 Query Papers")

    with st.form(key="query_form"):
        algo_filter = st.multiselect(
            "Filter by ML Algorithms:",
            sorted(df["ML_Algorithms"].dropna().str.split(";").explode().str.strip().unique()),
        )
        opt_filter = st.multiselect(
            "Filter by Optimization Methods:",
            sorted(df["Optimization_Method_Normalised"].dropna().str.split(";").explode().str.strip().unique()),
        )
        interp_filter = st.multiselect(
            "Filter by Interpretability Methods:",
            sorted(df["Interpretability_Method_Normalised"].dropna().str.split(";").explode().str.strip().unique()),
        )
        journal_filter = st.text_input("Search by Journal:")

        submitted = st.form_submit_button("🔎 Apply Filters", width='stretch')

    # ── 3. APPLY FILTERS (only runs after submit; defaults to full dataset) ──
    # session_state persists the filtered result between reruns triggered by
    # interactions outside the form (e.g. opening an expander).
    if submitted:
        filtered = df.copy()
        if algo_filter:
            filtered = filtered[
                filtered["ML_Algorithms"].str.contains("|".join(algo_filter), case=False, na=False)
            ]
        if opt_filter:
            filtered = filtered[
                filtered["Optimization_Method_Normalised"].str.contains("|".join(opt_filter), case=False, na=False)
            ]
        if interp_filter:
            filtered = filtered[
                filtered["Interpretability_Method_Normalised"].str.contains("|".join(interp_filter), case=False, na=False)
            ]
        if journal_filter:
            filtered = filtered[filtered["Journal"].str.contains(journal_filter, case=False, na=False)]

        st.session_state["ml_filtered"]      = filtered
        st.session_state["ml_active_algos"]  = set(
            filtered["ML_Algorithms"].dropna().str.split(";").explode().str.strip().unique()
        )
        st.session_state["ml_active_opts"]   = set(
            filtered["Optimization_Method_Normalised"].dropna().str.split(";").explode().str.strip().unique()
        )
        st.session_state["ml_active_interps"] = set(
            filtered["Interpretability_Method_Normalised"].dropna().str.split(";").explode().str.strip().unique()
        )

    # Fall back to the full dataset on first load (before any submit)
    filtered       = st.session_state.get("ml_filtered", df)
    active_algos   = st.session_state.get(
        "ml_active_algos",
        set(df["ML_Algorithms"].dropna().str.split(";").explode().str.strip().unique()),
    )
    active_opts    = st.session_state.get(
        "ml_active_opts",
        set(df["Optimization_Method_Normalised"].dropna().str.split(";").explode().str.strip().unique()),
    )
    active_interps = st.session_state.get(
        "ml_active_interps",
        set(df["Interpretability_Method_Normalised"].dropna().str.split(";").explode().str.strip().unique()),
    )

    # ── 4. RESULTS TABLE ────────────────────────────────────────────────────
    st.subheader("📚 Filtered Papers")
    st.caption(f"Showing **{len(filtered)}** of **{len(df)}** papers.")
    st.dataframe(
        filtered[[
            "Serial", "Title", "Author", "Year", "Journal",
            "ML_Algorithms", "Optimization_Method_Normalised", "Interpretability_Method_Normalised",
            "Hydrogen_Route", "Feedstock", "Best_R2", "Key_Performance_Metric", "Strengths",
        ]],
        width='stretch',
    )

    # ── 5. TECHNICAL EXPLANATIONS (from database/ml_methods_dictionary.py) ──
    st.subheader("📘 Technical Explanations")
    st.caption(
        "Expand any method below to read a detailed technical explanation, strengths, limitations, "
        "and domain-specific context drawn from the reviewed papers. "
        "Methods marked ⭐ appear in the current filtered view."
    )

    tab_algo, tab_opt, tab_interp = st.tabs([
        "🤖 ML Algorithms",
        "⚙️ Optimization Methods",
        "🔍 Interpretability Methods",
    ])

    with tab_algo:
        st.markdown(
            "Detailed explanations for every ML algorithm found in the dataset. "
            "Methods highlighted with ⭐ appear in the **current filtered view**."
        )
        algo_dict = ML_METHODS_DICTIONARY["ML_Algorithms"]
        sorted_algos = sorted(algo_dict.keys(), key=lambda k: (k not in active_algos, k))
        for method_key in sorted_algos:
            info = algo_dict[method_key]
            label = f"⭐ {method_key}" if method_key in active_algos else method_key
            full_name = info.get("full_name", method_key)
            with st.expander(f"ℹ️ {label}  —  *{full_name}*"):
                _render_entry(info, "ML_Algorithms")

    with tab_opt:
        st.markdown(
            "Detailed explanations for every optimisation method found in the dataset. "
            "Methods highlighted with ⭐ appear in the **current filtered view**."
        )
        opt_dict = ML_METHODS_DICTIONARY["Optimization_Methods"]
        sorted_opts = sorted(opt_dict.keys(), key=lambda k: (k not in active_opts, k))
        for method_key in sorted_opts:
            info = opt_dict[method_key]
            label = f"⭐ {method_key}" if method_key in active_opts else method_key
            full_name = info.get("full_name", method_key)
            with st.expander(f"ℹ️ {label}  —  *{full_name}*"):
                _render_entry(info, "Optimization_Methods")

    with tab_interp:
        st.markdown(
            "Detailed explanations for every interpretability method found in the dataset. "
            "Methods highlighted with ⭐ appear in the **current filtered view**."
        )
        interp_dict = ML_METHODS_DICTIONARY["Interpretability_Methods"]
        sorted_interps = sorted(interp_dict.keys(), key=lambda k: (k not in active_interps, k))
        for method_key in sorted_interps:
            info = interp_dict[method_key]
            label = f"⭐ {method_key}" if method_key in active_interps else method_key
            full_name = info.get("full_name", method_key)
            with st.expander(f"ℹ️ {label}  —  *{full_name}*"):
                _render_entry(info, "Interpretability_Methods")


# ── Entry point ──────────────────────────────────────────────────────────────
show_ml_analysis(df)
