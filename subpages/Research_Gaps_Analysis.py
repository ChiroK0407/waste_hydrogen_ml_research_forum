import streamlit as st
import pandas as pd
import altair as alt

# --- Load Data ---
mapped = pd.read_csv("database/researchgaps_clean_mapped.csv")
codes = pd.read_csv("database/researchgaps_category_code.csv")

st.header("Research Gaps Analysis")

st.markdown("""
This page visualizes the **research gaps** identified across papers.  
Since many papers list multiple gaps, totals exceed the number of papers.
""")

# --- Merge for labels ---
merged = mapped.merge(codes, on="Code", how="left")

# --- Aggregate counts ---
gap_counts = merged.groupby(["Code","Category"]).size().reset_index(name="count")

# --- Chart ---

chart = alt.Chart(gap_counts).mark_bar().encode(
    x=alt.X('Category', sort='-y', axis=alt.Axis(labelAngle=-45, labelLimit=200)),
    y='count',
    color=alt.Color('Category', legend=alt.Legend(title="Research Gap Category")),
    tooltip=['Code','Category','count']
).properties(title="Frequency of Research Gaps Across Papers", height=450)

st.altair_chart(chart, width='stretch')

st.caption("""
**Interpretation:**  
This chart shows how often each research gap is mentioned across papers.  
Totals exceed the number of papers since many papers identify multiple gaps.
""")
st.subheader("What Do These Categories Refer To?")

with st.expander("1️⃣ TEA (Techno-Economic Analysis)"):
    st.write("Evaluates cost, efficiency, and feasibility of hydrogen production pathways alongside ML modeling.")

with st.expander("2️⃣ Larger datasets"):
    st.write("Calls for bigger, more diverse datasets to improve model robustness and generalization.")

with st.expander("3️⃣ Policy frameworks"):
    st.write("Focuses on system-level adoption, industrial integration, and regulatory or circular economy considerations.")

with st.expander("4️⃣ Standardized datasets"):
    st.write("Highlights the need for consistent reporting formats and standardized data structures across studies.")

with st.expander("5️⃣ Expanded parameters"):
    st.write("Refers to broadening the scope of optimization or modeling variables beyond the usual set.")

with st.expander("6️⃣ Expanded feedstocks/catalysts"):
    st.write("Encourages exploration of new feedstocks, catalysts, or co-gasification blends for hydrogen production.")

with st.expander("7️⃣ Experimental validation"):
    st.write("Indicates the need for lab-scale or field-scale experiments to validate ML predictions and simulations.")

with st.expander("8️⃣ Pilot-scale validation"):
    st.write("Specifically refers to scaling up to pilot plants, distinct from small-scale experimental validation.")

with st.expander("9️⃣ Hybrid ML"):
    st.write("Combines multiple ML approaches or integrates ML with physics-based models (e.g., PINNs).")

with st.expander("🔟 Dynamic Modelling"):
    st.write("Focuses on time-dependent or process-dynamic simulations, beyond static datasets.")

with st.expander("1️⃣1️⃣ Optimization integration"):
    st.write("Use of advanced optimizers (GA, PSO, NSGA-II, Bayesian tuning) to improve ML models or process design.")

with st.expander("1️⃣2️⃣ LCA (Life Cycle Assessment)"):
    st.write("Evaluates environmental impacts of hydrogen production pathways across their full lifecycle.")

with st.expander("1️⃣3️⃣ Carbon Capture & Storage (CCS)"):
    st.write("Integration of CCS technologies into hydrogen production, including cost-effective storage solutions.")

with st.expander("1️⃣4️⃣ Uncertainty"):
    st.write("Explicit quantification of uncertainty in ML predictions and process outcomes.")

with st.expander("1️⃣5️⃣ Industrial integration"):
    st.write("Addresses deployment into industrial systems, sector coupling, and large-scale adoption challenges.")

with st.expander("1️⃣6️⃣ Comparative optimizers"):
    st.write("Refers to benchmarking and comparing different optimization algorithms for performance and reliability.")