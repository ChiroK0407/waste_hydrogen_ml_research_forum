# =============================================================================
# ML METHODS TECHNICAL DICTIONARY
# For: Smart ML Dashboard — Analysis of ML Methods for Hydrogen Production
# Covers: ML Algorithms | Optimization Methods | Interpretability Methods
# Source: papers_cleaned.csv (29 papers, hydrogen production from wastes)
# =============================================================================

ML_METHODS_DICTIONARY = {

    # =========================================================================
    # SECTION 1: ML ALGORITHMS
    # =========================================================================
    "ML_Algorithms": {

        "ANN": {
            "full_name": "Artificial Neural Network",
            "family": "Neural Network",
            "type": "Supervised Learning",
            "description": (
                "ANNs are computational models inspired by the structure and function of biological neural networks. "
                "They consist of an input layer, one or more hidden layers, and an output layer, where each node "
                "(neuron) applies a non-linear activation function (e.g., ReLU, sigmoid, tanh) to a weighted sum "
                "of its inputs. Training occurs via backpropagation combined with gradient descent to minimise a "
                "loss function. In hydrogen production research, ANNs are widely used for predicting H₂ yield, "
                "syngas composition, and reactor performance from process variables such as temperature, pressure, "
                "equivalence ratio, and feedstock properties."
            ),
            "strengths": [
                "Universal function approximators capable of capturing complex non-linear relationships",
                "Flexible architecture — depth and width can be tuned to problem complexity",
                "Well-established in thermochemical and biological hydrogen process modelling",
            ],
            "limitations": [
                "Prone to overfitting on small experimental datasets",
                "Black-box nature limits physical interpretability",
                "Sensitive to hyperparameter choices (learning rate, layer size, activation function)",
            ],
            "typical_use_in_domain": "H₂ yield prediction from gasification, SCWG, pyrolysis, and dark fermentation",
        },

        "Adaboost": {
            "full_name": "Adaptive Boosting",
            "family": "Boosting Ensemble",
            "type": "Supervised Learning",
            "description": (
                "AdaBoost is an ensemble meta-algorithm that iteratively trains a sequence of weak learners "
                "(typically shallow decision trees) on re-weighted versions of the training data. Misclassified "
                "or poorly predicted samples receive higher weights in subsequent rounds, forcing later learners "
                "to focus on hard cases. The final prediction is a weighted majority vote (classification) or "
                "weighted sum (regression) of all weak learners. It is effective for small-to-medium datasets "
                "common in experimental hydrogen production studies."
            ),
            "strengths": [
                "Robust performance on structured tabular data with limited samples",
                "Less prone to overfitting than single decision trees",
                "Simple to implement; few critical hyperparameters",
            ],
            "limitations": [
                "Sensitive to noisy data and outliers — high weights amplify noise",
                "Sequential training makes it slower than parallel ensemble methods",
                "Weaker than gradient boosting variants (XGBoost, LightGBM) on complex datasets",
            ],
            "typical_use_in_domain": "Tar yield prediction; H₂ concentration modelling in biomass gasification",
        },

        "Bagging": {
            "full_name": "Bootstrap Aggregating",
            "family": "Bagging Ensemble",
            "type": "Supervised Learning",
            "description": (
                "Bagging trains multiple instances of a base learner (commonly decision trees) on different "
                "bootstrap samples (random subsets with replacement) of the training data and aggregates their "
                "predictions by averaging (regression) or majority voting (classification). This variance-reduction "
                "strategy improves generalisation and stability, especially when the base learner is unstable "
                "(high variance). Random Forest is the most prominent special case of bagging applied to decision trees."
            ),
            "strengths": [
                "Significantly reduces variance compared to a single model",
                "Parallelisable — each model trains independently",
                "Provides natural out-of-bag (OOB) error estimation without a separate validation set",
            ],
            "limitations": [
                "Does not reduce bias — if the base model is biased, the ensemble remains biased",
                "Less interpretable than a single model",
                "Memory-intensive for large ensembles",
            ],
            "typical_use_in_domain": "Ensemble modelling for biohydrogen yield prediction and process optimisation",
        },

        "Bagxgboost": {
            "full_name": "Bagged XGBoost",
            "family": "Hybrid Ensemble",
            "type": "Supervised Learning",
            "description": (
                "Bagged XGBoost combines the variance-reduction of bootstrap aggregation (bagging) with the "
                "powerful gradient boosting framework of XGBoost. Multiple XGBoost models are trained on "
                "different bootstrap samples of the data and their predictions are averaged. This hybrid "
                "approach reduces the risk of overfitting that can occur with a single XGBoost model tuned "
                "aggressively, particularly beneficial for small experimental datasets in hydrogen production."
            ),
            "strengths": [
                "Combines variance reduction (bagging) with strong learner capacity (XGBoost)",
                "More robust to overfitting than a single XGBoost on small datasets",
                "Leverages XGBoost's handling of missing values and regularisation",
            ],
            "limitations": [
                "Increased computational cost — multiple XGBoost models must be trained",
                "Hyperparameter space is large (bagging + XGBoost parameters)",
                "Marginal improvement over single XGBoost may not justify cost on large datasets",
            ],
            "typical_use_in_domain": "Advanced ensemble strategies for hydrogen yield and process efficiency prediction",
        },

        "Bayesian Regression": {
            "full_name": "Bayesian Regression",
            "family": "Probabilistic / Linear Model",
            "type": "Supervised Learning",
            "description": (
                "Bayesian Regression extends ordinary linear regression by placing prior probability distributions "
                "over model parameters and updating them with observed data via Bayes' theorem to yield a posterior "
                "distribution. Rather than a single point estimate, it produces a full predictive distribution, "
                "naturally quantifying uncertainty. Regularisation is embedded via the prior (e.g., Gaussian prior "
                "corresponds to Ridge regression). It is particularly valuable in hydrogen production research where "
                "datasets are small and uncertainty quantification is critical."
            ),
            "strengths": [
                "Inherent uncertainty quantification — outputs predictive distributions, not just point estimates",
                "Regularisation is principled and probabilistically motivated",
                "Well-suited to small datasets where frequentist overfitting is a risk",
            ],
            "limitations": [
                "Assumes linearity (in its basic form) — poor for highly non-linear H₂ yield relationships",
                "Computationally expensive for large feature spaces with complex priors",
                "Requires careful prior specification which can influence results significantly",
            ],
            "typical_use_in_domain": "Uncertainty-aware modelling of biohydrogen yields; probabilistic process analysis",
        },

        "Catboost": {
            "full_name": "Categorical Boosting",
            "family": "Boosting Ensemble",
            "type": "Supervised Learning",
            "description": (
                "CatBoost is a gradient boosting algorithm developed by Yandex that uses ordered boosting "
                "(target statistics computed in a way that prevents target leakage) and native handling of "
                "categorical features without manual encoding. It builds symmetric (oblivious) decision trees "
                "which have fast prediction times. Its ordered boosting approach reduces overfitting on small "
                "datasets. In hydrogen production studies with mixed numerical and categorical inputs (e.g., "
                "catalyst type, feedstock category), CatBoost handles these directly."
            ),
            "strengths": [
                "Native categorical feature handling — no manual one-hot encoding required",
                "Reduced overfitting via ordered boosting on small datasets",
                "Fast inference due to symmetric tree structure",
            ],
            "limitations": [
                "Longer training time compared to XGBoost or LightGBM",
                "Less community adoption in the process engineering domain",
                "Default hyperparameters may need substantial tuning for optimal results",
            ],
            "typical_use_in_domain": "Prediction tasks with mixed categorical (catalyst, feedstock type) and numerical inputs",
        },

        "Cnn": {
            "full_name": "Convolutional Neural Network",
            "family": "Deep Learning / Neural Network",
            "type": "Supervised Learning",
            "description": (
                "CNNs are deep neural networks that apply learnable convolutional filters to detect local patterns "
                "in structured data (images, spectra, time-series). Convolutional layers extract spatial/temporal "
                "features, pooling layers reduce dimensionality, and fully-connected layers perform final prediction. "
                "In biofuel and hydrogen research, CNNs are applied to image-based classification of microalgae "
                "morphology, spectroscopic data interpretation, and processing sensor time-series data from reactors."
            ),
            "strengths": [
                "Automatic feature extraction from raw image or spectral data",
                "Translation-invariant — can detect features regardless of position",
                "Achieves state-of-the-art on image-based biological classification tasks",
            ],
            "limitations": [
                "Requires large labelled datasets — data-hungry",
                "Computationally intensive; requires GPU for efficient training",
                "Architecture design (filter sizes, depth) requires domain expertise",
            ],
            "typical_use_in_domain": "Image-based algae classification; spectroscopic feature extraction for biofuel production",
        },

        "Decision Tree": {
            "full_name": "Decision Tree",
            "family": "Tree-Based",
            "type": "Supervised Learning",
            "description": (
                "A Decision Tree partitions the feature space into axis-aligned rectangular regions through a "
                "recursive binary splitting process guided by an impurity criterion (Gini impurity for classification; "
                "MSE or MAE for regression). Each internal node represents a feature threshold test and each leaf "
                "node a prediction. The tree is fully interpretable — the decision path from root to leaf can be "
                "read directly as an if-then rule set. In hydrogen research, they serve both as standalone models "
                "and as base learners in ensemble methods."
            ),
            "strengths": [
                "Fully interpretable and visualisable — explicit rule extraction",
                "No feature scaling required; handles mixed data types",
                "Fast training and prediction",
            ],
            "limitations": [
                "High variance — small data changes can drastically alter the tree structure",
                "Prone to overfitting without pruning or depth constraints",
                "Poor extrapolation — cannot predict beyond training data range",
            ],
            "typical_use_in_domain": "Rule extraction for H₂ yield optimisation; base learner in Random Forest and boosting models",
        },

        "Deep Learning": {
            "full_name": "Deep Learning (general)",
            "family": "Neural Network",
            "type": "Supervised / Semi-Supervised / Unsupervised Learning",
            "description": (
                "Deep Learning refers to neural architectures with many hidden layers (deep networks) that learn "
                "hierarchical feature representations from data. This umbrella term covers feedforward deep ANNs, "
                "CNNs, RNNs, LSTMs, Transformers, and Physics-Informed variants. The depth enables modelling "
                "complex non-linear mappings. In hydrogen production, deep learning is applied to large-scale "
                "simulation data, multi-variable process control, and data fusion from multiple sensors or sources."
            ),
            "strengths": [
                "Capable of modelling highly complex, multi-scale relationships",
                "Scalable to large datasets and high-dimensional inputs",
                "Flexible architecture enables task-specific customisation",
            ],
            "limitations": [
                "Extremely data-hungry — experimental H₂ datasets are often too small",
                "Black-box — low interpretability without auxiliary XAI methods",
                "Computationally expensive to train and tune",
            ],
            "typical_use_in_domain": "Large-scale H₂ process simulation data; multi-input yield and efficiency modelling",
        },

        "Elm": {
            "full_name": "Extreme Learning Machine",
            "family": "Neural Network",
            "type": "Supervised Learning",
            "description": (
                "ELM is a single-hidden-layer feedforward neural network (SLFN) where input weights and hidden "
                "biases are randomly assigned and fixed; only the output weights are analytically computed via "
                "least-squares (Moore-Penrose pseudoinverse). This eliminates iterative backpropagation, resulting "
                "in training speeds orders of magnitude faster than standard ANNs. ELM is particularly attractive "
                "for small datasets in hydrogen production where rapid model development and deployment are needed."
            ),
            "strengths": [
                "Extremely fast training — analytical solution, no gradient descent",
                "Good generalisation on small experimental datasets",
                "Simple implementation with minimal hyperparameters",
            ],
            "limitations": [
                "Random initialisation introduces variance between runs — results not fully reproducible",
                "Performance generally below deep networks on large, complex datasets",
                "Less expressive than multi-layer deep architectures",
            ],
            "typical_use_in_domain": "Rapid modelling for algal biofuel/biohydrogen yield prediction with limited data",
        },

        "Ensemble Boosting": {
            "full_name": "Ensemble Boosting (general)",
            "family": "Boosting Ensemble",
            "type": "Supervised Learning",
            "description": (
                "Ensemble Boosting is a general class of meta-learning algorithms that combine multiple weak "
                "learners sequentially, where each subsequent learner corrects the errors of its predecessors. "
                "This includes AdaBoost, Gradient Boosting, XGBoost, LightGBM, and CatBoost. The boosting "
                "paradigm reduces both bias and variance, achieving strong predictive performance on structured "
                "tabular data. In hydrogen production ML studies, boosting ensembles consistently rank among "
                "the best-performing model families."
            ),
            "strengths": [
                "State-of-the-art performance on tabular/structured data",
                "Sequential error correction reduces both bias and variance",
                "Built-in regularisation (in modern variants) prevents overfitting",
            ],
            "limitations": [
                "Sequential training cannot be parallelised across trees within the sequence",
                "More hyperparameters to tune than simpler models",
                "Can overfit noisy small datasets if not properly regularised",
            ],
            "typical_use_in_domain": "General predictive modelling across hydrogen production routes (gasification, SCWG, fermentation)",
        },

        "Extra Trees": {
            "full_name": "Extra-Randomised Trees (Extremely Randomised Trees)",
            "family": "Tree-Based Ensemble",
            "type": "Supervised Learning",
            "description": (
                "Extra Trees builds an ensemble of decision trees with two additional levels of randomisation "
                "beyond Random Forest: (1) split thresholds are chosen completely at random for each feature "
                "rather than optimally, and (2) the entire training set (not a bootstrap sample) is used for "
                "each tree. This extreme randomisation reduces variance and computation at the cost of slightly "
                "higher bias. It often matches or exceeds Random Forest performance while being faster to train."
            ),
            "strengths": [
                "Faster training than Random Forest — no optimal split search",
                "Very low variance due to double randomisation",
                "Provides feature importance rankings for interpretability",
            ],
            "limitations": [
                "Higher bias than Random Forest due to non-optimal splits",
                "Less established in the hydrogen production literature",
                "Feature importance can be biased towards high-cardinality features",
            ],
            "typical_use_in_domain": "Fast ensemble modelling for H₂ yield and process condition optimisation",
        },

        "Gaussian Process": {
            "full_name": "Gaussian Process Regression (GPR)",
            "family": "Kernel-Based / Probabilistic",
            "type": "Supervised Learning",
            "description": (
                "GPR is a non-parametric Bayesian approach that defines a prior distribution over functions "
                "and updates it with observed data to produce a posterior predictive distribution. Predictions "
                "include both a mean estimate and a confidence interval, providing rigorous uncertainty "
                "quantification. The behaviour is governed by a kernel (covariance) function (e.g., RBF, Matérn) "
                "that encodes assumptions about function smoothness. GPR is highly effective for small "
                "experimental datasets, as commonly encountered in thermochemical hydrogen production studies."
            ),
            "strengths": [
                "Full predictive uncertainty quantification — critical for safety-relevant process design",
                "Flexible non-parametric modelling with kernel selection",
                "Excellent performance on small datasets",
            ],
            "limitations": [
                "Computational complexity scales as O(n³) — impractical for large datasets without approximations",
                "Kernel selection and hyperparameter optimisation require expertise",
                "Assumes Gaussian noise — may not suit all experimental error structures",
            ],
            "typical_use_in_domain": "Small-dataset SCWG and pyrolysis H₂ yield modelling with uncertainty bounds",
        },

        "Gradient Boosting": {
            "full_name": "Gradient Boosting Regressor/Classifier",
            "family": "Boosting Ensemble",
            "type": "Supervised Learning",
            "description": (
                "Gradient Boosting builds an additive ensemble of decision trees by fitting each new tree to "
                "the negative gradient (pseudo-residuals) of a differentiable loss function with respect to "
                "the current ensemble prediction. This generalises AdaBoost to arbitrary differentiable loss "
                "functions. Regularisation is achieved via a learning rate (shrinkage), tree depth constraints, "
                "and subsampling. Gradient Boosting is among the most powerful methods for tabular hydrogen "
                "production data and is the foundation for XGBoost and LightGBM."
            ),
            "strengths": [
                "Highly accurate on structured/tabular data",
                "Flexible loss function selection (MSE, MAE, Huber, etc.)",
                "Robust to outliers with appropriate loss function choice",
            ],
            "limitations": [
                "Sequential tree building prevents full parallelisation",
                "Requires careful tuning of learning rate and number of estimators",
                "Prone to overfitting without regularisation on small datasets",
            ],
            "typical_use_in_domain": "H₂ yield, tar yield, and syngas composition prediction across multiple thermochemical routes",
        },

        "Kernel Ridge": {
            "full_name": "Kernel Ridge Regression",
            "family": "Kernel-Based",
            "type": "Supervised Learning",
            "description": (
                "Kernel Ridge Regression (KRR) combines Ridge regression (L2-regularised linear regression) "
                "with the kernel trick, enabling non-linear regression in high-dimensional feature spaces "
                "without explicit feature mapping. The kernel function (e.g., RBF, polynomial) implicitly "
                "computes inner products in the transformed space. Unlike SVR, KRR has a closed-form analytical "
                "solution (no quadratic programming), making it efficient for moderate dataset sizes."
            ),
            "strengths": [
                "Analytically solvable — no iterative optimisation",
                "Flexible non-linear modelling via kernel selection",
                "Well-regularised — L2 penalty prevents overfitting",
            ],
            "limitations": [
                "Computationally O(n³) — scales poorly to large datasets",
                "Kernel and regularisation hyperparameter selection critical",
                "Less interpretable than linear models",
            ],
            "typical_use_in_domain": "Non-linear yield modelling in thermochemical hydrogen processes with small datasets",
        },

        "Knn": {
            "full_name": "K-Nearest Neighbours",
            "family": "Instance-Based / Non-parametric",
            "type": "Supervised Learning",
            "description": (
                "KNN is a non-parametric, lazy learning algorithm that predicts the output for a new data point "
                "by averaging (regression) or majority voting (classification) among its K nearest training "
                "samples in the feature space, using a distance metric (typically Euclidean). There is no "
                "explicit training phase — the entire training set is stored. It is intuitive and requires no "
                "assumptions about data distribution, making it a useful baseline model for hydrogen yield "
                "prediction from experimental process data."
            ),
            "strengths": [
                "Simple, interpretable decision logic",
                "No model training — adapts automatically to new training data",
                "Effective when decision boundary is locally smooth",
            ],
            "limitations": [
                "High memory and prediction cost — scales linearly with training data size",
                "Sensitive to irrelevant features and feature scaling",
                "Poor performance in high-dimensional spaces (curse of dimensionality)",
            ],
            "typical_use_in_domain": "Baseline comparison model for H₂ yield prediction; useful for small, low-dimensional datasets",
        },

        "Lightgbm": {
            "full_name": "Light Gradient Boosting Machine",
            "family": "Boosting Ensemble",
            "type": "Supervised Learning",
            "description": (
                "LightGBM is a highly efficient gradient boosting framework that uses two innovations: "
                "(1) Gradient-based One-Side Sampling (GOSS) — retains samples with large gradients and "
                "randomly drops those with small gradients, and (2) Exclusive Feature Bundling (EFB) — bundles "
                "mutually exclusive sparse features to reduce dimensionality. It builds trees leaf-wise (best-first) "
                "rather than level-wise, enabling deeper trees with lower memory. These optimisations make "
                "LightGBM significantly faster than XGBoost and standard Gradient Boosting."
            ),
            "strengths": [
                "Fastest training speed among gradient boosting implementations",
                "Memory efficient — handles large datasets with millions of samples",
                "Leaf-wise tree growth achieves lower loss for a given number of leaves",
            ],
            "limitations": [
                "Leaf-wise growth can overfit on small datasets — requires careful regularisation (min_data_in_leaf)",
                "Less robust to hyperparameter choices than XGBoost on small data",
                "Less adoption in the hydrogen production ML literature",
            ],
            "typical_use_in_domain": "Large-scale hydrogen process optimisation studies; fast model comparison pipelines",
        },

        "Linear Regression": {
            "full_name": "Linear Regression",
            "family": "Linear Model",
            "type": "Supervised Learning",
            "description": (
                "Linear Regression models the target variable as a weighted linear combination of input features, "
                "with weights estimated by minimising the sum of squared residuals (OLS) or via regularised "
                "variants (Ridge, Lasso, ElasticNet). Despite its simplicity, it provides valuable physical "
                "insight into how individual process variables (temperature, pressure, feed ratio) linearly "
                "influence H₂ yield. It also serves as a critical baseline to assess the benefit of more "
                "complex non-linear models."
            ),
            "strengths": [
                "Fully interpretable — coefficients directly quantify feature influence",
                "Computationally trivial to train and predict",
                "Provides reliable baseline performance and coefficient confidence intervals",
            ],
            "limitations": [
                "Cannot capture non-linear relationships without feature engineering",
                "Assumes feature-target linearity — often violated in thermochemical processes",
                "Sensitive to multicollinearity among process variables",
            ],
            "typical_use_in_domain": "Baseline modelling; interpretable coefficient analysis for H₂ yield factor screening",
        },

        "Lstm": {
            "full_name": "Long Short-Term Memory Network",
            "family": "Recurrent Neural Network / Deep Learning",
            "type": "Supervised Learning",
            "description": (
                "LSTMs are a special type of Recurrent Neural Network (RNN) designed to learn long-range "
                "temporal dependencies in sequential data. They use a gating mechanism (input, forget, and "
                "output gates) to control information flow through the cell state, mitigating the vanishing "
                "gradient problem of standard RNNs. In hydrogen production, LSTMs are applied to dynamic "
                "process modelling, time-series prediction of reactor states, and real-time monitoring "
                "of biohydrogen fermentation batch processes."
            ),
            "strengths": [
                "Captures long-range temporal dependencies in sequential process data",
                "Robust to vanishing gradient — suitable for long time-series",
                "Effective for dynamic modelling of batch fermentation and reactor transients",
            ],
            "limitations": [
                "Data-hungry — requires substantial time-series data for reliable training",
                "Computationally expensive and slow to train",
                "Hyperparameter tuning (hidden units, sequence length) is non-trivial",
            ],
            "typical_use_in_domain": "Dynamic modelling of dark fermentation and electrolysis systems; batch process monitoring",
        },

        "Modified Monod Model (Scipy Optimization)": {
            "full_name": "Modified Monod Kinetic Model with SciPy Optimisation",
            "family": "Mechanistic / Hybrid Model",
            "type": "Kinetic / Semi-empirical Model",
            "description": (
                "The Monod model is a mechanistic kinetic model describing microbial growth rate as a function "
                "of substrate concentration, analogous to Michaelis-Menten enzyme kinetics. In dark fermentation "
                "hydrogen production, the Modified Monod model incorporates inhibition terms (substrate, product, "
                "or pH inhibition) to capture real bioreactor dynamics. SciPy's optimisation routines (e.g., "
                "curve_fit, minimize) are used to fit the model parameters (μmax, Ks, Ki) to experimental "
                "batch or continuous fermentation data."
            ),
            "strengths": [
                "Physically interpretable kinetic parameters grounded in microbiology",
                "Extrapolates more reliably than pure data-driven models",
                "Well-validated framework for biological hydrogen production processes",
            ],
            "limitations": [
                "Requires simplifying assumptions about microbial population dynamics",
                "Parameter estimation can be ill-conditioned for complex inhibition models",
                "Limited applicability to multi-species or syntrophic microbial communities",
            ],
            "typical_use_in_domain": "Kinetic modelling of dark fermentation and photobiological hydrogen production",
        },

        "Multi-Objective Grey Wolf Optimizer": {
            "full_name": "Multi-Objective Grey Wolf Optimizer (MOGWO)",
            "family": "Bio-Inspired / Metaheuristic Optimisation",
            "type": "Multi-Objective Optimisation",
            "description": (
                "MOGWO extends the single-objective Grey Wolf Optimizer (GWO) — a swarm intelligence algorithm "
                "mimicking the social hierarchy and hunting behaviour of grey wolves — to handle multiple "
                "conflicting objectives simultaneously. It maintains a Pareto archive of non-dominated solutions "
                "and uses an external archive with crowding distance to ensure diversity. In hydrogen production "
                "studies, MOGWO can simultaneously optimise H₂ yield and purity, energy efficiency and cost, "
                "or other competing process objectives."
            ),
            "strengths": [
                "Finds a diverse Pareto-optimal front for trade-off analysis",
                "Few hyperparameters compared to NSGA-II or MOEA/D",
                "Effective on non-convex, discontinuous multi-objective landscapes",
            ],
            "limitations": [
                "Convergence speed lower than gradient-based methods for smooth problems",
                "Pareto front quality sensitive to archive size and crowding distance metric",
                "Relatively newer algorithm with less benchmarking in hydrogen production",
            ],
            "typical_use_in_domain": "Multi-objective process optimisation for simultaneous maximisation of H₂ yield and purity",
        },

        "NSGA-II": {
            "full_name": "Non-dominated Sorting Genetic Algorithm II",
            "family": "Evolutionary / Multi-Objective Optimisation",
            "type": "Multi-Objective Optimisation",
            "description": (
                "NSGA-II is one of the most widely used multi-objective evolutionary algorithms. It uses "
                "fast non-dominated sorting to rank solutions into Pareto fronts, and crowding distance "
                "to maintain diversity within each front. Each generation, offspring are created via "
                "crossover and mutation, and the combined parent-offspring population is sorted to retain "
                "the best solutions. In hydrogen production, NSGA-II is used to explore trade-offs between "
                "competing objectives such as H₂ yield vs. energy cost or H₂ production vs. CO₂ emissions."
            ),
            "strengths": [
                "Well-established with extensive literature validation",
                "Produces a well-distributed Pareto front for multi-objective trade-off analysis",
                "Applicable to any objective landscape — no gradient information required",
            ],
            "limitations": [
                "Computationally expensive — requires many objective function evaluations",
                "Performance degrades for more than 3 objectives (use NSGA-III instead)",
                "Stochastic — results vary between runs; requires multiple runs for reliability",
            ],
            "typical_use_in_domain": "Multi-objective optimisation in integrated hydrogen production and carbon capture systems",
        },

        "Not specified": {
            "full_name": "Not Specified",
            "family": "N/A",
            "type": "N/A",
            "description": (
                "The specific ML algorithm(s) used in the study were not explicitly identified in the paper "
                "or could not be extracted from the available metadata. This may occur in review papers that "
                "discuss ML applications broadly without specifying individual algorithms, or in studies where "
                "the methodology section lacks sufficient detail."
            ),
            "strengths": [],
            "limitations": ["Insufficient methodological reporting limits reproducibility and comparability"],
            "typical_use_in_domain": "N/A",
        },

        "Physics-Informed Ml": {
            "full_name": "Physics-Informed Machine Learning (PIML)",
            "family": "Hybrid Neural Network / Physics-Based",
            "type": "Supervised / Physics-Constrained Learning",
            "description": (
                "PIML embeds known physical laws, governing equations, or domain constraints (mass balance, "
                "energy balance, thermodynamic equilibria, reaction kinetics) directly into the ML model "
                "architecture or loss function. Physics-Informed Neural Networks (PINNs) are the most prominent "
                "variant, where partial differential equations appear as additional penalty terms in the training "
                "loss. This ensures predictions remain physically consistent and improves generalisation, "
                "particularly outside the training data range — a critical benefit for hydrogen process "
                "extrapolation scenarios."
            ),
            "strengths": [
                "Physically consistent predictions — satisfies conservation laws and thermodynamic constraints",
                "Superior extrapolation compared to pure data-driven models",
                "Effective with limited experimental data by leveraging physical priors",
            ],
            "limitations": [
                "Requires domain expertise to formulate and implement physical constraints",
                "Training is more complex and computationally demanding than standard NNs",
                "Hard constraints may conflict with noisy experimental data",
            ],
            "typical_use_in_domain": "Thermodynamically consistent H₂ yield prediction; reactor simulation with embedded kinetics",
        },

        "Polynomial Regression": {
            "full_name": "Polynomial Regression",
            "family": "Linear Model (non-linear features)",
            "type": "Supervised Learning",
            "description": (
                "Polynomial Regression extends linear regression by including polynomial feature transformations "
                "(e.g., x², x³, x₁·x₂) as additional inputs, enabling modelling of non-linear relationships "
                "within the linear regression framework. It is interpretable for low-degree polynomials and "
                "often used for Response Surface Methodology (RSM) in experimental design for hydrogen "
                "production optimisation, where second-order response surfaces are fitted to optimise "
                "process variables."
            ),
            "strengths": [
                "Simple extension of linear regression capturing low-order non-linearities",
                "Interpretable for degree-2 (quadratic) models via RSM",
                "Analytically tractable — closed-form solution",
            ],
            "limitations": [
                "Prone to overfitting at high polynomial degrees",
                "Poor extrapolation — oscillates wildly outside training range",
                "Feature space grows rapidly with polynomial degree and number of features",
            ],
            "typical_use_in_domain": "Response Surface Methodology for H₂ production process parameter optimisation",
        },

        "Random Forest": {
            "full_name": "Random Forest",
            "family": "Tree-Based Ensemble (Bagging)",
            "type": "Supervised Learning",
            "description": (
                "Random Forest builds an ensemble of decision trees on bootstrap samples of the training data, "
                "with an additional randomisation: at each split, only a random subset of features (typically "
                "√p for classification, p/3 for regression) is considered. Predictions are averaged across "
                "all trees (regression) or by majority vote (classification). This combination of bagging and "
                "feature randomisation yields a powerful, low-variance model. Random Forest is one of the most "
                "frequently used algorithms in the hydrogen production ML literature due to its robustness and "
                "built-in feature importance."
            ),
            "strengths": [
                "Robust to overfitting — ensemble averaging reduces variance significantly",
                "Built-in feature importance via mean decrease in impurity or permutation importance",
                "Handles mixed feature types and missing data with minimal preprocessing",
            ],
            "limitations": [
                "Less interpretable than single decision trees",
                "Memory intensive for large ensembles and deep trees",
                "Underperforms gradient boosting on many structured tabular datasets",
            ],
            "typical_use_in_domain": "H₂ yield prediction from biomass gasification, pyrolysis, dark fermentation; feature importance analysis",
        },

        "Rl": {
            "full_name": "Reinforcement Learning",
            "family": "Reinforcement Learning",
            "type": "Reinforcement Learning",
            "description": (
                "Reinforcement Learning (RL) trains an agent to make sequential decisions by interacting with "
                "an environment to maximise a cumulative reward signal. The agent learns a policy mapping "
                "states to actions without labelled training data. In hydrogen production, RL is applied to "
                "real-time process control, dynamic optimisation of electrolyser operation, adaptive "
                "scheduling of renewable-powered hydrogen production, and optimising biohydrogen fermentation "
                "feeding strategies."
            ),
            "strengths": [
                "Optimises dynamic, sequential decision-making in a closed-loop manner",
                "Does not require labelled data — learns from environmental interaction",
                "Handles non-stationary environments and process disturbances adaptively",
            ],
            "limitations": [
                "Requires a reliable process simulator or digital twin as the RL environment",
                "Slow convergence — requires many environment interactions",
                "Reward function design is non-trivial and greatly influences learned policy",
            ],
            "typical_use_in_domain": "Real-time electrolyser control; dynamic scheduling of renewable hydrogen systems",
        },

        "SVM": {
            "full_name": "Support Vector Machine",
            "family": "Kernel-Based",
            "type": "Supervised Learning",
            "description": (
                "SVM finds the optimal hyperplane (or non-linear decision boundary via kernel trick) that "
                "maximises the margin between classes (classification) or minimises prediction error within "
                "an ε-insensitive tube (regression — SVR). The kernel function (RBF, polynomial, sigmoid) "
                "maps inputs to a high-dimensional feature space implicitly, enabling non-linear modelling. "
                "SVR is particularly effective for small datasets and is among the most commonly applied "
                "algorithms in the hydrogen production ML literature, often achieving top R² values."
            ),
            "strengths": [
                "Excellent generalisation on small, high-dimensional datasets",
                "Robust to overfitting due to margin maximisation",
                "Flexible non-linear modelling via kernel selection",
            ],
            "limitations": [
                "Computationally expensive for large datasets (O(n²) to O(n³))",
                "Kernel and regularisation hyperparameters (C, γ, ε) require careful tuning",
                "No probabilistic output — does not provide predictive uncertainty natively",
            ],
            "typical_use_in_domain": "H₂ and tar yield prediction from gasification; SCWG output modelling",
        },

        "XGBoost": {
            "full_name": "Extreme Gradient Boosting",
            "family": "Boosting Ensemble",
            "type": "Supervised Learning",
            "description": (
                "XGBoost is an optimised, scalable implementation of gradient boosting that introduces "
                "second-order Taylor expansion of the loss function, L1 and L2 regularisation terms, "
                "column (feature) subsampling, sparse-aware split finding, and parallel tree construction "
                "via block storage. These innovations make it both highly accurate and computationally "
                "efficient. XGBoost is consistently among the top-performing algorithms in hydrogen "
                "production ML studies and Kaggle-style tabular data competitions."
            ),
            "strengths": [
                "State-of-the-art accuracy on tabular data with built-in regularisation",
                "Handles missing values natively via learned default split directions",
                "Supports built-in cross-validation and early stopping",
            ],
            "limitations": [
                "Many hyperparameters — requires systematic tuning (e.g., Bayesian optimisation)",
                "Can overfit small, noisy datasets without careful regularisation",
                "Less efficient than LightGBM on very large datasets",
            ],
            "typical_use_in_domain": "Best-in-class yield prediction for biomass gasification, HTL, and algal biofuel production",
        },
    },

    # =========================================================================
    # SECTION 2: OPTIMIZATION METHODS (Normalised)
    # =========================================================================
    "Optimization_Methods": {

        "Architecture Tuning": {
            "full_name": "Neural Network Architecture Tuning",
            "category": "Hyperparameter Optimisation",
            "description": (
                "Architecture tuning refers to the systematic search for optimal neural network structural "
                "hyperparameters: number of hidden layers, neurons per layer, activation functions, dropout "
                "rates, batch normalisation placement, and connectivity patterns. This is distinct from weight "
                "optimisation (gradient descent) and is typically performed via grid search, random search, or "
                "automated Neural Architecture Search (NAS) methods. In hydrogen production ANN models, "
                "architecture tuning is critical to balance model expressiveness against overfitting on "
                "small experimental datasets."
            ),
            "when_to_use": "When training ANN/LSTM/CNN models where structural decisions strongly affect performance",
            "typical_domain_use": "Optimising ANN architectures for H₂ yield regression with limited experimental data",
        },

        "Battle Royale Optimization": {
            "full_name": "Battle Royale Optimisation (BRO)",
            "category": "Bio-Inspired / Metaheuristic",
            "description": (
                "BRO is a population-based metaheuristic algorithm inspired by the mechanics of battle royale "
                "video games. A population of candidate solutions ('players') are distributed across a search "
                "space ('map'), interact with neighbouring solutions ('combat'), and weaker solutions are "
                "eliminated while survivors adapt by moving towards stronger solutions. A 'safe zone' mechanism "
                "narrows the search region progressively, functioning analogously to exploration-exploitation "
                "balance. BRO has shown competitive performance with PSO and GA on benchmark optimisation "
                "problems and has begun appearing in engineering optimisation contexts."
            ),
            "when_to_use": "As an alternative to PSO or GA for continuous non-linear optimisation problems",
            "typical_domain_use": "Novel metaheuristic used for ML hyperparameter tuning and process condition optimisation",
        },

        "Bayesian Optimization": {
            "full_name": "Bayesian Optimisation",
            "category": "Sequential Model-Based Optimisation",
            "description": (
                "Bayesian Optimisation (BO) is a sequential, model-based strategy for global optimisation of "
                "expensive-to-evaluate black-box functions. It constructs a probabilistic surrogate model "
                "(typically a Gaussian Process) of the objective function and uses an acquisition function "
                "(e.g., Expected Improvement, Upper Confidence Bound) to balance exploration of uncertain "
                "regions with exploitation of promising regions. BO is highly sample-efficient, making it "
                "ideal for ML hyperparameter tuning where each evaluation involves a full model training run, "
                "and for optimising expensive physical hydrogen production experiments."
            ),
            "when_to_use": "When function evaluations are expensive (model training, physical experiments) and sample efficiency is critical",
            "typical_domain_use": "Efficient ML hyperparameter optimisation for H₂ production models; experimental design",
        },

        "Cross Validation": {
            "full_name": "Cross-Validation (Model Selection / Evaluation)",
            "category": "Model Evaluation / Hyperparameter Selection",
            "description": (
                "Cross-validation partitions the available dataset into K folds and iterates K times, each "
                "time training on K-1 folds and evaluating on the held-out fold. The K performance estimates "
                "are averaged to give a low-variance estimate of generalisation performance. K-fold CV (K=5 "
                "or 10) is standard; Leave-One-Out CV (LOOC) is used for very small datasets. In the context "
                "of small experimental hydrogen production datasets (often <100 samples), CV is essential to "
                "obtain reliable performance estimates and to select hyperparameters without overfitting to a "
                "fixed test set."
            ),
            "when_to_use": "Always — especially critical for small experimental datasets (<200 samples)",
            "typical_domain_use": "Model evaluation and hyperparameter selection for H₂ yield regression models",
        },

        "Differential Evolution": {
            "full_name": "Differential Evolution (DE)",
            "category": "Evolutionary / Metaheuristic",
            "description": (
                "DE is a population-based stochastic optimisation algorithm that evolves candidate solutions "
                "by forming trial vectors through differential mutation (adding the scaled difference of two "
                "random population members to a third) and crossover with the current target vector. The trial "
                "vector replaces the target only if it achieves a better objective value (greedy selection). "
                "DE is effective for continuous, non-linear, and non-differentiable optimisation problems. "
                "In hydrogen production, it is used for both ML hyperparameter tuning and direct process "
                "variable optimisation."
            ),
            "when_to_use": "Continuous non-linear optimisation, especially with non-differentiable objectives",
            "typical_domain_use": "ML hyperparameter search; process condition optimisation for H₂ production maximisation",
        },

        "Genetic Algorithm": {
            "full_name": "Genetic Algorithm (GA)",
            "category": "Evolutionary / Metaheuristic",
            "description": (
                "GAs are evolutionary algorithms inspired by Darwinian natural selection. A population of "
                "candidate solutions (encoded as chromosomes) evolves over generations through selection "
                "(fitness-proportionate or tournament), crossover (recombination of parent chromosomes), "
                "and mutation (random perturbation). The population progressively evolves towards higher "
                "fitness (lower objective function value). GAs are widely used in hydrogen production ML "
                "studies for both ML hyperparameter optimisation and for finding optimal process conditions "
                "(temperature, pressure, catalyst loading) that maximise H₂ yield predictions from "
                "trained surrogate models."
            ),
            "when_to_use": "Discrete or mixed (discrete + continuous) search spaces; multi-modal optimisation landscapes",
            "typical_domain_use": "ML hyperparameter tuning; optimal process condition search using ML surrogate models for SCWG and gasification",
        },

        "Grey Wolf Optimizer": {
            "full_name": "Grey Wolf Optimizer (GWO)",
            "category": "Bio-Inspired / Metaheuristic",
            "description": (
                "GWO is a swarm intelligence metaheuristic that mimics the leadership hierarchy and hunting "
                "strategy of grey wolf packs. The population is divided into Alpha (best), Beta, Delta, "
                "and Omega wolves. Alpha, Beta, and Delta guide the search, while Omega wolves follow. "
                "The prey (optimal solution) is encircled and hunted by updating each wolf's position "
                "based on the three best solutions found. GWO has shown competitive performance with "
                "PSO and GA on engineering optimisation benchmarks with fewer hyperparameters."
            ),
            "when_to_use": "Continuous non-linear optimisation; alternative to PSO with simpler parameter setup",
            "typical_domain_use": "Process condition optimisation and ML hyperparameter tuning in hydrogen production",
        },

        "Grid Search": {
            "full_name": "Grid Search (Exhaustive Hyperparameter Search)",
            "category": "Hyperparameter Optimisation",
            "description": (
                "Grid Search exhaustively evaluates all combinations of hyperparameter values defined on a "
                "pre-specified discrete grid. Each combination is typically evaluated via cross-validation "
                "and the combination yielding the best CV score is selected. While guaranteed to find the "
                "best point within the grid, it scales exponentially with the number of hyperparameters "
                "(curse of dimensionality). In hydrogen production ML studies, it is commonly used for "
                "tuning models with a small number of hyperparameters (e.g., SVM: C and γ; Random Forest: "
                "n_estimators and max_depth)."
            ),
            "when_to_use": "Small hyperparameter spaces (<4 parameters); when computational budget allows exhaustive search",
            "typical_domain_use": "SVM and Random Forest hyperparameter tuning for H₂ yield prediction models",
        },

        "MILP + ε‑Constraint": {
            "full_name": "Mixed-Integer Linear Programming with ε-Constraint Method",
            "category": "Mathematical Optimisation / Multi-Objective",
            "description": (
                "MILP is a mathematical programming technique for optimising a linear objective function "
                "subject to linear equality and inequality constraints, where some decision variables are "
                "required to be integers (binary, integer, or continuous). The ε-Constraint method converts "
                "a multi-objective optimisation problem into a series of single-objective problems by keeping "
                "one objective in the objective function and converting the others into inequality constraints "
                "with varying ε bounds. This generates the Pareto front deterministically. Used in "
                "hydrogen production for techno-economic optimisation of integrated energy systems."
            ),
            "when_to_use": "Structured optimisation problems with linear or linearisable objectives and constraints; system design problems",
            "typical_domain_use": "Optimal design of hydrogen production and distribution networks; TEA-driven process optimisation",
        },

        "Multi-Objective Grey Wolf Optimizer": {
            "full_name": "Multi-Objective Grey Wolf Optimizer (MOGWO)",
            "category": "Bio-Inspired / Multi-Objective Metaheuristic",
            "description": (
                "MOGWO is the multi-objective extension of GWO, maintaining a Pareto archive of non-dominated "
                "solutions alongside the standard GWO hunting mechanism. An external archive stores discovered "
                "Pareto-optimal solutions, and crowding distance or grid mechanisms ensure archive diversity. "
                "Leaders (Alpha, Beta, Delta) are selected from the archive based on least-crowded regions "
                "to promote diverse Pareto front coverage. MOGWO finds trade-off solutions for competing "
                "objectives in hydrogen production simultaneously."
            ),
            "when_to_use": "Multi-objective optimisation problems where Pareto trade-off analysis is required",
            "typical_domain_use": "Simultaneous optimisation of H₂ yield and CO₂ emissions; yield vs. energy cost trade-offs",
        },

        "NSGA-II": {
            "full_name": "Non-dominated Sorting Genetic Algorithm II",
            "category": "Evolutionary / Multi-Objective",
            "description": (
                "NSGA-II is a reference multi-objective evolutionary algorithm using fast non-dominated sorting "
                "(O(MN²) where M=objectives, N=population size) to assign Pareto rank to solutions and "
                "crowding distance within each front to maintain diversity. The combined parent-offspring "
                "population of size 2N is sorted and the best N solutions propagated to the next generation. "
                "Binary tournament selection using rank and crowding distance drives evolution. NSGA-II is "
                "particularly appropriate for 2-3 objective hydrogen production optimisation problems."
            ),
            "when_to_use": "2-3 objective multi-objective optimisation; well-studied benchmark problems",
            "typical_domain_use": "Pareto-optimal process design for integrated H₂ production with carbon capture constraints",
        },

        "Novel Random-Based Optimizer": {
            "full_name": "Novel Random-Based Optimizer",
            "category": "Metaheuristic / Stochastic",
            "description": (
                "This refers to newly proposed random-based or stochastic search algorithms presented in "
                "recent research, distinct from established methods like PSO or GA. These algorithms "
                "typically introduce novel mechanisms for balancing exploration and exploitation in the "
                "search space using randomised strategies. In the context of hydrogen production ML studies, "
                "such methods may be proposed as alternatives to traditional optimisers for ML hyperparameter "
                "tuning or process variable optimisation."
            ),
            "when_to_use": "When evaluating novel optimisation strategies; algorithm benchmarking studies",
            "typical_domain_use": "Proposed as competitive alternatives to GA/PSO for H₂ process optimisation",
        },

        "Particle Swarm Optimization": {
            "full_name": "Particle Swarm Optimisation (PSO)",
            "category": "Swarm Intelligence / Metaheuristic",
            "description": (
                "PSO simulates the social behaviour of bird flocking or fish schooling. A swarm of particles "
                "moves through the search space, with each particle updating its velocity based on its "
                "personal best position (cognitive component) and the global best position found by any "
                "particle (social component). The balance between personal memory and social influence is "
                "controlled by cognitive and social coefficients (c₁, c₂) and inertia weight (w). PSO is "
                "widely used in hydrogen production ML studies for both hyperparameter tuning and direct "
                "process condition optimisation, often combined with SVM or ANN surrogate models."
            ),
            "when_to_use": "Continuous non-linear optimisation; widely applicable to ML hyperparameter tuning and process optimisation",
            "typical_domain_use": "SVR hyperparameter tuning; optimal H₂ yield process condition identification for gasification and SCWG",
        },

        "Photoperiod Tuning": {
            "full_name": "Photoperiod Tuning (Light Cycle Optimisation)",
            "category": "Domain-Specific Process Optimisation",
            "description": (
                "Photoperiod tuning refers to the systematic optimisation of light-dark cycle durations for "
                "photobiological hydrogen production processes, such as biophotolysis by microalgae or "
                "photofermentation by purple non-sulphur bacteria. The light period drives photosynthesis "
                "and H₂ evolution, while the dark period may allow recovery of photosynthetic machinery "
                "and nitrogenase activity. Optimal photoperiod (light:dark ratio and cycle duration) "
                "maximises H₂ production rates while minimising biomass damage from photo-inhibition."
            ),
            "when_to_use": "Optimising photobiological hydrogen production systems",
            "typical_domain_use": "Maximising photohydrogen yield in microalgal biophotolysis and photofermentation",
        },

        "Randomized SearchCV": {
            "full_name": "Randomised Search with Cross-Validation",
            "category": "Hyperparameter Optimisation",
            "description": (
                "Randomised SearchCV samples hyperparameter combinations randomly from specified distributions "
                "(or discrete sets) for a fixed number of iterations, evaluating each via cross-validation. "
                "Unlike Grid Search, it does not evaluate all combinations, making it far more efficient for "
                "large or continuous hyperparameter spaces. Research has demonstrated that Randomised Search "
                "finds equally good or better hyperparameter configurations than Grid Search in a fraction of "
                "the computational budget, because not all hyperparameters are equally important to the "
                "objective function."
            ),
            "when_to_use": "Large hyperparameter spaces; continuous hyperparameter ranges; limited computational budget",
            "typical_domain_use": "Efficient hyperparameter tuning for gradient boosting and SVM models in hydrogen production studies",
        },

        "Response Surface Methodology": {
            "full_name": "Response Surface Methodology (RSM)",
            "category": "Statistical Design of Experiments",
            "description": (
                "RSM is a statistical technique that uses a sequence of designed experiments and polynomial "
                "regression models (typically second-order: main effects, interaction terms, and quadratic "
                "terms) to empirically model the relationship between process variables and a response "
                "(output). A central composite design (CCD) or Box-Behnken design (BBD) is commonly used "
                "for the experimental design phase. RSM provides a smooth response surface that can be "
                "analytically optimised to find the combination of process variables maximising H₂ yield. "
                "It is widely used in hydrogen production literature before or alongside ML modelling."
            ),
            "when_to_use": "When a smooth, interpretable, low-dimensional process model is needed for optimisation",
            "typical_domain_use": "Optimising temperature, pressure, pH, and catalyst concentration for maximum H₂ yield",
        },
    },

    # =========================================================================
    # SECTION 3: INTERPRETABILITY METHODS (Normalised)
    # =========================================================================
    "Interpretability_Methods": {

        "Garson's Algorithm (NN weight analysis)": {
            "full_name": "Garson's Algorithm (Neural Network Weight Analysis)",
            "category": "Model-Specific / Neural Network Interpretability",
            "xai_type": "Model-Specific",
            "description": (
                "Garson's Algorithm decomposes the connection weights of a trained feedforward ANN to estimate "
                "the relative importance of each input variable to the output. It partitions the product of "
                "absolute input-hidden and hidden-output weights, normalising contributions across neurons "
                "to yield percentage importance scores summing to 100%. While simple and computationally "
                "trivial, it assumes the magnitude of weights reflects input importance and ignores non-linear "
                "interactions. It has been widely used in early ANN applications to biomass conversion and "
                "hydrogen production."
            ),
            "scope": "Global (dataset-level importance)",
            "data_needed": "Trained ANN weights only",
            "strengths": [
                "Computationally trivial — only trained weights needed",
                "Produces a simple, interpretable ranking of input importance",
                "Historically popular and easy to explain to non-experts",
            ],
            "limitations": [
                "Ignores non-linear interactions between input variables",
                "Weight magnitude ≠ importance in deep or recurrent networks",
                "Superseded by SHAP, LIME, and permutation importance in modern practice",
            ],
        },

        "Gini Importance": {
            "full_name": "Gini Importance (Mean Decrease in Impurity)",
            "category": "Model-Specific / Tree-Based Interpretability",
            "xai_type": "Model-Specific",
            "description": (
                "Gini Importance (also called Mean Decrease in Impurity, MDI) measures the total reduction "
                "in Gini impurity (for classification) or MSE (for regression) achieved by splits on each "
                "feature, summed and averaged across all trees in a forest. Features with higher total "
                "impurity reduction are considered more important. It is computed 'for free' during tree "
                "training — no additional computation required. In hydrogen production Random Forest models, "
                "Gini importance identifies which process variables (temperature, pressure, biomass "
                "composition) most strongly determine H₂ yield."
            ),
            "scope": "Global (dataset-level importance)",
            "data_needed": "Trained Random Forest / tree ensemble",
            "strengths": [
                "Zero additional computation cost — importance is a byproduct of training",
                "Provides global feature ranking across the entire forest",
                "Simple to interpret and communicate",
            ],
            "limitations": [
                "Biased towards high-cardinality and continuous features",
                "Not invariant to feature correlations — correlated features share importance",
                "Can be misleading for datasets with many irrelevant or noisy features",
            ],
        },

        "Grey Relational Analysis + Shapley Values": {
            "full_name": "Grey Relational Analysis (GRA) combined with Shapley Values",
            "category": "Hybrid / Multi-Method Interpretability",
            "xai_type": "Hybrid (statistical + game-theoretic)",
            "description": (
                "Grey Relational Analysis (GRA) is a method from Grey System Theory that quantifies the "
                "degree of similarity between reference and comparator sequences using a relational grade "
                "(0–1 scale), capturing the closeness of factor-output relationships even with incomplete "
                "information. Shapley Values (from cooperative game theory, implemented via SHAP) assign "
                "each feature a contribution value equal to its average marginal contribution across all "
                "possible feature coalitions. Combining GRA with Shapley Values provides both global "
                "statistical correlation (GRA) and model-agnostic, theoretically grounded importance "
                "(SHAP) for comprehensive interpretability."
            ),
            "scope": "Global (both methods)",
            "data_needed": "Dataset + trained ML model",
            "strengths": [
                "Dual-perspective interpretability — statistical correlation plus model-agnostic attribution",
                "GRA handles incomplete/uncertain data scenarios common in experimental studies",
                "SHAP provides consistent, theoretically grounded feature attributions",
            ],
            "limitations": [
                "Requires expertise in both methods",
                "SHAP computational cost can be high for tree-based models with many features",
                "GRA relational grades are not directly comparable to SHAP values",
            ],
        },

        "Individual Conditional Expectation (ICE)": {
            "full_name": "Individual Conditional Expectation (ICE) Plots",
            "category": "Model-Agnostic / Visualisation",
            "xai_type": "Post-hoc, Model-Agnostic",
            "description": (
                "ICE plots visualise how the predicted output of a model changes as a single feature is "
                "varied across its range, holding all other features fixed at their observed values for "
                "each individual data point. Unlike PDPs (which show the average effect), ICE plots show "
                "one line per sample, revealing heterogeneous feature effects and interactions hidden by "
                "averaging. In hydrogen production models, ICE plots can reveal whether the effect of "
                "temperature on H₂ yield differs across different feedstock types or initial pressures."
            ),
            "scope": "Local + Global (individual lines + overall pattern)",
            "data_needed": "Trained ML model + dataset for prediction",
            "strengths": [
                "Reveals individual-level heterogeneity in feature effects",
                "Detects feature interactions hidden by PDP averaging",
                "Model-agnostic — applicable to any ML model",
            ],
            "limitations": [
                "Visual interpretation becomes cluttered with many samples",
                "Does not account for feature correlation — may evaluate unrealistic feature combinations",
                "Provides less aggregated insight than SHAP for overall feature importance ranking",
            ],
        },

        "Partial Dependence Plots (PDP)": {
            "full_name": "Partial Dependence Plots (PDP)",
            "category": "Model-Agnostic / Visualisation",
            "xai_type": "Post-hoc, Model-Agnostic",
            "description": (
                "PDPs show the marginal effect of one or two features on the predicted outcome of an ML model, "
                "averaging out the influence of all other features by integrating over their empirical "
                "distribution. They reveal the direction (positive/negative) and shape (linear, monotone, "
                "non-linear) of feature-output relationships across the feature range. Two-way PDPs can "
                "visualise interaction effects between pairs of features. In hydrogen production studies, "
                "PDPs are widely used alongside SHAP to explain which process variables drive H₂ yield "
                "predictions and how their effects operate."
            ),
            "scope": "Global (marginal effect averaged over dataset)",
            "data_needed": "Trained ML model + dataset for marginalisation",
            "strengths": [
                "Intuitive visualisation of feature-response relationships",
                "Model-agnostic — works with any ML algorithm",
                "Two-way PDPs reveal interaction effects",
            ],
            "limitations": [
                "Averaging can hide heterogeneous effects and interactions — use ICE plots alongside PDPs",
                "Assumes feature independence during marginalisation — misleading under correlation",
                "Computationally expensive for two-way PDPs with many features",
            ],
        },

        "Pearson Correlation": {
            "full_name": "Pearson Correlation Coefficient",
            "category": "Statistical / Feature Analysis",
            "xai_type": "Pre-model / Statistical",
            "description": (
                "Pearson Correlation measures the linear dependence between two continuous variables, yielding "
                "a coefficient r ∈ [-1, +1] where +1 indicates perfect positive linear correlation, -1 "
                "perfect negative, and 0 no linear relationship. In hydrogen production ML pipelines, "
                "Pearson correlation matrices are used as a pre-modelling interpretability step: identifying "
                "highly correlated input features (multicollinearity), selecting informative features "
                "correlated with H₂ yield, and understanding pairwise relationships between process "
                "variables (temperature, pressure, feedstock composition)."
            ),
            "scope": "Global (pairwise dataset-level statistic)",
            "data_needed": "Dataset only — no trained model required",
            "strengths": [
                "Simple, fast, and universally understood",
                "No model training required — pure data analysis",
                "Useful for multicollinearity screening before modelling",
            ],
            "limitations": [
                "Captures only linear relationships — misses non-linear dependencies",
                "Sensitive to outliers in small experimental datasets",
                "Does not provide model-level attribution — does not reflect model behaviour",
            ],
        },

        "SHAP (SHapley Additive Explanations)": {
            "full_name": "SHAP (SHapley Additive Explanations)",
            "category": "Model-Agnostic / Game-Theoretic",
            "xai_type": "Post-hoc, Model-Agnostic",
            "description": (
                "SHAP is a unified framework for interpreting ML model predictions grounded in cooperative "
                "game theory. Each feature's SHAP value represents its average marginal contribution to "
                "the model output across all possible subsets (coalitions) of features. SHAP satisfies "
                "desirable axioms: efficiency (SHAP values sum to prediction − expected value), symmetry, "
                "dummy (zero contribution for irrelevant features), and additivity. TreeSHAP provides "
                "exact, efficient computation for tree-based models (O(TLD²) where T=trees, L=leaves, "
                "D=depth). In hydrogen production research, SHAP is the gold standard for explaining "
                "which process variables drive individual H₂ yield predictions."
            ),
            "scope": "Both Local (per-sample) and Global (aggregated importance)",
            "data_needed": "Trained ML model + dataset for marginalisation",
            "strengths": [
                "Theoretically grounded — satisfies game-theoretic fairness axioms",
                "Both local (individual prediction) and global (feature importance) explanations",
                "TreeSHAP provides exact values for tree ensembles without sampling approximation",
                "Rich visualisations: summary plots, waterfall plots, beeswarm plots, dependence plots",
            ],
            "limitations": [
                "KernelSHAP (model-agnostic) is computationally expensive for large datasets",
                "SHAP values can be unstable for highly correlated features",
                "Interaction SHAP values require additional computation",
            ],
        },

        "Sensitivity Analysis": {
            "full_name": "Sensitivity Analysis",
            "category": "Model-Agnostic / Process Analysis",
            "xai_type": "Post-hoc",
            "description": (
                "Sensitivity Analysis (SA) systematically studies how variation in a model's input variables "
                "propagates to variation in its output. Local SA (one-at-a-time, OAT) perturbs one input at "
                "a time around a nominal point and measures the output change. Global SA (Sobol, Morris) "
                "explores the entire input space and decomposes output variance among inputs. In hydrogen "
                "production ML models, SA identifies the most influential process parameters (temperature, "
                "pressure, equivalence ratio) and quantifies their relative impact on H₂ yield predictions, "
                "guiding experimental design and process control priorities."
            ),
            "scope": "Global (variance-based) or Local (point-based)",
            "data_needed": "Trained ML model (or any model) + input ranges",
            "strengths": [
                "Applicable to any model type — ML, mechanistic, or hybrid",
                "Provides both ranking and quantitative contribution of input variables",
                "Global SA (Sobol) decomposes variance and captures interaction effects",
            ],
            "limitations": [
                "Local OAT SA misses global effects and interactions",
                "Variance-based global SA requires many model evaluations (computationally expensive)",
                "Assumes inputs are independent — misleading under strong feature correlations",
            ],
        },

        "Sobol Sensitivity Analysis": {
            "full_name": "Sobol Sensitivity Analysis (Variance-Based Global SA)",
            "category": "Statistical / Global Sensitivity Analysis",
            "xai_type": "Post-hoc, Model-Agnostic",
            "description": (
                "Sobol Sensitivity Analysis is a variance-based global sensitivity method that decomposes "
                "the total output variance into contributions from individual inputs (first-order Sobol "
                "index, Sᵢ) and their interactions (total-order index, Sᵢᵀ). It uses Monte Carlo sampling "
                "or quasi-Monte Carlo sequences (Saltelli sampling) to estimate indices with minimal model "
                "evaluations. Sᵢ captures the fraction of output variance due to input Xᵢ alone; Sᵢᵀ "
                "includes all higher-order interaction effects involving Xᵢ. It is particularly valuable "
                "for hydrogen production models to identify and rank the influence of process variables "
                "including interaction effects."
            ),
            "scope": "Global (full input space variance decomposition)",
            "data_needed": "Trained ML model (or any model) + input probability distributions",
            "strengths": [
                "Rigorous variance decomposition — quantifies both individual and interaction effects",
                "Applicable to non-linear, non-monotonic functions",
                "Model-agnostic — treats the model as a black box",
            ],
            "limitations": [
                "Requires 100s–1000s of model evaluations — impractical for computationally expensive models",
                "Assumes statistically independent inputs — invalid under multicollinearity",
                "Interpretation requires understanding of variance-based sensitivity framework",
            ],
        },

        "Statistical Metrics (MSE, MAE)": {
            "full_name": "Statistical Performance Metrics (MSE, MAE, RMSE, R²)",
            "category": "Model Evaluation / Indirect Interpretability",
            "xai_type": "Indirect / Evaluative",
            "description": (
                "Statistical metrics including Mean Squared Error (MSE), Mean Absolute Error (MAE), Root "
                "Mean Squared Error (RMSE), and the coefficient of determination (R²) quantify the "
                "predictive accuracy of ML models. While not interpretability methods in the XAI sense, "
                "these metrics are used in hydrogen production studies to evaluate how well models capture "
                "the underlying process behaviour and to compare competing models. R² measures the fraction "
                "of variance in H₂ yield explained by the model; MAE provides the average absolute "
                "prediction error in original units (e.g., mmol/L or mL/g)."
            ),
            "scope": "Global (dataset-level model evaluation)",
            "data_needed": "Model predictions + ground truth values",
            "strengths": [
                "Universal, easy to compute and communicate",
                "Enable direct comparison across different ML models and studies",
                "MAE and RMSE are in interpretable original units of the target variable",
            ],
            "limitations": [
                "Do not explain why the model makes specific predictions",
                "MSE/RMSE are sensitive to outliers — may not reflect typical performance",
                "R² can be misleadingly high in interpolation without testing extrapolation",
            ],
        },

        "Surrogate Trees": {
            "full_name": "Surrogate Decision Trees (Global Surrogate Models)",
            "category": "Model-Agnostic / Global Surrogate",
            "xai_type": "Post-hoc, Model-Agnostic",
            "description": (
                "A surrogate tree is a simple, interpretable decision tree trained to approximate the "
                "predictions of a complex black-box model (e.g., XGBoost, ANN, Random Forest). The "
                "black-box model generates predictions on a large set of input samples, and a shallow "
                "decision tree is fitted to these predictions. The tree provides a globally interpretable "
                "approximation of the black-box decision logic through human-readable if-then rules. "
                "In hydrogen production ML, surrogate trees translate opaque ensemble model behaviour "
                "into actionable process rules (e.g., 'if temperature > 650°C and pressure > 25 MPa, "
                "H₂ yield exceeds 35 mol/kg biomass')."
            ),
            "scope": "Global (approximate explanation of the full model behaviour)",
            "data_needed": "Trained black-box model + dataset for generating pseudo-labels",
            "strengths": [
                "Produces human-readable decision rules from black-box models",
                "Fully model-agnostic — applicable to any ML algorithm",
                "Single tree visualisation is highly communicable to domain experts",
            ],
            "limitations": [
                "Fidelity of surrogate tree to the original model is limited — approximation errors",
                "Shallow trees may oversimplify complex non-linear model behaviour",
                "Does not provide local (per-sample) explanations — LIME or SHAP needed for local XAI",
            ],
        },
    },
}


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_algorithm_info(algorithm_name: str) -> dict:
    """Retrieve detailed info for a specific ML algorithm."""
    return ML_METHODS_DICTIONARY["ML_Algorithms"].get(algorithm_name, {})


