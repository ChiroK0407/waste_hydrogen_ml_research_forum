import streamlit as st
import pandas as pd
import altair as alt

def show_strengths_and_gaps():
    st.header("💡 Strengths & Research Gaps Analysis")

    # --- Load clean mapped data (codes only) ---
    strengths = pd.read_csv("database/strengths_clean_mapped.csv")
    gaps = pd.read_csv("database/researchgaps_clean_mapped.csv")

    # --- Load category code files ---
    strengths_codes = pd.read_csv("database/strengths_category_code.csv")
    gaps_codes = pd.read_csv("database/researchgaps_category_code.csv")

    # --- Build dictionaries {Code → Category} ---
    strengths_dict = dict(zip(strengths_codes["Code"], strengths_codes["Category"]))
    gaps_dict = dict(zip(gaps_codes["Code"], gaps_codes["Category"]))

    # --- Attach category labels at runtime ---
    strengths["Category"] = strengths["Code"].map(strengths_dict)
    gaps["Category"] = gaps["Code"].map(gaps_dict)

    # --- Strengths Chart ---
    strength_counts = strengths.groupby(["Code","Category"]).size().reset_index(name="count")

    chart_strengths = alt.Chart(strength_counts).mark_bar().encode(
        x=alt.X('Category', sort='-y', axis=alt.Axis(labelAngle=-45, labelLimit=200)),
        y='count',
        color=alt.Color('Category', legend=alt.Legend(title="Strength Category")),
        tooltip=['Code','Category','count']
    ).properties(title="Frequency of Strengths Across Papers", height=450)

    st.altair_chart(chart_strengths, width='stretch')
    st.caption("This chart shows how often each strength category is mentioned across papers.")

    # --- Research Gaps Chart ---
    gap_counts = gaps.groupby(["Code","Category"]).size().reset_index(name="count")

    chart_gaps = alt.Chart(gap_counts).mark_bar().encode(
        x=alt.X('Category', sort='-y', axis=alt.Axis(labelAngle=-45, labelLimit=200)),
        y='count',
        color=alt.Color('Category', legend=alt.Legend(title="Research Gap Category")),
        tooltip=['Code','Category','count']
    ).properties(title="Frequency of Research Gaps Across Papers", height=450)

    st.altair_chart(chart_gaps, width='stretch')
    st.caption("This chart shows how often each research gap category is mentioned across papers.")