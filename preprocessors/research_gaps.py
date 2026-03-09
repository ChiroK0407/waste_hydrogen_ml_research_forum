import pandas as pd

# Load data
papers = pd.read_csv("papers_cleaned.csv")
codes = pd.read_csv("database/researchgaps_category_code.csv")

# --- Preprocessing ---
gap_exploded = papers[["Serial","Research_Gap_Normalised"]].dropna()
gap_exploded = gap_exploded.assign(
    Research_Gap_Normalised=gap_exploded["Research_Gap_Normalised"].str.split(";")
).explode("Research_Gap_Normalised")

gap_exploded["Research_Gap_Normalised"] = gap_exploded["Research_Gap_Normalised"].str.strip()

# Deduplicate per paper + category
gap_exploded = gap_exploded.drop_duplicates(subset=["Serial","Research_Gap_Normalised"])

# --- Normalization dictionary (collapse variants to your 16 categories) ---
normalization_map = {
    "dynamic modelling": "Dynamic Modelling",
    "uncertainty": "Uncertainty",
    "hybrid ML": "Hybrid ML",
    "expanded parameters": "Expanded parameters",
    "comparative optimizers": "Comparative optimizers",
    "industrial integration": "Industrial integration"
}

gap_exploded["Research_Gap_Normalised"] = gap_exploded["Research_Gap_Normalised"].replace(normalization_map)

# --- Merge with manual codes ---
merged = gap_exploded.merge(
    codes, left_on="Research_Gap_Normalised", right_on="Category", how="left"
)

# --- Diagnostics ---
print("=== Diagnostics: Research Gap Categories ===")
print(f"Total unique categories in dataset (after normalization): {merged['Research_Gap_Normalised'].nunique()}")
print(f"Total categories in mapping file: {codes['Category'].nunique()}\n")

print("Categories without codes (check mapping file):")
print(merged[merged["Code"].isna()]["Research_Gap_Normalised"].unique())

print("\nCounts per category (with codes):")
print(merged.groupby(["Research_Gap_Normalised","Code"]).size())

# --- Save clean CSV ---
clean_csv = merged[["Serial","Research_Gap_Normalised","Code"]]
clean_csv.to_csv("database/researchgaps_clean_mapped.csv", index=False)

print("\n✅ Clean CSV saved to database/researchgaps_clean_mapped.csv")