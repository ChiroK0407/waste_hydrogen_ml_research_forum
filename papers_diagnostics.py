import pandas as pd
import numpy as np
import re

# ==============================
# 1. LOAD DATA
# ==============================

df = pd.read_csv("papers.csv", encoding="utf-8")

print("\nInitial shape:", df.shape)
print("\nOriginal Columns:", df.columns.tolist())


# ==============================
# 2. CLEAN COLUMN NAMES
# ==============================

# Fix encoding artifact if present
df.rename(columns={"Best RÂ²": "Best_R2"}, inplace=True)

df.columns = df.columns.str.strip()
df.columns = df.columns.str.replace(" ", "_")
df.columns = df.columns.str.replace("/", "_")

print("\nCleaned Columns:", df.columns.tolist())


# ==============================
# 3. UNIFORM TEXT CLEANING
# ==============================

def clean_text(x):
    if pd.isna(x):
        return np.nan
    x = str(x).strip()
    x = re.sub(r"\s+", " ", x)
    return x

for col in df.columns:
    if df[col].dtype == "object":
        df[col] = df[col].apply(clean_text)


# ==============================
# 4. STANDARDIZE YES/NO FIELDS
# ==============================

yes_no_cols = [
    "TEA",
    "LCA",
    "Carbon_Capture",
    "Dynamic_Modelling",
    "Uncertainty_Quantification"
]

def normalize_yes_no(x):
    if pd.isna(x):
        return np.nan
    x = str(x).lower()
    if x in ["yes", "y", "included", "true"]:
        return "Yes"
    elif x in ["no", "n", "not included", "false"]:
        return "No"
    else:
        return x

for col in yes_no_cols:
    if col in df.columns:
        df[col] = df[col].apply(normalize_yes_no)


# ==============================
# 5. CLEAN SEMICOLON FIELDS
# ==============================

def clean_semicolon_field(x):
    if pd.isna(x):
        return np.nan
    items = [i.strip().title() for i in x.split(";")]
    items = sorted(set(items))
    return "; ".join(items)

semicolon_cols = [
    "ML_Algorithms",
    "Optimization_Method",
    "Interpretability_Method"
]

for col in semicolon_cols:
    if col in df.columns:
        df[col] = df[col].apply(clean_semicolon_field)


# ==============================
# 6. NORMALIZE ML ALGORITHM NAMES
# ==============================

ml_mapping = {
    # Random Forest
    "Rf": "Random Forest",
    "Rfr": "Random Forest",
    "Random Forest": "Random Forest",
    "Rf + Ga": "Random Forest",

    # XGBoost
    "Xgb": "XGBoost",
    "Xgboost": "XGBoost",

    # ANN family
    "Ann": "ANN",
    "Bpann": "ANN",
    "Mlp": "ANN",
    "Fnn": "ANN",

    # Decision Tree
    "Dt": "Decision Tree",

    # Gradient Boosting
    "Gb": "Gradient Boosting",
    "Gbr": "Gradient Boosting",

    # SVM
    "Svr": "SVM",
    "Svm": "SVM",

    # Linear Regression
    "Lr": "Linear Regression",
    "Mlr": "Linear Regression",

    # Deep Learning
    "Dl": "Deep Learning",

    # Gaussian Process
    "Gpr": "Gaussian Process",
    "Gp": "Gaussian Process",
}

def normalize_ml_field(x):
    if pd.isna(x):
        return np.nan
    
    items = [i.strip() for i in x.split(";")]
    normalized = []
    
    for item in items:
        item_clean = item.title()
        normalized.append(ml_mapping.get(item_clean, item_clean))
    
    normalized = sorted(set(normalized))
    
    return "; ".join(normalized)

if "ML_Algorithms" in df.columns:
    df["ML_Algorithms"] = df["ML_Algorithms"].apply(normalize_ml_field)


# ==============================
# 7. CREATE ML FAMILY COLUMN
# ==============================

ml_family_map = {
    "Random Forest": "Tree-Based Ensemble",
    "XGBoost": "Boosting Ensemble",
    "Gradient Boosting": "Boosting Ensemble",
    "Decision Tree": "Tree-Based",
    "ANN": "Neural Network",
    "Deep Learning": "Neural Network",
    "LSTM": "Neural Network",
    "CNN": "Neural Network",
    "SVM": "Kernel-Based",
    "Gaussian Process": "Kernel-Based",
    "Linear Regression": "Linear Model",
    "KNN": "Instance-Based",
    "Catboost": "Boosting Ensemble",
    "Lightgbm": "Boosting Ensemble",
    "Adaboost": "Boosting Ensemble",
}

ml_family_map.update({
    "Elm": "Neural Network",
    "Kernel Ridge": "Kernel-Based",
    "Bayesian Regression": "Linear Model",
    "Extra Trees": "Tree-Based Ensemble",
    "Rl": "Reinforcement Learning",
    "Ensemble Boosting": "Boosting Ensemble",
    "Bagxgboost": "Boosting Ensemble",
    "Lightgbm": "Boosting Ensemble",
    "Catboost": "Boosting Ensemble"
})

def assign_ml_family(x):
    if pd.isna(x):
        return np.nan
    
    items = x.split("; ")
    families = []
    
    for item in items:
        families.append(ml_family_map.get(item, "Other"))
    
    return "; ".join(sorted(set(families)))

df["ML_Family"] = df["ML_Algorithms"].apply(assign_ml_family)


# ==============================
# 8. ENSURE NUMERIC COLUMNS
# ==============================

if "Dataset_Size_Numeric" in df.columns:
    df["Dataset_Size_Numeric"] = pd.to_numeric(
        df["Dataset_Size_Numeric"], errors="coerce"
    )

if "Best_R2" in df.columns:
    df["Best_R2"] = (
        df["Best_R2"]
        .astype(str)
        .str.extract(r"(\d*\.?\d+)")
    )
    df["Best_R2"] = pd.to_numeric(df["Best_R2"], errors="coerce")


# ==============================
# 9. DERIVED FEATURES
# ==============================

def count_models(x):
    if pd.isna(x):
        return 0
    return len(x.split(";"))

df["Num_ML_Models"] = df["ML_Algorithms"].apply(count_models)


# ==============================
# 10. DIAGNOSTICS
# ==============================

print("\n===== FINAL DIAGNOSTICS =====")

print("\nColumn Data Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isna().sum())

print("\nDataset Size Statistics:")
print(df["Dataset_Size_Numeric"].describe())

print("\nML Method Distribution:")
ml_exploded = df["ML_Algorithms"].str.split("; ").explode()
print(ml_exploded.value_counts())

print("\nML Family Distribution:")
family_exploded = df["ML_Family"].str.split("; ").explode()
print(family_exploded.value_counts())

print("\nBest R2 Statistics:")
print(df["Best_R2"].describe())


# ==============================
# 11. SAVE CLEAN DATASET
# ==============================

df.to_csv("papers_cleaned.csv", index=False)

print("\nCleaned dataset saved as 'papers_cleaned.csv'")