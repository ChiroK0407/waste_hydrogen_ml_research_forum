import streamlit as st
import pandas as pd
import altair as alt

# Import subpage functions
from subpages.Hydrogen_Processes import show_hydrogen_processes
from subpages.Dataset_Landscape import show_dataset_landscape
from subpages.Strengths_and_Gaps import show_strengths_and_gaps
from subpages.ML_Methodology import show_ml_methods

# --- Load Data ---
df = pd.read_csv("database/papers_cleaned.csv")

st.header("📊 Overview Dashboard")

st.markdown("""
This page provides a high-level overview of the research landscape on **machine learning for hydrogen production from wastes**.  
It summarizes the types of datasets used and the families of ML methods applied.
""")

# --- Dataset Type Distribution ---
chart1 = alt.Chart(df).mark_bar().encode(
    x='Dataset_Type',
    y='count()',
    tooltip=['Dataset_Type']
).properties(title="Dataset Type Distribution")

st.altair_chart(chart1, width='stretch')

st.caption("""
**Interpretation:**  
- *Experimental*: Lab or pilot-scale datasets.  
- *Simulation*: Data from process models (Aspen Plus, CFD).  
- *Literature*: Curated datasets from published studies.  
- *Review*: No dataset, purely synthesis.  
- *Hybrid*: Combination of experimental + literature.  
- *Sensor*: IoT or real-time sensor datasets.  
- *CFD*: Computational fluid dynamics simulations.  
""")

# --- ML Family Frequency ---
# --- ML Family Frequency ---
ml_exploded = df["ML_Family"].str.split("; ").explode().reset_index()

chart2 = alt.Chart(ml_exploded).mark_bar().encode(
    x=alt.X('ML_Family', sort='-y', axis=alt.Axis(labelAngle=-45, labelLimit=200)),
    y='count()',
    color=alt.Color('ML_Family', legend=alt.Legend(title="ML Family")),
    tooltip=['ML_Family']
).properties(title="Frequency of ML Families Across Papers", height=450)

st.altair_chart(chart2, width='stretch')

st.caption("""
**Interpretation:**  
This chart counts each ML family used across all papers.  
Totals exceed the number of papers since many use multiple algorithms.  
Categories include Tree-Based Ensembles, Boosting Ensembles, Neural Networks, Kernel-Based methods, Linear Models, and Other specialized approaches.  
""")

# --- Navigation Buttons ---
st.markdown("### 🔎 Explore More (Part of Overview)")

if st.button("⚗️ Hydrogen Processes", width='stretch'):
    show_hydrogen_processes(df)
    if st.button("⬅️ Back to Overview", width='stretch'):
        st.experimental_rerun()

if st.button("📊 Dataset Landscape", width='stretch'):
    show_dataset_landscape(df)
    if st.button("⬅️ Back to Overview", width='stretch'):
        st.experimental_rerun()

if st.button("💡 Strengths and Gaps", width='stretch'):
    show_strengths_and_gaps()
    if st.button("⬅️ Back to Overview", width='stretch'):
        st.experimental_rerun()

if st.button("🤖 ML Methodology", width='stretch'):
    show_ml_methods(df)
    if st.button("⬅️ Back to Overview", width='stretch'):
        st.experimental_rerun()