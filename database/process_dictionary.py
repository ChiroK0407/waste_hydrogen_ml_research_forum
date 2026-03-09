# =============================================================================
# PROCESS ANALYSIS DICTIONARY
# For: Smart ML Dashboard — Hydrogen Production from Wastes
# Covers: Hydrogen Production Routes | Feedstock Types
# Source: papers_cleaned.csv (29 papers)
# =============================================================================

PROCESS_DICTIONARY = {

    # =========================================================================
    # SECTION 1: HYDROGEN PRODUCTION ROUTES
    # =========================================================================
    "Hydrogen_Routes": {

        "SCWG": {
            "full_name": "Supercritical Water Gasification",
            "category": "Thermochemical",
            "phase": "Supercritical Aqueous",
            "temp_range": "374–700 °C",
            "pressure_range": "22–35 MPa",
            "description": (
                "SCWG converts wet biomass and waste feedstocks into a hydrogen-rich syngas by reacting them "
                "with water above its critical point (374 °C, 22.1 MPa). At supercritical conditions, water "
                "acts simultaneously as a solvent, reactant, and catalyst, enabling complete gasification of "
                "high-moisture feedstocks (60–90% water content) without an energy-intensive drying step. "
                "Key reactions include steam reforming, water–gas shift, and methanation. The process produces "
                "a clean, pressurised H₂/CO₂ gas stream that is readily suited for downstream CO₂ capture. "
                "Catalysts (alkali metals, Ni, Ru) are often used to improve H₂ selectivity and suppress char formation."
            ),
            "h2_yield_range": "10–50 mol H₂/kg dry biomass (catalyst-dependent)",
            "key_inputs": ["Wet biomass", "Sewage sludge", "Food waste", "Plastics", "Organic wastewater"],
            "key_outputs": ["H₂", "CO₂", "CH₄", "CO"],
            "strengths": [
                "No pre-drying needed — directly processes high-moisture waste streams",
                "High H₂ selectivity with appropriate catalysts",
                "Pressurised product stream facilitates carbon capture",
                "Simultaneous destruction of organic pollutants and pathogens",
            ],
            "limitations": [
                "Extreme operating conditions (high P and T) require expensive reactor materials",
                "Catalyst deactivation by char, sintering, and sulphur poisoning",
                "Corrosion and salt precipitation at supercritical conditions",
                "High capital and operating costs — limited pilot-scale validation",
            ],
            "ml_applications": (
                "ANN, Random Forest, SVM, XGBoost, and Gaussian Process models have been applied to predict "
                "H₂ yield, syngas composition, and carbon gasification efficiency from SCWG operating "
                "conditions (T, P, residence time, feedstock concentration) and biomass properties. "
                "SHAP and PDP are used to identify the most influential process variables."
            ),
        },

        "Gasification": {
            "full_name": "Biomass/Waste Gasification",
            "category": "Thermochemical",
            "phase": "High-Temperature Solid-Gas",
            "temp_range": "700–1200 °C",
            "pressure_range": "0.1–3 MPa (atmospheric to pressurised)",
            "description": (
                "Gasification converts carbonaceous feedstocks into a combustible syngas (H₂, CO, CO₂, CH₄, N₂) "
                "by reacting them with a controlled sub-stoichiometric amount of a gasifying agent (air, steam, "
                "O₂, CO₂, or their mixtures) at high temperatures. The process involves drying, pyrolysis, "
                "combustion, and reduction zones. Steam gasification maximises H₂ yield via the water–gas "
                "shift reaction. Gasifier configurations include fixed-bed (updraft/downdraft), fluidised-bed, "
                "and entrained-flow reactors. The raw syngas contains tars that must be removed before H₂ "
                "purification (PSA, membrane separation)."
            ),
            "h2_yield_range": "25–60 vol% H₂ in syngas (steam gasification)",
            "key_inputs": ["Woody biomass", "Agricultural residues", "MSW", "Plastics", "Coal blends", "RDF"],
            "key_outputs": ["H₂", "CO", "CO₂", "CH₄", "Tars", "Char", "Ash"],
            "strengths": [
                "Mature technology with established pilot and commercial-scale systems",
                "Flexible feedstock — handles a wide range of solid wastes",
                "High throughput and continuous operation capability",
                "Co-gasification of biomass with plastics/coal improves H₂ yield",
            ],
            "limitations": [
                "Tar formation causes fouling and catalyst poisoning in downstream equipment",
                "Syngas requires extensive cleaning (tar removal, desulphurisation) before use",
                "N₂ dilution with air gasification reduces H₂ concentration",
                "Ash and heavy metal management required for waste feedstocks",
            ],
            "ml_applications": (
                "ML models (ANN, SVM, Random Forest, XGBoost, AdaBoost) predict H₂ yield, tar content, "
                "and syngas composition from reactor temperature, equivalence ratio, steam-to-biomass ratio, "
                "and feedstock proximate/ultimate analysis. PSO-SVR is frequently optimal for small datasets. "
                "SHAP + PDP provide dual-objective interpretability for tar inhibition and H₂ maximisation."
            ),
        },

        "Gasification (Chemical Looping)": {
            "full_name": "Chemical Looping Gasification (CLG)",
            "category": "Thermochemical — Advanced",
            "phase": "Solid-Gas (Dual Reactor)",
            "temp_range": "700–1000 °C",
            "pressure_range": "0.1–0.3 MPa",
            "description": (
                "Chemical Looping Gasification uses an oxygen carrier (metal oxide, e.g., Fe₂O₃, NiO, CuO) "
                "to transfer oxygen from air to the fuel reactor, avoiding direct contact between fuel and air. "
                "In the fuel reactor, the metal oxide oxidises the biomass/waste to produce syngas while being "
                "reduced. The reduced metal is regenerated in a separate air reactor. This inherent gas "
                "separation produces a N₂-free, CO₂-rich flue gas from the air reactor and a pure H₂/CO "
                "stream from the fuel reactor, dramatically simplifying carbon capture. CLG offers high energy "
                "efficiency and is considered a promising pathway for negative-emission hydrogen."
            ),
            "h2_yield_range": "30–65 vol% H₂ (fuel reactor outlet)",
            "key_inputs": ["Biomass", "Coal", "Plastics", "Waste-derived fuels"],
            "key_outputs": ["H₂-rich syngas", "CO₂ (inherently separated)", "Ash"],
            "strengths": [
                "Inherent CO₂ separation — low-cost carbon capture without post-combustion treatment",
                "N₂-free syngas — high H₂ concentration without air separation unit",
                "High energy efficiency due to internal heat integration between reactors",
                "Potential for negative emissions with biomass feedstocks (BECCS)",
            ],
            "limitations": [
                "Oxygen carrier attrition, agglomeration, and deactivation over cycles",
                "Complex dual-reactor system with particle circulation challenges",
                "Still predominantly at pilot/bench scale — limited commercial deployment",
                "Feedstock ash can contaminate oxygen carrier particles",
            ],
            "ml_applications": (
                "ML models predict oxygen carrier conversion, syngas composition, and H₂ purity as a function "
                "of temperature, fuel/carrier ratio, and cycle time. Simulation datasets from CFD or process "
                "simulators (Aspen) are commonly used as training data."
            ),
        },

        "Gasification (Co-gasification)": {
            "full_name": "Co-gasification (Biomass + Waste Blends)",
            "category": "Thermochemical",
            "phase": "High-Temperature Solid-Gas",
            "temp_range": "750–1100 °C",
            "pressure_range": "0.1–1 MPa",
            "description": (
                "Co-gasification involves simultaneously gasifying a blend of two or more feedstocks — most "
                "commonly biomass with plastics, coal, municipal solid waste (MSW), or sewage sludge — to "
                "exploit synergistic effects that improve H₂ yield and carbon conversion beyond what either "
                "feedstock achieves alone. Plastics contribute high hydrogen content (H/C ratio) while biomass "
                "provides reactive char and alkali catalysts. Blending ratios are a critical optimisation "
                "variable, and ML models trained on blend composition data can identify optimal co-feed ratios."
            ),
            "h2_yield_range": "30–65 vol% H₂ (blend and conditions dependent)",
            "key_inputs": ["Biomass + plastics", "Biomass + coal", "Biomass + MSW", "Biomass + sludge"],
            "key_outputs": ["H₂-rich syngas", "CO", "CO₂", "Char", "Ash"],
            "strengths": [
                "Synergistic effects: plastic's high H content boosts H₂ yield beyond additive prediction",
                "Simultaneous waste valorisation of multiple waste streams",
                "Blending can improve ash melting behaviour and tar reduction",
                "Flexible operation — blend ratio can be adjusted in real time",
            ],
            "limitations": [
                "Synergistic effects are feedstock-pair specific and difficult to predict without experiments",
                "Plastic gasification produces HCl and other problematic trace species",
                "Ash chemistry interactions between co-feed components can cause fouling",
                "Regulatory complexity for co-processing classified waste streams",
            ],
            "ml_applications": (
                "ML models map the multi-dimensional blend composition + operating condition space to "
                "H₂ yield and syngas quality. Tree-based ensembles and ANNs are used; SHAP reveals "
                "which blend ratio and condition features dominate performance."
            ),
        },

        "Gasification (Downdraft)": {
            "full_name": "Downdraft Fixed-Bed Gasification",
            "category": "Thermochemical",
            "phase": "Fixed-Bed Solid-Gas",
            "temp_range": "700–900 °C",
            "pressure_range": "~0.1 MPa (atmospheric)",
            "description": (
                "In a downdraft (co-current) gasifier, both the feedstock and gasification agent flow "
                "downwards. The feedstock passes through drying, pyrolysis, combustion (oxidation), and "
                "reduction zones in sequence. The hot syngas passes through the reduction zone where tars "
                "are thermally cracked, producing a relatively clean, low-tar syngas compared to updraft "
                "designs. Downdraft gasifiers are well-suited to small-to-medium scale power generation "
                "and are widely used for agricultural residues and woody biomass."
            ),
            "h2_yield_range": "15–22 vol% H₂ in syngas (air gasification)",
            "key_inputs": ["Wood chips", "Agricultural residues", "Coconut shell", "Energy crops"],
            "key_outputs": ["Syngas (H₂, CO, CO₂, N₂, CH₄)", "Char", "Ash"],
            "strengths": [
                "Lower tar content than updraft gasifiers — reduced gas cleaning burden",
                "Simple, robust design — suitable for small-scale decentralised applications",
                "Well-established technology with extensive operational experience",
            ],
            "limitations": [
                "Sensitive to feedstock moisture content (ideally <20%)",
                "Poor performance with fine or high-ash feedstocks (bridging, channelling)",
                "Limited scale-up potential compared to fluidised-bed designs",
                "Lower H₂ yield compared to steam or O₂-blown systems",
            ],
            "ml_applications": (
                "ANN and ensemble models correlate equivalence ratio, feedstock moisture, and particle "
                "size to syngas H₂ concentration and cold gas efficiency."
            ),
        },

        "Gasification (Steam Co-gasification)": {
            "full_name": "Steam Co-gasification",
            "category": "Thermochemical",
            "phase": "High-Temperature Solid-Gas",
            "temp_range": "750–950 °C",
            "pressure_range": "0.1–0.5 MPa",
            "description": (
                "Steam co-gasification uses steam as the sole or primary gasifying agent for blended "
                "feedstocks. Steam promotes the water–gas reaction (C + H₂O → CO + H₂) and the water–gas "
                "shift reaction (CO + H₂O → CO₂ + H₂), maximising H₂ yield. The absence of nitrogen "
                "(unlike air gasification) produces a nitrogen-free, high-H₂ syngas, though an external "
                "heat source is required since steam gasification is endothermic. It is particularly "
                "effective for H₂-rich blends of biomass with high-hydrogen waste streams."
            ),
            "h2_yield_range": "40–65 vol% H₂ in syngas",
            "key_inputs": ["Biomass blends", "Waste-derived fuels", "Steam"],
            "key_outputs": ["H₂", "CO", "CO₂", "CH₄"],
            "strengths": [
                "Highest H₂ yield among gasification variants",
                "N₂-free syngas — directly suitable for H₂ purification by PSA",
                "Steam-to-biomass ratio is a powerful control variable for H₂ maximisation",
            ],
            "limitations": [
                "Endothermic — requires external energy input (reduces overall efficiency)",
                "Higher operating costs than air gasification",
                "Steam generation infrastructure adds capital cost",
            ],
            "ml_applications": (
                "ML models optimise steam-to-biomass ratio alongside temperature and pressure "
                "to maximise H₂ yield. GA and PSO are used with trained surrogate models."
            ),
        },

        "Biological (Dark Fermentation)": {
            "full_name": "Dark Fermentation Biohydrogen Production",
            "category": "Biological",
            "phase": "Aqueous Anaerobic",
            "temp_range": "25–70 °C (mesophilic 30–40 °C; thermophilic 50–70 °C)",
            "pressure_range": "~0.1 MPa (atmospheric)",
            "description": (
                "Dark fermentation is an anaerobic microbial process in which fermentative bacteria "
                "(Clostridium, Enterobacter, Thermoanaerobacterium) break down carbohydrate-rich substrates "
                "to produce H₂, CO₂, and organic acids (acetate, butyrate) without light. The theoretical "
                "maximum yield is 4 mol H₂/mol glucose (Thauer limit), but practical yields are typically "
                "1–3.5 mol H₂/mol glucose due to metabolic pathway competition. Key process parameters "
                "include pH (5.0–6.5), temperature, hydraulic retention time (HRT), and substrate "
                "concentration. The organic acid effluent can be further converted via photofermentation "
                "or anaerobic digestion to recover additional energy."
            ),
            "h2_yield_range": "1–3.5 mol H₂/mol glucose; 50–300 mL H₂/g VS",
            "key_inputs": ["Wastewater substrates", "Food waste", "Sugar-rich biomass", "Cheese whey", "Sucrose"],
            "key_outputs": ["H₂", "CO₂", "Volatile fatty acids (acetate, butyrate, propionate)"],
            "strengths": [
                "Light-independent — continuous operation day and night",
                "Can directly valorise organic-rich wastewaters and food waste",
                "Well-understood microbiology and established reactor configurations (CSTR, UASB, ASBR)",
                "Organic acid effluent has value for further energy recovery (photofermentation, AD)",
            ],
            "limitations": [
                "Low H₂ yield — only 33% of theoretical maximum achievable from glucose oxidation",
                "H₂ partial pressure inhibition — continuous gas sparging required",
                "pH management critical — acidic metabolites shift pathways towards propionate (no H₂)",
                "Substrate specificity — complex feedstocks require pre-treatment",
            ],
            "ml_applications": (
                "ANN, Random Forest, XGBoost, and Modified Monod kinetic models predict H₂ yield and "
                "volumetric production rate from pH, temperature, substrate concentration, HRT, and "
                "inoculum source. SHAP analysis identifies pH and substrate load as dominant drivers. "
                "Bayesian Optimisation and RSM are used to optimise fermentation conditions."
            ),
        },

        "Biological (Dark + Photo Fermentation)": {
            "full_name": "Two-Stage Dark + Photofermentation",
            "category": "Biological — Two-Stage",
            "phase": "Aqueous Anaerobic + Photobiological",
            "temp_range": "30–40 °C (dark); 30–35 °C (photo)",
            "pressure_range": "~0.1 MPa",
            "description": (
                "Two-stage systems couple dark fermentation (Stage 1) with photofermentation (Stage 2) to "
                "overcome the Thauer limit. Dark fermentation converts carbohydrates to H₂ and volatile "
                "fatty acids (VFAs). These VFAs are then fed to purple non-sulphur (PNS) bacteria "
                "(Rhodobacter sphaeroides, R. palustris) in the photofermentation stage, which use light "
                "energy (nitrogenase enzyme) to convert VFAs completely to H₂ and CO₂. The theoretical "
                "maximum for the combined system approaches 12 mol H₂/mol glucose — three times the "
                "dark fermentation limit. Practical yields of 6–9 mol H₂/mol glucose have been reported."
            ),
            "h2_yield_range": "4–10 mol H₂/mol glucose (combined)",
            "key_inputs": ["Sugar-rich substrates", "Wastewater", "VFA-rich effluent from Stage 1"],
            "key_outputs": ["H₂", "CO₂", "Bacterial biomass (PNS bacteria)"],
            "strengths": [
                "Substantially higher H₂ yield than dark fermentation alone",
                "Near-complete substrate conversion to H₂",
                "PNS bacteria can use a broad range of organic acids",
            ],
            "limitations": [
                "Light requirement for Stage 2 — large photobioreactor area needed",
                "Low light conversion efficiency of PNS bacteria (~1–5%)",
                "VFA composition from Stage 1 must match PNS substrate preferences",
                "Complex two-reactor system with high capital and operational complexity",
            ],
            "ml_applications": (
                "ML models for two-stage systems predict inter-stage VFA composition and final H₂ yield. "
                "ANNs with SHAP analysis identify light intensity and VFA speciation as key Stage 2 drivers."
            ),
        },

        "Biological (Biophotolysis + Fermentation)": {
            "full_name": "Biophotolysis Combined with Fermentation",
            "category": "Biological — Photobiological",
            "phase": "Aqueous Photobiological + Anaerobic",
            "temp_range": "25–35 °C",
            "pressure_range": "~0.1 MPa",
            "description": (
                "Biophotolysis uses the photosynthetic apparatus of microalgae (green algae: Chlamydomonas "
                "reinhardtii) or cyanobacteria to split water into H₂ and O₂ using solar energy. The "
                "[FeFe]-hydrogenase or nitrogenase enzymes catalyse proton reduction to H₂. Direct "
                "biophotolysis is O₂-sensitive (hydrogenase inhibited by O₂), so indirect biophotolysis "
                "uses sulphur deprivation to separate the O₂-evolving and H₂-producing phases. Combining "
                "biophotolysis with dark fermentation or photofermentation in multi-stage systems improves "
                "overall solar-to-H₂ conversion efficiency."
            ),
            "h2_yield_range": "0.5–3 mol H₂/mol glucose equivalent; solar conversion ~0.5–2%",
            "key_inputs": ["Water", "CO₂", "Sunlight", "Microalgae or cyanobacteria culture"],
            "key_outputs": ["H₂", "O₂", "Algal biomass"],
            "strengths": [
                "Uses water and sunlight as sole inputs — renewable and carbon-neutral",
                "No organic substrate required for biophotolysis stage",
                "Algal biomass byproduct has additional value (lipids, protein)",
            ],
            "limitations": [
                "Very low solar conversion efficiency — large land area requirements",
                "O₂ sensitivity of hydrogenase severely limits continuous H₂ production",
                "Photobioreactor construction and operation costs are high",
                "Scale-up from lab to pilot remains a major challenge",
            ],
            "ml_applications": (
                "CNN for microalgae classification and health monitoring; ANN and ELM for H₂ yield "
                "prediction from light intensity, CO₂ concentration, temperature, and nutrient status. "
                "Photoperiod tuning optimisation applied to maximise H₂ photoproduction rates."
            ),
        },

        "Biological (Anaerobic Fermentation)": {
            "full_name": "Anaerobic Fermentation (General)",
            "category": "Biological",
            "phase": "Aqueous Anaerobic",
            "temp_range": "25–55 °C",
            "pressure_range": "~0.1 MPa",
            "description": (
                "Anaerobic fermentation encompasses all biological hydrogen-producing processes that occur "
                "in the absence of oxygen, driven by microbial communities or pure cultures. This includes "
                "dark fermentation, hyperthermophilic fermentation, and thermophilic processes. Mixed "
                "microbial consortia derived from anaerobic sludge, compost, or soil can ferment a broader "
                "range of complex substrates than pure cultures. Reactor designs include CSTR, UASB, "
                "packed-bed, and membrane bioreactors. Pre-treatment of inoculum (heat shock, acid/base) "
                "suppresses methanogens that consume H₂."
            ),
            "h2_yield_range": "0.5–3.5 mol H₂/mol hexose substrate",
            "key_inputs": ["Organic wastewaters", "Food waste", "Agricultural effluents", "Microalgae"],
            "key_outputs": ["H₂", "CO₂", "Volatile fatty acids", "Alcohols"],
            "strengths": [
                "Broad substrate range including complex lignocellulosic and proteinaceous wastes",
                "Established reactor engineering and operational know-how from anaerobic digestion",
                "Can be integrated with CH₄ production for maximum energy recovery",
            ],
            "limitations": [
                "Methanogen suppression requires ongoing management",
                "Lower H₂ yields from complex substrates than from pure sugars",
                "Effluent treatment required before discharge",
            ],
            "ml_applications": (
                "ML models predict H₂ production rate and yield from substrate composition, OLR, "
                "HRT, pH, and temperature. Sensitivity analysis and SHAP identify critical operational parameters."
            ),
        },

        "Biological (Fermentation)": {
            "full_name": "Biological Fermentation (Broad)",
            "category": "Biological",
            "phase": "Aqueous",
            "temp_range": "25–70 °C",
            "pressure_range": "~0.1 MPa",
            "description": (
                "This category encompasses biological hydrogen production via fermentative pathways broadly, "
                "including both dark and light-dependent fermentation processes studied in the reviewed "
                "literature. Papers in this category examine H₂ production using various microbial strains, "
                "reactor designs, and operating strategies without restricting to a single fermentation mode. "
                "The focus is on the ML-based prediction and optimisation of fermentation performance "
                "metrics such as H₂ production rate (HPR), cumulative H₂ production, and substrate "
                "conversion efficiency across diverse experimental conditions."
            ),
            "h2_yield_range": "Highly variable — substrate and organism dependent",
            "key_inputs": ["Organic substrates", "Wastewater", "Microbial inoculum"],
            "key_outputs": ["H₂", "CO₂", "Organic acids", "Biomass"],
            "strengths": [
                "Diverse applicability across substrate types and microbial communities",
                "Established biological and reactor engineering knowledge base",
            ],
            "limitations": [
                "High variability between studies makes cross-study ML modelling challenging",
                "Process performance highly sensitive to inoculum source and pre-treatment",
            ],
            "ml_applications": (
                "ANN, XGBoost, and kinetic models (Modified Monod) are applied. SHAP and sensitivity "
                "analysis identify pH and substrate concentration as the dominant control variables."
            ),
        },

        "Biological (Dark Fermentation + Photo cycles)": {
            "full_name": "Dark Fermentation with Photobiological Cycles",
            "category": "Biological — Hybrid Cyclic",
            "phase": "Aqueous Anaerobic + Photobiological",
            "temp_range": "30–40 °C",
            "pressure_range": "~0.1 MPa",
            "description": (
                "This process integrates dark fermentation cycles with intermittent light-driven "
                "photohydrogen production stages to exploit both metabolic pathways. During dark cycles, "
                "fermentative bacteria convert organic substrates to H₂ and VFAs. During illuminated "
                "cycles, photosynthetic organisms (microalgae, PNS bacteria) use the VFAs and light "
                "to produce additional H₂. The cyclic, time-shared approach reduces the engineering "
                "complexity of fully separate two-stage systems while capturing the yield benefits "
                "of both pathways. Photoperiod optimisation is a key ML application in this context."
            ),
            "h2_yield_range": "3–8 mol H₂/mol glucose (cycle-averaged)",
            "key_inputs": ["Carbohydrate-rich substrates", "VFAs from dark phase", "Light (for photo cycles)"],
            "key_outputs": ["H₂", "CO₂", "Residual organic acids"],
            "strengths": [
                "Combines yields of both biological H₂ pathways in a single system",
                "Photoperiod tuning offers an accessible optimisation lever",
                "Lower capital complexity than fully separate two-stage systems",
            ],
            "limitations": [
                "Light distribution in reactor limits scale-up",
                "Metabolic synchronisation between dark and light phases is non-trivial",
                "Operational complexity exceeds single-stage dark fermentation",
            ],
            "ml_applications": (
                "ML models (ANN, LSTM) predict H₂ yield variation across light/dark cycle parameters. "
                "Photoperiod tuning optimisation and sensitivity analysis guide cycle design."
            ),
        },

        "Biofuel (HTL; pyrolysis)": {
            "full_name": "Biofuel Production via Hydrothermal Liquefaction and Pyrolysis",
            "category": "Thermochemical — Biofuel Pathway",
            "phase": "Thermal / Subcritical Aqueous",
            "temp_range": "250–550 °C (HTL: 250–374 °C; Pyrolysis: 400–550 °C)",
            "pressure_range": "5–20 MPa (HTL); ~0.1 MPa (pyrolysis)",
            "description": (
                "HTL converts wet biomass at subcritical water conditions (250–374 °C, 5–20 MPa) into a "
                "bio-crude oil, aqueous phase (with dissolved organics), gas phase (CO₂, H₂), and solid "
                "biochar. Pyrolysis thermally decomposes dry biomass (400–550 °C, atmospheric pressure) "
                "in the absence of oxygen to produce bio-oil, syngas (including H₂), and biochar. Both "
                "pathways produce H₂ as part of the gas fraction. While neither is a dedicated H₂ "
                "production route, the H₂-rich gas fraction can be upgraded via steam reforming of "
                "bio-oil or aqueous phase reforming of HTL aqueous byproducts."
            ),
            "h2_yield_range": "5–25 vol% H₂ in gas fraction (process and feedstock dependent)",
            "key_inputs": ["Algae", "Lignocellulosic biomass", "Sewage sludge", "Municipal food waste"],
            "key_outputs": ["Bio-crude/bio-oil", "Biochar", "Aqueous phase", "H₂-containing gas"],
            "strengths": [
                "HTL processes wet feedstocks without drying",
                "Biochar has value as soil amendment or activated carbon precursor",
                "Bio-crude can be co-processed in existing petroleum refineries",
                "Flexible product slate — energy products and H₂ simultaneously",
            ],
            "limitations": [
                "H₂ is a minor product — not the primary target for these routes",
                "High pressure for HTL requires substantial capital investment",
                "Bio-crude upgrading to transport fuels requires further hydrotreatment",
                "Aqueous phase contains recalcitrant organics requiring treatment",
            ],
            "ml_applications": (
                "CNN and ANN models are applied to algal biomass characterisation and H₂/bio-crude "
                "yield prediction. XGBoost and Random Forest trained on HTL datasets identify "
                "temperature, feedstock ash content, and reaction time as dominant predictors."
            ),
        },

        "Biogas Reforming (SR + DR)": {
            "full_name": "Biogas Reforming — Steam Reforming + Dry Reforming",
            "category": "Thermochemical — Reforming",
            "phase": "Gas-Phase Catalytic",
            "temp_range": "700–950 °C",
            "pressure_range": "0.1–3 MPa",
            "description": (
                "Biogas (55–70% CH₄, 30–45% CO₂ from anaerobic digestion or landfill) is reformed to "
                "syngas (H₂ + CO) via steam reforming (SR: CH₄ + H₂O → 3H₂ + CO) and dry reforming "
                "(DR: CH₄ + CO₂ → 2H₂ + 2CO) simultaneously. Combined SR + DR of biogas (bi-reforming) "
                "is thermally advantageous — the endothermic DR can be partially offset by the exothermic "
                "water–gas shift. Ni-based catalysts are standard; noble metals (Rh, Ru) offer superior "
                "coking resistance. The H₂/CO ratio is tunable by adjusting the SR/DR balance, targeting "
                "downstream Fischer-Tropsch, methanol synthesis, or pure H₂ production."
            ),
            "h2_yield_range": "2.5–3.5 mol H₂/mol CH₄ (SR dominant); 1.5–2 mol H₂/mol CH₄ (DR dominant)",
            "key_inputs": ["Biogas (CH₄ + CO₂)", "Steam (for SR)", "Ni or noble metal catalyst"],
            "key_outputs": ["H₂", "CO", "CO₂ (residual)", "H₂O"],
            "strengths": [
                "Utilises existing biogas infrastructure — low feedstock cost",
                "CO₂ in biogas is a reactant in DR — simultaneous waste valorisation",
                "Established catalytic reforming technology from natural gas industry",
                "Tunable H₂/CO ratio for diverse downstream applications",
            ],
            "limitations": [
                "Catalyst coking (carbon deposition) deactivates reforming catalyst rapidly",
                "High operating temperatures require heat integration for efficiency",
                "H₂S in biogas poisons Ni catalysts — requires upstream gas cleaning",
                "Endothermic reactions require substantial energy input",
            ],
            "ml_applications": (
                "ML models predict CH₄ conversion, H₂ yield, and catalyst lifetime from operating "
                "temperature, S/C ratio, and feed composition. Neural networks and Gaussian Process "
                "models with uncertainty quantification are used for catalyst performance modelling."
            ),
        },

        "Electrolysis": {
            "full_name": "Water Electrolysis for Hydrogen Production",
            "category": "Electrochemical",
            "phase": "Aqueous / Solid Electrolyte",
            "temp_range": "20–80 °C (alkaline/PEM); 700–900 °C (SOEC)",
            "pressure_range": "0.1–3 MPa",
            "description": (
                "Water electrolysis splits water into H₂ and O₂ using electrical energy. Three main "
                "technology types exist: (1) Alkaline Water Electrolysis (AWE) — mature, low-cost, uses "
                "KOH electrolyte; (2) Proton Exchange Membrane (PEM) electrolysis — fast response, high "
                "purity H₂, suited for intermittent renewable energy sources; (3) Solid Oxide Electrolysis "
                "Cells (SOEC) — high-efficiency steam electrolysis at 700–900 °C using waste heat. When "
                "powered by renewable electricity (solar, wind), the product is green hydrogen with near-zero "
                "lifecycle emissions. In the reviewed literature, ML is applied to electrolyser efficiency "
                "modelling, degradation prediction, and renewable energy coupling optimisation."
            ),
            "h2_yield_range": "Energy efficiency: 60–85% (LHV); ~50 kWh/kg H₂ (PEM)",
            "key_inputs": ["Water", "Electricity (ideally renewable)", "KOH or PEM electrolyte"],
            "key_outputs": ["H₂ (cathode)", "O₂ (anode)"],
            "strengths": [
                "Produces ultra-high purity H₂ (>99.999%) with no CO",
                "Fast response — PEM can follow fluctuating renewable power",
                "Modular and scalable from kW to GW",
                "Zero direct emissions with renewable electricity",
            ],
            "limitations": [
                "High electricity cost dominates economics (~70–80% of H₂ production cost)",
                "PEM: requires expensive Pt/Ir catalysts and Nafion membrane",
                "SOEC: high temperature introduces materials durability challenges",
                "Grid-powered electrolysis has high carbon footprint",
            ],
            "ml_applications": (
                "Reinforcement Learning for real-time electrolyser scheduling and renewable energy "
                "integration. ANN models predict cell voltage and efficiency degradation. Multi-objective "
                "optimisation (NSGA-II, MOGWO) balances H₂ cost and carbon intensity."
            ),
        },

        "Gasification + Electrolysis + Methanation": {
            "full_name": "Integrated Gasification + Electrolysis + Methanation (Power-to-Gas)",
            "category": "Hybrid Thermochemical-Electrochemical",
            "phase": "Multi-phase Integrated System",
            "temp_range": "Multiple zones: 700–1100 °C (gasification); 250–350 °C (methanation)",
            "pressure_range": "0.1–3 MPa",
            "description": (
                "This integrated pathway combines biomass gasification (producing H₂-rich syngas) with "
                "water electrolysis (producing green H₂ from renewable electricity) and catalytic "
                "methanation (CO + CO₂ + H₂ → CH₄ + H₂O) to produce substitute natural gas (SNG) or "
                "maximise H₂ output. Excess renewable electricity drives electrolysis, providing "
                "supplemental H₂ to the gasification syngas. The integration enables flexible operation: "
                "when renewable electricity is abundant, more H₂ is co-produced; when scarce, gasification "
                "H₂ dominates. This Power-to-Gas concept improves overall carbon utilisation."
            ),
            "h2_yield_range": "System-level: dependent on electricity availability and gasification throughput",
            "key_inputs": ["Biomass/waste", "Water", "Renewable electricity", "Ni catalyst (methanation)"],
            "key_outputs": ["H₂ or SNG (CH₄)", "CO₂", "Heat"],
            "strengths": [
                "Flexible product slate: H₂ or SNG on demand",
                "Maximises use of intermittent renewable electricity via Power-to-Gas buffering",
                "High overall carbon utilisation — CO and CO₂ from gasification are methanated",
                "Synergistic integration reduces overall system levelised cost",
            ],
            "limitations": [
                "High system complexity — multiple unit operations to integrate and control",
                "Methanation consumes H₂ — trade-off between H₂ and SNG production",
                "Capital-intensive — requires gasifier, electrolyser, and methanation reactor",
                "TEA and LCA required to validate economic and environmental case",
            ],
            "ml_applications": (
                "ML-based system optimisation uses MILP, NSGA-II, and Reinforcement Learning to "
                "schedule gasification and electrolysis operations dynamically. Surrogate models "
                "replace expensive process simulation for real-time control."
            ),
        },

        "Multiple (SMR; SCWG; Electrolysis; Biological; Photocatalytic)": {
            "full_name": "Multi-Route Comparative Study",
            "category": "Comparative / Review",
            "phase": "Multiple",
            "temp_range": "Varies by route",
            "pressure_range": "Varies by route",
            "description": (
                "Papers in this category conduct comparative analyses or reviews of multiple hydrogen "
                "production routes simultaneously, including steam methane reforming (SMR), SCWG, "
                "electrolysis, biological fermentation, and photocatalytic splitting. The ML "
                "contribution in these studies is typically a benchmarking or meta-analysis of model "
                "performance across routes, identification of research gaps, or development of a "
                "unified predictive framework applicable to multiple production pathways. These studies "
                "are valuable for identifying cross-cutting ML opportunities and technology readiness "
                "levels across the H₂ production landscape."
            ),
            "h2_yield_range": "Route-dependent (see individual route entries)",
            "key_inputs": ["Route-specific"],
            "key_outputs": ["Route-specific H₂"],
            "strengths": [
                "Holistic comparison enables technology selection guidance",
                "Identifies which ML approaches transfer across production routes",
                "Provides techno-economic and environmental benchmarking across routes",
            ],
            "limitations": [
                "Breadth limits depth — route-specific insights may be superficial",
                "Comparing routes with fundamentally different maturity levels is challenging",
                "Data heterogeneity across routes complicates unified ML modelling",
            ],
            "ml_applications": (
                "Meta-analysis of ML model performance across routes. Transfer learning and "
                "cross-route feature importance analysis. Multi-objective optimisation across "
                "competing H₂ production technologies."
            ),
        },
    },

    # =========================================================================
    # SECTION 2: FEEDSTOCK TYPES
    # =========================================================================
    "Feedstocks": {

        "Biomass": {
            "full_name": "Lignocellulosic Biomass (General)",
            "category": "Solid Organic Waste / Energy Crop",
            "origin": "Agricultural, Forestry, Energy Crops",
            "composition": "Cellulose (30–50%), Hemicellulose (15–30%), Lignin (10–25%), Ash (1–15%)",
            "description": (
                "Biomass is the most widely studied feedstock for thermochemical hydrogen production. "
                "Lignocellulosic biomass comprises three structural biopolymers: cellulose (glucose chains), "
                "hemicellulose (mixed pentose/hexose sugars), and lignin (aromatic polymer). The specific "
                "proportions vary widely by species and growth conditions and significantly influence "
                "gasification and pyrolysis behaviour. Key characterisation parameters used as ML model "
                "inputs include proximate analysis (moisture, ash, volatile matter, fixed carbon) and "
                "ultimate analysis (C, H, N, O, S content). Biomass has near-zero net CO₂ emissions "
                "when sustainably sourced."
            ),
            "suitable_routes": ["Gasification", "SCWG", "Pyrolysis", "Biological Fermentation"],
            "h2_potential": "High — 25–60 vol% H₂ in syngas from steam gasification",
            "key_ml_inputs": ["Moisture content", "Ash content", "Volatile matter", "C/H/O ratios", "Particle size"],
            "strengths": [
                "Widely available and low-cost in agricultural and forestry regions",
                "Carbon-neutral — CO₂ released was recently sequestered during growth",
                "Rich ML dataset availability — most studied feedstock category",
                "High volatile matter promotes good gasification reactivity",
            ],
            "limitations": [
                "High variability in composition — ML models must account for feedstock diversity",
                "Moisture content requires pre-drying for most thermochemical routes",
                "Seasonal and geographical supply variability affects process consistency",
                "Alkali and alkaline earth metals in ash cause fouling and slagging",
            ],
        },

        "Wastewater substrates": {
            "full_name": "Wastewater and Organic Liquid Substrates",
            "category": "Liquid Organic Waste",
            "origin": "Municipal, Industrial, Agricultural Effluents",
            "composition": "COD: 0.5–50 g/L; Carbohydrates, proteins, lipids, VFAs",
            "description": (
                "Wastewater substrates encompass a broad range of liquid organic waste streams used "
                "as substrates for dark fermentation and anaerobic fermentation biohydrogen production. "
                "These include municipal wastewater, food processing effluents, dairy wastewaters "
                "(cheese whey, milk processing), brewery and distillery effluents, and agricultural "
                "slurries. The substrate's chemical oxygen demand (COD), carbohydrate/protein/lipid "
                "ratios, and the presence of inhibitors (NH₄⁺, heavy metals, sulphide) are critical "
                "determinants of H₂ yield. ML models trained on wastewater fermentation data must "
                "account for this high compositional variability."
            ),
            "suitable_routes": ["Dark Fermentation", "Photofermentation", "Anaerobic Fermentation"],
            "h2_potential": "Moderate — 50–200 mL H₂/g COD (dark fermentation)",
            "key_ml_inputs": ["COD", "Carbohydrate concentration", "pH", "Temperature", "HRT", "C/N ratio"],
            "strengths": [
                "Negative feedstock cost — waste treatment avoided",
                "High moisture content ideal for biological routes",
                "Diverse carbon sources available for fermentative bacteria",
                "Simultaneous wastewater treatment and energy recovery",
            ],
            "limitations": [
                "Inhibitory compounds (ammonia, sulphide, heavy metals) reduce H₂ yield",
                "Highly variable composition complicates consistent model training",
                "Pre-treatment often required (pH adjustment, dilution, nutrient addition)",
                "Low H₂ concentration in fermentation gas requires upgrading",
            ],
        },

        "Biomass + Plastics": {
            "full_name": "Biomass and Plastic Waste Blends",
            "category": "Solid Mixed Waste Blend",
            "origin": "Municipal Solid Waste / Industrial Mixed Waste",
            "composition": "Variable blend ratio; plastics: C-H polymers (PE, PP, PS, PET)",
            "description": (
                "Blending lignocellulosic biomass with plastic waste for co-gasification or co-pyrolysis "
                "exploits synergistic interactions that improve H₂ yield beyond additive prediction. "
                "Plastics (polyethylene PE, polypropylene PP, polystyrene PS) have very high hydrogen "
                "content (H/C ≈ 2 for PE/PP) and low ash content, complementing biomass's high reactivity "
                "and volatile matter. Synergistic effects arise from hydrogen transfer from plastics to "
                "biomass-derived radicals. The blend ratio (biomass:plastic weight fraction) is the primary "
                "optimisation variable, typically studied in the 20:80 to 80:20 range."
            ),
            "suitable_routes": ["Gasification (Co-gasification)", "Pyrolysis", "SCWG"],
            "h2_potential": "High — synergistic H₂ yield enhancement of 15–40% over individual components",
            "key_ml_inputs": ["Blend ratio", "Temperature", "Heating rate", "Gasifying agent", "Particle size"],
            "strengths": [
                "Plastic waste valorisation — addresses end-of-life plastic problem",
                "High H/C ratio of plastics significantly boosts H₂ yield",
                "Plastics reduce ash and improve char reactivity in co-processing",
                "Synergistic interactions create non-linear yield gains predictable by ML",
            ],
            "limitations": [
                "Plastic gasification produces HCl (from PVC), dioxins, and other harmful trace species",
                "Halogenated plastics require specialised gas cleaning equipment",
                "Synergistic effects are specific to plastic type — PET, PS behave differently from PE/PP",
                "Mixed plastic waste streams require sorting or accept compositional variability",
            ],
        },

        "Algae": {
            "full_name": "Microalgae and Macroalgae",
            "category": "Aquatic Biomass",
            "origin": "Freshwater / Marine Cultivation",
            "composition": "Lipids (5–50%), Proteins (20–60%), Carbohydrates (10–50%), Ash (5–20%)",
            "description": (
                "Algae are photosynthetic microorganisms with substantially higher biomass productivity "
                "per unit area than terrestrial crops. Microalgae (Chlorella, Scenedesmus, Spirulina) "
                "have high lipid and protein content that makes them attractive for HTL, pyrolysis, and "
                "biological H₂ production. Their high moisture content (>80%) makes them natural "
                "candidates for SCWG and HTL. In biological routes, Chlamydomonas reinhardtii "
                "is the principal organism for biophotolysis H₂ production. The biochemical composition "
                "varies significantly with growth conditions (N-limitation increases lipid content), "
                "making ML-based composition-to-yield mapping particularly valuable."
            ),
            "suitable_routes": ["SCWG", "HTL", "Biophotolysis", "Dark Fermentation", "Pyrolysis"],
            "h2_potential": "Moderate-High — route dependent; 15–40 vol% H₂ from SCWG",
            "key_ml_inputs": ["Lipid content", "Protein content", "Ash content", "Growth conditions", "Cell density"],
            "strengths": [
                "High areal biomass productivity (10–50× higher than terrestrial crops)",
                "Can be cultivated on wastewater — nutrient and water recycling",
                "Biochemical composition tuneable via growth condition manipulation",
                "Direct solar-to-hydrogen via biophotolysis pathways",
            ],
            "limitations": [
                "High cultivation and harvesting costs dominate economics",
                "High ash content in some species reduces thermochemical conversion efficiency",
                "Protein-derived nitrogen can form NOx during thermochemical processing",
                "Scale-up of photobioreactors remains cost-prohibitive at commercial scale",
            ],
        },

        "MSW": {
            "full_name": "Municipal Solid Waste (MSW)",
            "category": "Mixed Urban Waste",
            "origin": "Urban Residential and Commercial Waste Collection",
            "composition": "Highly heterogeneous: organics (50–70%), paper (10–20%), plastics (10–15%), metals, glass",
            "description": (
                "MSW is the mixed solid waste collected from households, commercial premises, and public "
                "spaces in urban areas. Its composition varies significantly by region, season, and "
                "economic development level. For thermochemical H₂ production, the organic fraction "
                "(food waste, garden waste) and Refuse-Derived Fuel (RDF — shredded, sorted, dried MSW) "
                "are the most relevant fractions. MSW gasification is commercially deployed in several "
                "countries. The high compositional variability is a major challenge for ML modelling — "
                "robust models must generalise across different waste compositions."
            ),
            "suitable_routes": ["Gasification", "Pyrolysis", "SCWG (organic fraction)"],
            "h2_potential": "Moderate — 20–45 vol% H₂ in syngas; highly variable",
            "key_ml_inputs": ["Proximate analysis", "Ultimate analysis", "Moisture", "Chlorine content", "LHV"],
            "strengths": [
                "Abundant and reliably available in urban areas",
                "Negative or zero feedstock cost — tipping fees may apply",
                "Reduces landfill burden and associated methane emissions",
                "RDF preparation improves consistency for ML model training",
            ],
            "limitations": [
                "High heterogeneity and variability challenge ML model generalisation",
                "Contaminants (PVC → HCl; heavy metals) require extensive gas cleaning",
                "Sorting and pre-processing (RDF production) adds cost and complexity",
                "Regulatory requirements for waste-to-energy vary significantly by jurisdiction",
            ],
        },

        "Sewage sludge": {
            "full_name": "Sewage Sludge (Wastewater Treatment Biosolids)",
            "category": "Wet Organic Waste",
            "origin": "Municipal Wastewater Treatment Plants",
            "composition": "Proteins (30–40%), Lipids (15–25%), Carbohydrates (10–20%), Ash (20–50%)",
            "description": (
                "Sewage sludge is the solid residue from municipal wastewater treatment — it exists as "
                "primary sludge (raw settled solids), secondary/biological sludge (waste activated sludge, "
                "WAS), and anaerobically digested sludge (digestate). Its high water content (95–99%) makes "
                "it ideal for SCWG and hydrothermal processes without energy-intensive drying. High protein "
                "content provides nitrogen (NH₄⁺ in hydrothermal products) that must be managed. Heavy "
                "metals in sewage sludge can inhibit catalysts in thermochemical processes. In biological "
                "routes, sludge serves as both substrate and inoculum source for dark fermentation."
            ),
            "suitable_routes": ["SCWG", "Gasification (co-gasification)", "Pyrolysis", "Dark Fermentation"],
            "h2_potential": "Moderate — 15–35 mol H₂/kg dry sludge (SCWG)",
            "key_ml_inputs": ["Volatile solids (VS)", "Total solids (TS)", "Protein content", "Heavy metal content", "pH"],
            "strengths": [
                "High moisture content eliminates drying requirement for SCWG",
                "Available at scale at every wastewater treatment plant",
                "Sludge disposal problem converted to energy recovery opportunity",
                "High protein/nitrogen content supports dark fermentation microbiology",
            ],
            "limitations": [
                "Heavy metals (Cd, Pb, Hg, Cr) can poison thermochemical catalysts",
                "High ash content reduces energy yield from thermochemical routes",
                "Nitrogen compounds form ammonia and NOx in thermochemical processing",
                "Regulatory restrictions on sludge use and residue disposal in many regions",
            ],
        },

        "Coal + Biomass + Plastics": {
            "full_name": "Ternary Co-feed Blend: Coal, Biomass, and Plastics",
            "category": "Solid Mixed Fuel Blend",
            "origin": "Industrial / Mixed Waste Streams",
            "composition": "Variable ternary ratio; coal: high C, low H/C; biomass: moderate H/C; plastics: high H/C",
            "description": (
                "Ternary blends of coal, biomass, and plastic waste for co-gasification represent an "
                "advanced approach to maximising H₂ yield while valorising multiple waste streams. Coal "
                "provides high carbon content and consistent energy density; biomass adds reactive volatile "
                "matter and alkali catalysts; plastics contribute high H/C ratios and boost H₂ yield. "
                "The ternary blend optimisation is a high-dimensional problem — blend ratio, particle size, "
                "and operating conditions interact non-linearly. ML models trained on ternary blend "
                "gasification data can identify optimal blend ratios more efficiently than full "
                "experimental factorial designs."
            ),
            "suitable_routes": ["Gasification (Co-gasification)", "Pyrolysis"],
            "h2_potential": "High — synergistic interactions in optimised blends can achieve >50 vol% H₂",
            "key_ml_inputs": ["Coal fraction", "Biomass fraction", "Plastic fraction", "Temperature", "Steam/O₂ ratio"],
            "strengths": [
                "Simultaneous valorisation of three distinct waste/fuel streams",
                "Multi-component synergies enable H₂ yields exceeding binary co-feed performance",
                "Coal provides process stability and consistent energy input",
                "Blend ratio optimisation is a natural target for ML-guided experimental design",
            ],
            "limitations": [
                "High complexity — ternary interactions difficult to characterise experimentally",
                "Coal introduces sulphur requiring downstream desulphurisation",
                "Regulatory classification of coal as fossil fuel impacts carbon accounting",
                "Plastic-derived contaminants (HCl, heavy metals) compound with coal ash",
            ],
        },

        "Wastewater + Microalgae": {
            "full_name": "Wastewater-Cultivated Microalgae",
            "category": "Integrated Wastewater-Biomass System",
            "origin": "Microalgae Grown on Municipal or Industrial Wastewater",
            "composition": "Algal biomass composition (see Algae) with nutrient-rich cultivation medium",
            "description": (
                "This integrated approach cultivates microalgae on wastewater (nutrient removal) and then "
                "uses the harvested biomass for hydrogen production. The wastewater provides the nitrogen "
                "(NH₄⁺, NO₃⁻) and phosphorus (PO₄³⁻) nutrients required for algal growth, simultaneously "
                "treating the wastewater effluent. The harvested algal biomass can be processed via SCWG, "
                "HTL, dark fermentation, or biophotolysis. This circular approach avoids synthetic "
                "fertiliser costs for algal cultivation and converts a wastewater treatment liability into "
                "a hydrogen production asset."
            ),
            "suitable_routes": ["SCWG", "HTL", "Dark Fermentation", "Biophotolysis"],
            "h2_potential": "Moderate — depends on algal strain and chosen production route",
            "key_ml_inputs": ["Algal biomass concentration", "Nutrient (N, P) loading", "Light availability", "HRT"],
            "strengths": [
                "Double benefit: wastewater treatment + bioenergy production",
                "Low-cost algal cultivation — wastewater nutrients replace synthetic fertilisers",
                "Closed nutrient loop reduces overall system environmental footprint",
                "Scalable alongside existing wastewater treatment infrastructure",
            ],
            "limitations": [
                "Wastewater contaminants (heavy metals, micropollutants) can accumulate in biomass",
                "Algal harvesting from dilute cultures remains energy-intensive",
                "Seasonal variation in algal productivity complicates consistent H₂ production",
                "Regulatory barriers to land application of wastewater-grown biomass",
            ],
        },

        "Food waste": {
            "full_name": "Food Waste and Kitchen Residues",
            "category": "Organic Urban Waste",
            "origin": "Households, Restaurants, Food Processing Industry",
            "composition": "Carbohydrates (30–60%), Proteins (10–25%), Lipids (10–30%), Water (60–90%)",
            "description": (
                "Food waste is a carbohydrate and lipid-rich organic waste stream generated throughout "
                "the food supply chain — from agricultural production (crop residues, spoilage) through "
                "processing (whey, fruit pomace) to consumption (kitchen waste). Its high moisture content "
                "and readily fermentable carbohydrates make it an excellent substrate for dark fermentation "
                "biohydrogen production. Lipid-rich fractions can be converted via HTL. The variable "
                "composition (dependent on meal type, season, and source) is a challenge for robust ML "
                "model development — transfer learning and composition-normalised features help address this."
            ),
            "suitable_routes": ["Dark Fermentation", "SCWG", "Anaerobic Co-digestion", "HTL"],
            "h2_potential": "Good — 80–220 mL H₂/g VS from dark fermentation",
            "key_ml_inputs": ["Carbohydrate content", "Protein/lipid ratio", "pH", "Total solids", "C/N ratio"],
            "strengths": [
                "Abundant — ~1.3 billion tonnes of food waste generated globally per year",
                "High fermentability — simple sugars readily converted by fermentative bacteria",
                "High moisture content suitable for biological and hydrothermal routes",
                "Negative cost feedstock — gate fees may apply at food processing facilities",
            ],
            "limitations": [
                "High lipid content can inhibit dark fermentation bacteria above certain thresholds",
                "Variable and unpredictable composition requires adaptive ML models",
                "Rapid putrefaction requires prompt processing or pre-treatment",
                "Seasonal composition variation (festive periods produce fat-rich waste) affects yield",
            ],
        },

        "Cheese whey": {
            "full_name": "Cheese Whey (Dairy Processing Effluent)",
            "category": "Liquid Agro-Industrial Waste",
            "origin": "Dairy Industry — Cheese Production",
            "composition": "Lactose (4–5% w/v), Proteins (0.6–0.8%), Minerals; COD ~60–80 g/L",
            "description": (
                "Cheese whey is the liquid effluent generated during cheese production — approximately "
                "9 litres of whey are produced per kilogram of cheese. It contains high concentrations "
                "of lactose (a disaccharide of glucose and galactose) and whey proteins, making it an "
                "excellent substrate for dark fermentation biohydrogen production. Lactose is readily "
                "fermented by Clostridium and Enterobacter species without pre-treatment. The consistent "
                "composition of industrial cheese whey is an advantage for ML model training compared to "
                "heterogeneous municipal food waste."
            ),
            "suitable_routes": ["Dark Fermentation", "Photofermentation", "Anaerobic Fermentation"],
            "h2_potential": "High for dark fermentation — 2.5–3.5 mol H₂/mol lactose",
            "key_ml_inputs": ["Lactose concentration", "pH", "Temperature", "HRT", "Inoculum type"],
            "strengths": [
                "Consistent composition — lactose content predictable from source",
                "No pre-treatment required — lactose directly fermentable",
                "High-volume industrial effluent with significant H₂ production potential",
                "Well-characterised substrate for ML model development and validation",
            ],
            "limitations": [
                "High protein content can buffer pH, masking acidification during fermentation",
                "Seasonal availability tied to dairy production cycles",
                "Competing with more lucrative whey protein isolate recovery market",
                "Whey proteins can form fouling deposits in continuous reactor systems",
            ],
        },

        "Sucrose substrate": {
            "full_name": "Sucrose (Model Substrate for Dark Fermentation)",
            "category": "Model Carbohydrate Substrate",
            "origin": "Synthetic / Analytical Grade; Sugarcane / Sugar Beet Industry",
            "composition": "Pure sucrose (C₁₂H₂₂O₁₁) or sucrose-containing effluents",
            "description": (
                "Sucrose is widely used as a model substrate in dark fermentation H₂ production research "
                "because its well-defined chemical composition allows reproducible, controlled experiments "
                "ideal for ML model development and validation. It is hydrolysed to glucose and fructose "
                "by fermentative bacteria, both of which are efficiently converted to H₂ via the acetate "
                "and butyrate pathways. Sucrose-containing wastewaters (sugarcane molasses, soft drink "
                "effluents, confectionery wastewater) provide a scaled-up, lower-cost alternative to "
                "analytical grade sucrose for practical applications."
            ),
            "suitable_routes": ["Dark Fermentation", "Photofermentation"],
            "h2_potential": "High — up to 3.47 mol H₂/mol sucrose (theoretical); 2.5–3.0 mol/mol practical",
            "key_ml_inputs": ["Sucrose concentration", "pH", "Temperature", "HRT", "Buffer capacity"],
            "strengths": [
                "Well-defined composition — ideal for controlled ML training experiments",
                "High theoretical H₂ yield — benchmark substrate for fermentation studies",
                "Reproducible experimental results enabling reliable ML dataset construction",
                "Industrially available from sugarcane/beet industry effluents at low cost",
            ],
            "limitations": [
                "Not a 'waste' feedstock — limited real-world applicability as pure substrate",
                "ML models trained on pure sucrose may not generalise to complex real wastes",
                "High sucrose concentrations cause substrate inhibition of H₂-producing bacteria",
            ],
        },

        "Wood pellets": {
            "full_name": "Wood Pellets (Densified Woody Biomass)",
            "category": "Processed Woody Biomass",
            "origin": "Forestry Residues, Sawmill By-products",
            "composition": "Cellulose (~42%), Hemicellulose (~28%), Lignin (~27%), Ash (<1%)",
            "description": (
                "Wood pellets are densified cylindrical biomass pellets produced by compressing dried "
                "and milled sawdust, shavings, or forestry residues under high pressure. Their standardised "
                "dimensions, moisture content (<10%), and low ash content make them an ideal, consistent "
                "feedstock for thermochemical H₂ production. The uniformity of wood pellets is particularly "
                "advantageous for ML dataset development — reduced compositional variability improves "
                "model accuracy and generalisability. They are commercially available and widely used "
                "in gasification systems."
            ),
            "suitable_routes": ["Gasification", "Pyrolysis", "SCWG"],
            "h2_potential": "High — 30–55 vol% H₂ from steam gasification",
            "key_ml_inputs": ["Moisture", "Particle size (diameter)", "Temperature", "Equivalence ratio", "S/B ratio"],
            "strengths": [
                "Highly consistent composition — low variability ideal for ML training",
                "Low ash content reduces fouling and slagging",
                "Commercial availability enables reproducible experimental datasets",
                "Low moisture eliminates drying pre-treatment",
            ],
            "limitations": [
                "Higher cost than raw agricultural residues or waste biomass",
                "Energy and cost of pelletisation (grinding, drying, compressing) must be accounted for",
                "Sustainability questions around dedicated forestry for pellet production",
            ],
        },

        "Forestry residues": {
            "full_name": "Forestry and Logging Residues",
            "category": "Lignocellulosic Agricultural/Forestry Waste",
            "origin": "Forest Harvesting, Thinning, and Logging Operations",
            "composition": "Cellulose (35–45%), Hemicellulose (20–30%), Lignin (20–30%), Ash (1–5%)",
            "description": (
                "Forestry residues include branches, tops, bark, and stumps left after timber harvesting, "
                "as well as material from forest thinning and roadside clearing. They are low-cost, "
                "abundant waste biomass streams with good thermochemical conversion properties. Their "
                "higher bark and lignin content compared to clean wood increases char yield in pyrolysis "
                "and can slightly reduce H₂ selectivity in gasification. Spatial distribution across "
                "forest areas creates supply chain and logistics challenges. ML models can incorporate "
                "spatially varying composition data from different forest types."
            ),
            "suitable_routes": ["Gasification", "Pyrolysis", "SCWG"],
            "h2_potential": "Good — 25–50 vol% H₂ from steam gasification",
            "key_ml_inputs": ["Species mix", "Bark content", "Moisture", "Ultimate analysis", "Ash composition"],
            "strengths": [
                "Low-cost waste stream with no dedicated cultivation required",
                "Carbon-neutral — supports sustainable forest management",
                "Available in large quantities in forestry-intensive regions",
                "Consistent enough for ML model development with proximate/ultimate analysis as inputs",
            ],
            "limitations": [
                "High spatial dispersion increases collection and transport costs",
                "Seasonal and geographic variability in composition",
                "Higher moisture content than pelletised wood requires pre-drying or SCWG",
                "Competing uses (pulp, timber, mulch) limit availability",
            ],
        },

        "Biogas (CH₄ + CO₂)": {
            "full_name": "Biogas from Anaerobic Digestion",
            "category": "Gaseous Organic Waste / Bioenergy Carrier",
            "origin": "Anaerobic Digestion of Organic Waste (Landfill, WWTP, Agricultural)",
            "composition": "CH₄: 50–70%, CO₂: 30–45%, H₂S: 0.1–0.5%, H₂O, traces of N₂, O₂",
            "description": (
                "Biogas is the gaseous product of anaerobic digestion (AD) of organic matter. It consists "
                "primarily of methane and CO₂, with trace amounts of H₂S, NH₃, and siloxanes. As a "
                "feedstock for H₂ production, biogas undergoes steam reforming (SR) and/or dry reforming "
                "(DR) over Ni-based catalysts at 700–950 °C to produce syngas (H₂ + CO), followed by "
                "water–gas shift and H₂ purification. The CO₂ already present in biogas serves as the "
                "oxidant for dry reforming, making biogas reforming a thermodynamically advantageous "
                "pathway compared to pure methane reforming."
            ),
            "suitable_routes": ["Biogas Reforming (SR + DR)", "Chemical Looping Reforming"],
            "h2_potential": "High — 2.5–3 mol H₂/mol CH₄ (steam reforming pathway)",
            "key_ml_inputs": ["CH₄/CO₂ ratio", "H₂S content", "Temperature", "Steam/carbon ratio", "Catalyst type"],
            "strengths": [
                "Utilises existing AD infrastructure — biogas already produced at scale",
                "CO₂ in biogas is a reactant, not a waste — reduces CO₂ purification cost",
                "H₂S and other impurities are manageable with existing gas cleaning technology",
                "Renewable origin — biogas from waste has low carbon footprint",
            ],
            "limitations": [
                "H₂S in raw biogas poisons Ni reforming catalysts — requires upstream removal",
                "Siloxanes in landfill gas deposit silica on catalyst surfaces",
                "Methane in biogas is a potent greenhouse gas — any leakage is problematic",
                "Reforming is endothermic and energy-intensive",
            ],
        },
    },
}


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_route_info(route_name: str) -> dict:
    """Retrieve detailed info for a specific hydrogen production route."""
    return PROCESS_DICTIONARY["Hydrogen_Routes"].get(route_name, {})


def get_feedstock_info(feedstock_name: str) -> dict:
    """Retrieve detailed info for a specific feedstock."""
    return PROCESS_DICTIONARY["Feedstocks"].get(feedstock_name, {})


def list_all_entries() -> dict:
    """Return a summary of all entries in the dictionary."""
    return {
        "Hydrogen_Routes": sorted(PROCESS_DICTIONARY["Hydrogen_Routes"].keys()),
        "Feedstocks": sorted(PROCESS_DICTIONARY["Feedstocks"].keys()),
    }


def get_routes_for_feedstock(feedstock_name: str) -> list:
    """Return suitable hydrogen production routes for a given feedstock."""
    info = PROCESS_DICTIONARY["Feedstocks"].get(feedstock_name, {})
    return info.get("suitable_routes", [])


# =============================================================================
# QUICK DEMO
# =============================================================================
if __name__ == "__main__":
    import json
    summary = list_all_entries()
    for section, entries in summary.items():
        print(f"\n{section} ({len(entries)} entries):")
        for e in entries:
            print(f"  - {e}")
