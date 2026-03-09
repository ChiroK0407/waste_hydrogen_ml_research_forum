import streamlit as st
import altair as alt
import pandas as pd

def show_ml_methods(df: pd.DataFrame):
    st.header("🤖 ML Methods Analysis")

    st.markdown("""
    This section explores the **ML algorithms**, **optimization techniques**, and **interpretability methods** used across the papers.  
    Since many papers employ multiple methods, totals exceed the number of papers.  
    These charts provide a clear overview of methodological trends in hydrogen ML research.
    """)

    # --- ML Algorithms ---
    algo_exploded = df["ML_Algorithms"].dropna().str.replace(",", ";").str.split(";").explode().reset_index()
    algo_exploded["ML_Algorithms"] = algo_exploded["ML_Algorithms"].str.strip().str.title()

    chart_algorithms = alt.Chart(algo_exploded).mark_bar().encode(
        x=alt.X('ML_Algorithms', sort='-y', axis=alt.Axis(labelAngle=-45, labelLimit=200)),
        y='count()',
        color=alt.Color('ML_Algorithms', legend=alt.Legend(title="ML Algorithm")),
        tooltip=['ML_Algorithms']
    ).properties(title="Frequency of ML Algorithms Across Papers", height=400)

    st.altair_chart(chart_algorithms, width='stretch')
    st.caption("""
    **Interpretation:**  
    Algorithms include ANN, CNN, Random Forest, XGBoost, SVM, and others.  
    Many papers use multiple algorithms, so totals exceed the number of papers.
    """)

    # --- Optimization Methods ---
    opt_exploded = df["Optimization_Method_Normalised"].dropna().str.replace(",", ";").str.split(";").explode().reset_index()
    opt_exploded["Optimization_Method_Normalised"] = opt_exploded["Optimization_Method_Normalised"].str.strip().str.title()

    chart_optimization = alt.Chart(opt_exploded).mark_bar().encode(
        x=alt.X('Optimization_Method_Normalised', sort='-y', axis=alt.Axis(labelAngle=-45, labelLimit=200)),
        y='count()',
        color=alt.Color('Optimization_Method_Normalised', legend=alt.Legend(title="Optimization Method")),
        tooltip=['Optimization_Method_Normalised']
    ).properties(title="Frequency of Optimization Methods Across Papers", height=400)

    st.altair_chart(chart_optimization, width='stretch')
    st.caption("""
    **Interpretation:**  
    Optimization methods include Genetic Algorithms (GA), Particle Swarm Optimization (PSO), NSGA-II, Bayesian Optimization, Differential Evolution, and others.  
    These are used to fine-tune ML models or optimize process parameters.
    """)

    # --- Interpretability Methods ---
    interp_exploded = df["Interpretability_Method_Normalised"].dropna().str.replace(",", ";").str.split(";").explode().reset_index()
    interp_exploded["Interpretability_Method_Normalised"] = interp_exploded["Interpretability_Method_Normalised"].str.strip().str.title()

    chart_interpretability = alt.Chart(interp_exploded).mark_bar().encode(
        x=alt.X('Interpretability_Method_Normalised', sort='-y', axis=alt.Axis(labelAngle=-45, labelLimit=200)),
        y='count()',
        color=alt.Color('Interpretability_Method_Normalised', legend=alt.Legend(title="Interpretability Method")),
        tooltip=['Interpretability_Method_Normalised']
    ).properties(title="Frequency of Interpretability Methods Across Papers", height=400)

    st.altair_chart(chart_interpretability, width='stretch')
    st.caption("""
    **Interpretation:**  
    Interpretability methods include SHAP, PDP (Partial Dependence Plots), ICE, Sobol sensitivity analysis, surrogate trees, and statistical metrics.  
    These techniques help explain which features drive hydrogen yield predictions and improve trust in ML models.
    """)

    # --- Short Notes on ML Implementations ---
    st.subheader("Short Notes on ML Algorithms")

    with st.expander("🧠 Artificial Neural Networks (ANN)"):
        st.write("""
        ANN models mimic biological neurons and are widely used for nonlinear prediction tasks.  
        In hydrogen production, they capture complex relationships between feedstock properties and yields.
        """)

    with st.expander("🌳 Random Forest"):
        st.write("""
        Random Forest is an ensemble of decision trees.  
        It is robust to noise and provides feature importance, making it popular for syngas composition prediction.
        """)

    with st.expander("📈 Support Vector Machines (SVM)"):
        st.write("""
        SVMs are kernel-based models that find optimal hyperplanes for classification/regression.  
        They are effective for smaller datasets and high-dimensional features.
        """)

    with st.expander("⚡ XGBoost / Gradient Boosting"):
        st.write("""
        Boosting ensembles like XGBoost iteratively improve weak learners.  
        They are highly accurate and often outperform other methods in hydrogen yield prediction tasks.
        """)

    with st.expander("🔍 Gaussian Process Regression (GPR)"):
        st.write("""
        GPR is a probabilistic model that provides uncertainty estimates along with predictions.  
        Useful for small datasets and when confidence intervals are important.
        """)

    with st.expander("📊 Linear Regression"):
        st.write("""
        Linear regression is a baseline model that assumes linear relationships.  
        It is often used for benchmarking and quick interpretability.
        """)