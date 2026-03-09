import streamlit as st
import pandas as pd
import altair as alt

def show_hydrogen_processes(df: pd.DataFrame):
    st.header("⚗️ Hydrogen Processes")

    st.markdown("""
    This section explores the **hydrogen production pathways** represented in the dataset.  
    Each paper is categorized into one of 8 canonical routes:

    1. SCWG  
    2. Gasification  
    3. Fermentation (Dark / Anaerobic / Photo)  
    4. Biological (Biophotolysis + Fermentation)  
    5. Biogas Reforming (SR + DR)  
    6. Multiple  
    7. Biofuel (HTL; pyrolysis)  
    8. Other/Hybrid  
    """)

    # --- Load clean mapped data ---
    mapped = pd.read_csv("database/hydrogen_processes_clean_mapped.csv")
    codes = pd.read_csv("database/hydrogen_processes_category_code.csv")

    # Build dictionary {Code → Category}
    code_dict = dict(zip(codes["Code"], codes["Category"]))
    mapped["Category"] = mapped["Code"].map(code_dict)

    # --- Summary Counts ---
    counts = mapped.groupby("Category").size().reset_index(name="Count")
    st.subheader("📊 Category Distribution")
    st.dataframe(counts, width='stretch')

    chart = alt.Chart(counts).mark_bar().encode(
        x=alt.X("Category", sort='-y', axis=alt.Axis(labelAngle=-45, labelLimit=200)),
        y="Count",
        color=alt.Color("Category", legend=None),
        tooltip=["Category", "Count"]
    ).properties(title="Number of Papers per Hydrogen Route", height=400)

    st.altair_chart(chart, width='stretch')

    # --- Smart Search + Filter ---
    search_query = st.text_input("🔍 Search papers (by title, author, or journal):").lower()
    category_filter = st.selectbox(
        "Filter by Hydrogen Route:",
        ["All"] + sorted(mapped["Category"].dropna().unique().tolist())
    )

    if st.button("Apply Filters"):
        filtered = df.copy()

        # Apply search query
        if search_query:
            filtered = filtered[
                filtered["Title"].str.lower().str.contains(search_query) |
                filtered["Author"].str.lower().str.contains(search_query) |
                filtered["Journal"].str.lower().str.contains(search_query)
            ]

        # Apply category filter
        if category_filter != "All":
            filtered_serials = mapped[mapped["Category"] == category_filter]["Serial"]
            filtered = filtered[df["Serial"].isin(filtered_serials)]
    else:
        filtered = df

    # --- Tabular Display ---
    st.subheader("📚 Papers by Hydrogen Route")
    st.dataframe(filtered[[
        "Serial","Title","Author","Year","Journal","Country_Region","Type",
        "Hydrogen_Route","Feedstock","Dataset_Type","Dataset_Size_Numeric",
        "ML_Algorithms","Best_R2","Key_Performance_Metric","Research_Gap_Category"
    ]], width='stretch')

    # --- Educational Expanders ---
    with st.expander("🔥 Gasification"):
        st.write("Gasification converts carbon-rich feedstocks into syngas (H₂, CO, CH₄, CO₂)...")
        st.dataframe(df[df["Hydrogen_Route"] == "Gasification"][
            ["Serial","Title","Year","Journal","Dataset_Type","Best_R2"]
        ])

    with st.expander("💧 Supercritical Water Gasification (SCWG)"):
        st.write("SCWG operates above 374 °C and 22.1 MPa, converting wet biomass into hydrogen-rich syngas...")
        st.dataframe(df[df["Hydrogen_Route"] == "SCWG"][
            ["Serial","Title","Year","Journal","Dataset_Type","Best_R2"]
        ])

    with st.expander("🌱 Fermentation"):
        st.write("Fermentation uses anaerobic microbes to convert carbohydrate-rich wastewaters into hydrogen...")
        st.dataframe(df[df["Hydrogen_Route"] == "Fermentation"][
            ["Serial","Title","Year","Journal","Dataset_Type","Best_R2"]
        ])

    with st.expander("🌿 Biological (Biophotolysis + Fermentation)"):
        st.write("Microalgae can produce hydrogen via biophotolysis under light/dark cycles...")
        st.dataframe(df[df["Hydrogen_Route"] == "Biological (Biophotolysis + Fermentation)"][
            ["Serial","Title","Year","Journal","Dataset_Type","Best_R2"]
        ])

    with st.expander("🔥 Biogas Reforming"):
        st.write("Biogas reforming combines steam and dry reforming of CH₄ + CO₂ mixtures...")
        st.dataframe(df[df["Hydrogen_Route"] == "Biogas Reforming (SR + DR)"][
            ["Serial","Title","Year","Journal","Dataset_Type","Best_R2"]
        ])

    with st.expander("📚 Multiple"):
        st.write("Reviews or multi-process studies that cover several hydrogen production pathways...")
        st.dataframe(df[df["Hydrogen_Route"] == "Multiple"][
            ["Serial","Title","Year","Journal","Dataset_Type","Best_R2"]
        ])

    with st.expander("🧪 Biofuel (HTL; pyrolysis)"):
        st.write("Hydrothermal liquefaction and pyrolysis of algae/biomass for hydrogen-rich biofuels...")
        st.dataframe(df[df["Hydrogen_Route"] == "Biofuel (HTL; pyrolysis)"][
            ["Serial","Title","Year","Journal","Dataset_Type","Best_R2"]
        ])

    with st.expander("⚡ Other/Hybrid"):
        st.write("Hybrid systems that combine multiple processes (e.g., gasification + electrolysis + methanation)...")
        st.dataframe(df[df["Hydrogen_Route"] == "Other/Hybrid"][
            ["Serial","Title","Year","Journal","Dataset_Type","Best_R2"]
        ])