# waste_hydrogen_ml_research_forum
# Waste2Hydrogen ML Dashboard

> A structured analytical dashboard synthesising **29 peer-reviewed papers** (2024–2026) on machine learning applications for hydrogen production from waste feedstocks — covering thermochemical, biological, and electrochemical conversion routes.

---

## Overview

The **Waste2Hydrogen ML Dashboard** is a multi-page interactive [Streamlit](https://streamlit.io/) application built to support structured literature synthesis at the intersection of **machine learning** and **green hydrogen production from waste**. It compiles process data, ML methodologies, interpretability approaches, dataset characteristics, and identified research gaps into a single queryable interface, with each paper accompanied by a full structured technical summary.

The dashboard is intended for researchers, engineers, and postgraduate students working in the fields of hydrogen energy, waste valorisation, and applied machine learning.

---

## Features

- 📊 **Overview** — dataset composition, ML family frequency, publication trends
- ⚗️ **Process Analysis** — hydrogen route and feedstock distribution charts, country breakdown, system flags, and detailed process/feedstock explainers
- 🤖 **ML Analysis** — algorithm, optimisation method, and interpretability method frequency charts with full technical explainers for every method in the dataset
- 📚 **Paper Explorer** — full-text search, multi-filter paper browsing, and structured technical summaries with direct links to source papers

---

## Dataset at a Glance

| Metric | Value |
|---|---|
| Papers reviewed | 29 |
| Publication years | 2024 – 2026 |
| Unique journals | 14 |
| Countries / regions | 22 |
| Hydrogen production routes | 17 |
| Feedstock types | 14 |
| ML algorithms catalogued | 29 |
| Papers with R² reported | 23 |
| Mean Best R² | 0.905 |
| Highest reported R² | 0.990 |

### Study Types
| Type | Count |
|---|---|
| Original Research | 20 |
| Review | 6 |
| Simulation | 3 |

### Publication Timeline
| Year | Papers |
|---|---|
| 2024 | 3 |
| 2025 | 13 |
| 2026 | 13 |

### Top Hydrogen Production Routes
| Route | Papers |
|---|---|
| Biological (Dark Fermentation) | 6 |
| Gasification | 5 |
| SCWG (Supercritical Water Gasification) | 4 |
| Gasification (Chemical Looping) | 2 |
| Biofuel (HTL + Pyrolysis) | 1 |

### Top ML Algorithm Families
| Family | Papers |
|---|---|
| Boosting Ensemble | 21 |
| Tree-Based Ensemble | 19 |
| Neural Network | 14 |
| Kernel-Based | 14 |
| Linear Model | 8 |
| Tree-Based | 7 |
| Reinforcement Learning | 1 |

### Most Used Algorithms
`Random Forest (18)` · `ANN (15)` · `SVM (13)` · `XGBoost (12)` · `KNN (9)` · `Gradient Boosting (8)` · `Linear Regression (8)` · `Decision Tree (7)`

### Most Used Interpretability Methods
`SHAP (15)` · `PDP (6)` · `Gini Importance (1)` · `Sobol Sensitivity (1)` · `ICE Plots (1)` · `Surrogate Trees (1)`

### Top Journals
| Journal | Papers |
|---|---|
| International Journal of Hydrogen Energy | 9 |
| Energy | 4 |
| Biomass and Bioenergy | 3 |
| Renewable Energy | 2 |
| Fuel | 2 |

---

## Project Structure

```
Waste2Hydrogen_ML_Dashboard/
│
├── Waste2Hydrogen_ML_Dashboard.py   # Landing page (entry point)
│
├── pages/
│   ├── 1_Overview.py                # Dataset overview and ML family charts
│   ├── 2_Process_Analysis.py        # Hydrogen routes, feedstocks, process explainers
│   ├── 3_ML_Analysis.py             # ML algorithm, optimisation, interpretability analysis
│   └── 4_Paper_Explorer.py          # Searchable paper browser with technical summaries
│
└── database/
    ├── papers_cleaned.csv           # Main structured dataset (29 papers)
    ├── technical_summaries.csv      # Full technical summaries per paper
    ├── ml_methods_dictionary.py     # Technical explainers: ML algorithms, optimisers, XAI methods
    └── process_dictionary.py        # Technical explainers: H₂ routes and feedstock types
```

---

## Installation & Running Locally

### Prerequisites
- Python 3.9 or higher
- pip

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/waste2hydrogen-ml-dashboard.git
cd waste2hydrogen-ml-dashboard
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run Waste2Hydrogen_ML_Dashboard.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## Dependencies

```
streamlit>=1.32.0
pandas>=2.0.0
altair>=5.0.0
```

Create a `requirements.txt` with the above content, or install manually:

```bash
pip install streamlit pandas altair
```

---

## Pages in Detail

### 🏠 Landing Page — `Waste2Hydrogen_ML_Dashboard.py`
The entry point introduces the dashboard, displays key dataset metrics in stat pills, describes all four pages via feature cards, provides a suggested navigation path for first-time users, and outlines the scope and coverage of the review.

---

### 📊 Page 1 — Overview (`1_Overview.py`)
Provides a bird's-eye view of the dataset:
- Dataset type distribution (Experimental, Simulation, Literature, Hybrid, CFD, Sensor, Review)
- ML family frequency chart across all papers
- Publication year trends
- High-level summary statistics

---

### ⚗️ Page 2 — Process Analysis (`2_Process_Analysis.py`)
Explores hydrogen production routes and feedstocks:
- **4 chart rows**: Route frequency · Feedstock distribution · Study type donut + Country horizontal bar · System flags (Integrated System, Carbon Capture, LCA, TEA, Surrogate Model) · Dataset type + Year
- **Query form** with 9 filters: Route, Feedstock, Study Type, Year, Country, Journal, Integrated System, Carbon Capture, LCA, Dataset Type
- **Filtered results table** with 17 columns
- **Technical explainers** for all 17 hydrogen routes and 14 feedstock types, each with process description, operating conditions, H₂ yield range, key inputs/outputs, strengths, limitations, and ML applications
- Active filters highlight matching entries with ⭐ in the explainer tabs

---

### 🤖 Page 3 — ML Analysis (`3_ML_Analysis.py`)
Deep-dives into the ML methodologies:
- **Distribution charts** for ML algorithms, optimisation methods, and interpretability methods
- **Query form** with 4 filters: ML Algorithm, Optimisation Method, Interpretability Method, Journal
- **Filtered results table**
- **Technical explainer tabs** for:
  - 29 ML algorithms (description, family, type, strengths, limitations, domain use)
  - 16 optimisation methods (description, category, when to use, domain use)
  - 11 interpretability/XAI methods (description, XAI type, scope, strengths, limitations)
- All explainers sourced from `database/ml_methods_dictionary.py`

---

### 📚 Page 4 — Paper Explorer (`4_Paper_Explorer.py`)
Full paper browsing and reading interface:
- **Free-text search** across title, author, and journal fields
- **8 filter controls**: Year, Hydrogen Route, Feedstock, Study Type, ML Family, Dataset Type, Integrated System, LCA
- **Results table** (280px scrollable, 13 columns)
- **Paper detail view** with:
  - Dark gradient title banner (paper number, year, title, authors)
  - Meta row: journal, country, study type badge, R² with colour coding (🟢 ≥0.95 / 🟡 ≥0.85 / 🔴 below)
  - Quick-glance chips: route, feedstock, dataset size, system flags
  - Direct Google Drive link button
  - ML Snapshot expander (algorithms · optimisation · interpretability in 3 columns)
  - 8 collapsible technical summary sections: Objective, System Description, Modelling Approach, ML Component, Key Results, Strengths, Limitations, Research Gap
- **Chemistry symbol repair** — garbled subscripts in CSV (`H?`, `CO?`, `CH?`) automatically restored to `H₂`, `CO₂`, `CH₄` etc.
- **Bullet-to-Markdown conversion** — raw `•\t` / `o\t` CSV bullet format rendered as clean nested Markdown lists

---

## Data Notes

### `papers_cleaned.csv`
The primary dataset with one row per paper. Key columns include:

| Column | Description |
|---|---|
| `Serial` | Unique paper identifier (1–29) |
| `Title` | Full paper title |
| `Author` | Semicolon-separated author list |
| `Year` | Publication year |
| `Journal` | Journal name |
| `Country_Region` | Country or countries of study |
| `Type` | Original Research / Review / Simulation |
| `Hydrogen_Route` | Primary hydrogen production route |
| `Feedstock` | Feedstock(s) studied |
| `ML_Algorithms` | Semicolon-separated list of ML algorithms used |
| `ML_Family` | Normalised ML family classification |
| `Optimization_Method_Normalised` | Normalised optimisation methods |
| `Interpretability_Method_Normalised` | Normalised XAI/interpretability methods |
| `Best_R2` | Best reported R² value |
| `Integrated_System` | Yes/No — multi-unit system integration |
| `Carbon_Capture` | Yes/No — carbon capture component |
| `LCA` | Yes/No — life cycle assessment performed |
| `TEA` | Yes/No/Partial — techno-economic analysis |
| `Drive_Link` | Google Drive link to full paper PDF |

### `technical_summaries.csv`
One structured summary per paper (matched by `Serial`) with fields:
- Basic Information · Research Objective · System Description
- Modelling Approach · Machine Learning Component · Key Results
- Strengths · Limitations · Research Gap Identified

### `ml_methods_dictionary.py`
Python dictionary (`ML_METHODS_DICTIONARY`) with three sections:
- `ML_Algorithms` — 29 entries
- `Optimization_Methods` — 16 entries
- `Interpretability_Methods` — 11 entries

### `process_dictionary.py`
Python dictionary (`PROCESS_DICTIONARY`) with two sections:
- `Hydrogen_Routes` — 17 entries
- `Feedstocks` — 14 entries

---

## Scope & Coverage

**Included:**
- Papers published 2024–2026
- Studies applying ML to hydrogen production from waste feedstocks
- Thermochemical routes: gasification, SCWG, pyrolysis, HTL
- Biological routes: dark fermentation, photofermentation, biophotolysis
- Electrochemical routes: electrolysis
- Reforming routes: biogas steam reforming + dry reforming
- Integrated and hybrid system studies
- Review, simulation, and original research paper types

**Not included:**
- Papers without a direct ML modelling or application component
- Grey literature, theses, conference abstracts without full text
- Studies focused on fossil-fuel-based hydrogen without waste co-feed
- Papers pre-dating 2024
- Pure catalyst/materials development studies with no process ML
- TEA/LCA analyses without an ML predictive or optimisation model

---

## Acknowledgements

This dashboard was developed as part of a structured literature review on machine learning for sustainable hydrogen production. All papers referenced are publicly available via the journal links or accessible through the Drive links provided in the dataset.

---

## License

This project is released for academic and research use. Please cite the original papers appropriately when using insights drawn from this dashboard.