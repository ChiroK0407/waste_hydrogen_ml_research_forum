import pandas as pd

def map_strengths():
    # --- Load papers with encoding fallback ---
    try:
        papers = pd.read_csv("papers_cleaned.csv", encoding="utf-8-sig")
    except UnicodeDecodeError:
        papers = pd.read_csv("papers_cleaned.csv", encoding="latin1")

    # --- Split strengths into individual items ---
    strengths_split = papers.assign(
        Strengths=papers['Strengths'].str.split(';')
    ).explode('Strengths')
    strengths_split['Strengths'] = strengths_split['Strengths'].str.strip()

    # --- Mapping rules (keywords → codes) ---
    mapping_rules = {
        'Novel': 'S1', 'First': 'S1', 'Introduced': 'S1',
        'Rigorous': 'S2', 'Validated': 'S2',
        'Comprehensive': 'S3', 'Detailed': 'S3',
        'SHAP': 'S4', 'PDP': 'S4', 'Interpretability': 'S4',
        'Pilot': 'S5', 'Industrial': 'S5', 'Practical': 'S5',
        'Public': 'S6', 'GitHub': 'S6',
        'Optimization': 'S7', 'GA': 'S7', 'PSO': 'S7', 'NSGA': 'S7', 'Efficiency': 'S7',
        'Emissions': 'S8', 'Circular': 'S8', 'LCA': 'S8', 'Policy': 'S8'
    }

    def assign_code(strength):
        if pd.isna(strength) or not strength.strip():
            return "S0"  # special category for unmapped/other
        for keyword, code in mapping_rules.items():
            if keyword.lower() in strength.lower():
                return code
        return "S0"  # fallback if no match

    strengths_split['Code'] = strengths_split['Strengths'].apply(assign_code)

    # --- Keep only essential columns ---
    final = strengths_split[['Serial', 'Journal', 'Author', 'Code']]

    # --- Save clean mapped file ---
    final.to_csv("database/strengths_clean_mapped.csv", index=False)
    print("✅ strengths_clean_mapped.csv created (codes only)")

if __name__ == "__main__":
    map_strengths()