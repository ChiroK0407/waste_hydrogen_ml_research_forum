import streamlit as st
import pandas as pd
import altair as alt

# ── Load data ─────────────────────────────────────────────────────────────────
df = pd.read_csv("database/papers_cleaned.csv")

st.header("📊 Overview Dashboard")

st.markdown("""
This page provides a high-level overview of the research landscape on
**machine learning for hydrogen production from wastes** — summarising the
types of datasets used and the ML algorithm families applied across all
29 reviewed papers. Use the sidebar to navigate to the detailed pages.
""")

st.markdown("---")

# ── Dataset Type Distribution ─────────────────────────────────────────────────
st.subheader("Dataset Type Distribution")

palette_ds = ["#2E86AB", "#F4A261", "#2A9D8F", "#E76F51",
              "#457B9D", "#E9C46A", "#264653"]

dt_counts = (
    df["Dataset_Type"].dropna().str.strip()
    .value_counts().reset_index()
)
dt_counts.columns = ["Dataset_Type", "Count"]
domain_dt = dt_counts["Dataset_Type"].tolist()
colours_dt = (palette_ds * 3)[: len(domain_dt)]

chart1 = (
    alt.Chart(dt_counts)
    .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
    .encode(
        x=alt.X("Dataset_Type:N", sort="-y",
                axis=alt.Axis(labelAngle=-30, title="Dataset Type")),
        y=alt.Y("Count:Q", axis=alt.Axis(title="Number of Papers")),
        color=alt.Color("Dataset_Type:N",
                        scale=alt.Scale(domain=domain_dt, range=colours_dt),
                        legend=None),
        tooltip=[
            alt.Tooltip("Dataset_Type:N", title="Type"),
            alt.Tooltip("Count:Q",        title="Papers"),
        ],
    )
    .properties(height=360)
)

st.altair_chart(chart1, width='stretch')

st.caption(
    "**Experimental** — lab or pilot-scale measurements · "
    "**Simulation** — process model outputs (Aspen Plus, CFD, PRO/II) · "
    "**Literature** — curated datasets compiled from published studies · "
    "**Review** — no original dataset, purely synthesis · "
    "**Hybrid** — experimental + literature combined · "
    "**Sensor** — IoT / real-time sensor datapoints · "
    "**CFD** — computational fluid dynamics simulations"
)

st.markdown("---")

# ── ML Family Frequency ───────────────────────────────────────────────────────
st.subheader("ML Algorithm Family Frequency")

palette_ml = ["#2E86AB", "#A23B72", "#F18F01", "#C73E1D",
              "#44BBA4", "#E94F37", "#393E41", "#F5A623"]

ml_exploded = (
    df["ML_Family"].dropna()
    .str.replace(",", ";")
    .str.split(";")
    .explode()
    .str.strip()
    .reset_index(name="ML_Family")
)
domain_ml = sorted(ml_exploded["ML_Family"].unique().tolist())
colours_ml = (palette_ml * 3)[: len(domain_ml)]

chart2 = (
    alt.Chart(ml_exploded)
    .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
    .encode(
        x=alt.X("ML_Family:N", sort="-y",
                axis=alt.Axis(labelAngle=-40, labelLimit=200, title="ML Family")),
        y=alt.Y("count():Q", axis=alt.Axis(title="Number of Papers")),
        color=alt.Color("ML_Family:N",
                        scale=alt.Scale(domain=domain_ml, range=colours_ml),
                        legend=alt.Legend(title="ML Family")),
        tooltip=[
            alt.Tooltip("ML_Family:N", title="ML Family"),
            alt.Tooltip("count():Q",   title="Papers"),
        ],
    )
    .properties(height=420)
)

st.altair_chart(chart2, width='stretch')

st.caption(
    "Totals exceed 29 papers because many studies use multiple algorithm families. "
    "**Boosting Ensemble** (XGBoost, GBR, AdaBoost, LightGBM) and "
    "**Tree-Based Ensemble** (Random Forest) are the most frequently applied families, "
    "followed by **Neural Networks** (ANN, CNN, LSTM) and **Kernel-Based** (SVM, GPR) methods."
)

st.markdown("---")

# ── Page guide ────────────────────────────────────────────────────────────────
st.subheader("🗺️ Dashboard Pages")

c1, c2, c3, c4, c5 = st.columns(5)

c1.markdown("**⚗️ Process Analysis**\n\nHydrogen routes, feedstocks, country distribution and process explainers.")
c2.markdown("**🤖 ML Analysis**\n\nAlgorithm, optimisation and interpretability method frequency and explainers.")
c3.markdown("**📚 Paper Explorer**\n\nSearch and read full technical summaries for all 29 papers.")
c4.markdown("**🧪 Dataset Viewer**\n\nBrowse simulation-ready datasets extracted from the reviewed papers.")
c5.markdown("**📊 This page**\n\nDataset type and ML family overview across the full collection.")