def get_optimization_info(method_name: str) -> dict:
    """Retrieve detailed info for a specific optimisation method."""
    return ML_METHODS_DICTIONARY["Optimization_Methods"].get(method_name, {})


def get_interpretability_info(method_name: str) -> dict:
    """Retrieve detailed info for a specific interpretability method."""
    return ML_METHODS_DICTIONARY["Interpretability_Methods"].get(method_name, {})


def list_all_methods() -> dict:
    """Return a summary of all methods covered in the dictionary."""
    return {
        "ML_Algorithms": sorted(ML_METHODS_DICTIONARY["ML_Algorithms"].keys()),
        "Optimization_Methods": sorted(ML_METHODS_DICTIONARY["Optimization_Methods"].keys()),
        "Interpretability_Methods": sorted(ML_METHODS_DICTIONARY["Interpretability_Methods"].keys()),
    }


def search_by_family(family: str) -> list:
    """Return all ML algorithms belonging to a given family."""
    return [
        name for name, info in ML_METHODS_DICTIONARY["ML_Algorithms"].items()
        if family.lower() in info.get("family", "").lower()
    ]


# =============================================================================
# QUICK DEMO (run this file directly to verify)
# =============================================================================
if __name__ == "__main__":
    import json

    print("=" * 70)
    print("ML METHODS DICTIONARY — HYDROGEN PRODUCTION FROM WASTES")
    print("=" * 70)
    summary = list_all_methods()
    for section, methods in summary.items():
        print(f"\n{section} ({len(methods)} entries):")
        for m in methods:
            print(f"  - {m}")

    print("\n" + "=" * 70)
    print("EXAMPLE LOOKUP: SHAP")
    print("=" * 70)
    print(json.dumps(get_interpretability_info("SHAP (SHapley Additive Explanations)"), indent=2))

    print("\n" + "=" * 70)
    print("EXAMPLE LOOKUP: XGBoost")
    print("=" * 70)
    print(json.dumps(get_algorithm_info("XGBoost"), indent=2))

    print("\n" + "=" * 70)
    print("BOOSTING ENSEMBLE FAMILY MEMBERS:")
    print("=" * 70)
    print(search_by_family("Boosting"))
