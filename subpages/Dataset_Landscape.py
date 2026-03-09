import streamlit as st
import pandas as pd

def show_dataset_landscape(df: pd.DataFrame):
    st.header("📊 Dataset Landscape")

    st.markdown("""
    This section explores the **datasets** used across papers in the hydrogen ML research collection.  
    Instead of charts, we present a table of journals and their dataset sizes (if reported).
    """)

    # --- Prepare table ---
    table_df = df[['Journal', 'Dataset_Size_Numeric']].copy()
    table_df = table_df.dropna(subset=['Dataset_Size_Numeric'])
    table_df = table_df.sort_values(by='Dataset_Size_Numeric', ascending=False)

    st.dataframe(table_df, width='stretch')

    st.caption("""
    **Interpretation:**  
    - Dataset sizes vary widely across journals, from very small experimental datasets to very large sensor datasets.  
    - Most journals do not report dataset sizes at all, which limits comparability.  
    """)