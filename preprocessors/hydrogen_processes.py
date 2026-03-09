import pandas as pd

def map_hydrogen_processes():
    # --- Load papers with encoding fallback ---
    try:
        papers = pd.read_csv("papers_cleaned.csv", encoding="utf-8-sig")
    except UnicodeDecodeError:
        papers = pd.read_csv("papers_cleaned.csv", encoding="latin1")

    # Load category codes
    codes = pd.read_csv("database/hydrogen_processes_category_code.csv")

    # --- Mapping rules (keywords → codes) ---
    mapping_rules = {
        "SCWG": "1",
        "Gasification": "2",
        "Fermentation": "3",
        "Biological (Biophotolysis + Fermentation)": "4",
        "Biogas Reforming": "5",
        "Multiple": "6",
        "Biofuel": "7",
        "Other": "8",
        "Hybrid": "8"
    }

    def assign_code(route):
        if pd.isna(route) or not route.strip():
            return "0"  # special category for unmapped/other
        for keyword, code in mapping_rules.items():
            if keyword.lower() in route.lower():
                return code
        return "0"

    papers["Code"] = papers["Hydrogen_Route"].apply(assign_code)

    # --- Keep only essential columns ---
    final = papers[["Serial", "Hydrogen_Route", "Code"]]

    # --- Save clean mapped file ---
    final.to_csv("database/hydrogen_processes_clean_mapped.csv", index=False)
    print("✅ hydrogen_processes_clean_mapped.csv created (codes only)")

if __name__ == "__main__":
    map_hydrogen_processes()