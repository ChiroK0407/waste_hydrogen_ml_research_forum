import pandas as pd

# Load your corrected CSV
df = pd.read_csv("papers_cleaned.csv")

# --- Preprocessing ---
gap_exploded = df[["Serial","Research_Gap_Normalised"]].dropna()
gap_exploded = gap_exploded.assign(
    Research_Gap_Normalised=gap_exploded["Research_Gap_Normalised"].str.split(";")
).explode("Research_Gap_Normalised")

# Clean whitespace
gap_exploded["Research_Gap_Normalised"] = gap_exploded["Research_Gap_Normalised"].str.strip()

# Deduplicate per paper (Serial + category)
gap_exploded = gap_exploded.drop_duplicates(subset=["Serial","Research_Gap_Normalised"])

# --- Diagnostics ---
unique_categories = gap_exploded["Research_Gap_Normalised"].unique()
num_categories = len(unique_categories)

print("=== Diagnostics: Research Gap Categories ===")
print(f"Total unique categories formed: {num_categories}\n")

print("List of categories:")
for cat in sorted(unique_categories):
    print(f" - {cat}")

print("\nCounts per category:")
print(gap_exploded["Research_Gap_Normalised"].value_counts())