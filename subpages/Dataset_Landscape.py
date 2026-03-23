# Dataset_Landscape.py

import streamlit as st
import pandas as pd

def show_dataset_landscape(df: pd.DataFrame):
    st.header("📊 Dataset Landscape")

    st.markdown("""
    This section explores the **datasets** used across papers in the hydrogen ML research collection.  
    Instead of charts, we present a table of journals and their dataset sizes (if reported).
    """)

    # --- Prepare table ---
    table_df = df[['Serial', 'Title', 'Author', 'Country_Region', 'Journal', 'Dataset_Size_Numeric', 'Drive_Link']].copy()
    table_df = table_df.dropna(subset=['Dataset_Size_Numeric'])
    table_df = table_df.sort_values(by='Dataset_Size_Numeric', ascending=False)
    table_df = table_df.rename(columns={
        'Dataset_Size_Numeric': 'Dataset Size',
        'Drive_Link':           'Paper / Dataset',
    })

    st.dataframe(
        table_df,
        width='stretch',
        column_config={
            'Dataset Size': st.column_config.NumberColumn(
                format='%d samples',
                help='Number of datapoints reported in the paper',
            ),
            'Paper / Dataset': st.column_config.LinkColumn(
                display_text='🔗 Open',
                help='Opens the paper and its dataset in Google Drive',
            ),
        },
        hide_index=True,
    )

    st.caption("""
    **Interpretation:**  
    - Dataset sizes vary widely across journals, from very small experimental datasets to very large sensor datasets.  
    - Most journals do not report dataset sizes at all, which limits comparability.  
    """)