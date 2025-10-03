# Checkpoint 1: Data Gathering, KPIs

## Data Gathering
- **EPA walkability index**
  - [cancer.gov](https://gis.cancer.gov/research/files.html) based on EPA data
    - [Codebook](https://gis.cancer.gov/research/WalkIndex_Codebook.pdf) (explains each feature)
    - [.csv census tract 2019](https://gis.cancer.gov/research/WalkabilityIndex_Tract_2019.csv)
  - [EPA](https://catalog.data.gov/dataset/walkability-index8)
    - We mainly use 2019 census tract data, which uses the **year = 2018** survey for our analysis. The EPA walkability index is  calculated using four major factors:
      1. Street intersection density (pedestrian-oriented intersections). This variable was calculated as a weighted sum of different intersection types, with zero weight for automobile-oriented intersections and lower weights for 3- vs. 4-way intersections: directly correlated to walkability  
      2. The mix of employment types and occupied housing: directly correlated to walkability
      3. The mix of employment types  (such as retail, office, or industrial): directly correlated to walkability
      4. Distance from the population-weighted centroid to nearest transit stop (meters): indirectly correlated to walkability
- Health data [PLACES and 500 CITIES: Data Dictionary](https://data.cdc.gov/500-Cities-Places/PLACES-and-500-Cities-Data-Dictionary/m35w-spkz/data_preview)
  - There are multiple PLACES data sets since the project took place almost every year. Each project is based on BRFSS measures collected in previous years. Since Walkability is based on **year = 2018**, we should be using the PLACES dataset that uses measures from 2018. It appears that PLACES 2020 is the project that utilizes measures taken in 2018 the most. Therefore, in my opinion, we should use this one so that all our datasets include the year 2018.
  - The health dataset we are using [CDC PLACES 2020]([https://data.cdc.gov/500-Cities-Places/PLACES-Census-Tract-Data-GIS-Friendly-Format-2021-/mb5y-ytti/about_data](https://data.cdc.gov/500-Cities-Places/PLACES-Census-Tract-Data-GIS-Friendly-Format-2020-/ib3w-k9rq/about_data)) is based on a predictive model taking demographics into account (see [model description](https://www.cdc.gov/places/methodology/index.html#:~:text=PLACES%20methodology,census%20tract%2C%20and%20ZCTA%20levels.)). For each measure, the CDC PLACES dataset provides a 95 % confidence interval. This matters for the two reasons below (mentioned in [The Use of Small Area Estimates in Place-Based Health Research](https://pmc.ncbi.nlm.nih.gov/articles/PMC7204458/)):
    1. We may not include demographic features in our regression (see [CDC PLACES FAQ](https://www.cdc.gov/places/faqs/using-data/index.html?utm_source=chatgpt.com)),
    2. Our outcome is noisy (with known confidence intervals), so we need to take this into account in our approach. The following papers provide some guidance for this scenario:
      - [Estimating Regression Models in Which the Dependent Variable Is Based on Estimates](https://www.jstor.org/stable/pdf/25791822.pdf?casa_token=N0BnCWKeyXEAAAAA:zpUTCEulSLZaUusXK78zRF6oIMlStssy-Q8E0MgtPalPAsdhX10pAM3BlexT-Dgp9ZuE3HSiKWeZGZNoF_d4tcJ_tTp8Q57ZVxYtY0znSW3Ewu38Xod2zA)
      - [Usage of an estimated coefficient as a dependent variable](https://www.sciencedirect.com/science/article/pii/S0165176512001231)
- Demographics  
  - [census.gov](https://www.census.gov/programs-surveys/acs/data.html?utm_source=chatgpt.com) (Maryam)  
    I created a Python script to fetch ACS data using the Census API. We had discussed including features such as age, employment, and education. Since there are many other possible features, I decided to start with some basic ones. Specifically, I included: “ % unemployed, % below poverty level, % population over 65, % population with a bachelor’s degree or higher, % commuting by public transportation, % commuting by car ” All features are at the tract level, and I also added a column with the tract-level GEOID (constructed using the state \+ county \+ tract IDs). Attached are the Python script and the initial draft of the CSV data.
  - Based on Maryam's script, I am adding the **years = 2018** and **year = 2019**.

## Data Assessment

- **Volume and coverage**  
  * Is there enough data to support modeling?  
- **Granularity**  
  * Does the level of detail match the unit of analysis?  
- **Bias and representativeness**  
  * Consider missing subpopulations and selection bias.

## Assessing Learnability

- **Signal vs. noise**  
  * Do the features plausibly contain information about the target?  
- **Data sufficiency**  
  * Are there enough examples overall and per class?  
  * For time series, do you have enough cycles to capture seasonality or trends?  
- **Feature-target alignment**  
  * Are features actually available at prediction time (avoid leakage)?  
  * Do you have variables that could plausibly explain the target? I suppose this may actually be an issue, as the PLACES data set is a model based on demographic data. If we include Demographics, then features may indeed explain the target. I am not sure how we will account for this.  
- **Back-of-the-envelope model test**  
  - Quickly fit some models without investing too much work:  
    - Include very basic cleaning and imputation in your pipelines (so that the models can actually run), but no feature selection or engineering.  
    - Trivial Baselines  
      - [DummyRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyRegressor.html)  
      - [DummyClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html)  
    - Linear Models  
      - [LogisticRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html)  
      - [LinearRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html)  
    - Tree-Based Models  
      - [RandomForestClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)  
      - [RandomForestRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html)  
  - Always evaluate with **cross-validation**:  
    - [KFold](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.KFold.html)  
    - [cross\_val\_score](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_val_score.html)  
  - If performance is indistinguishable from trivial baselines across folds, the problem may not be learnable with the current data.  
- **Domain sanity check**  
  - Ask subject experts whether the target is realistically predictable given the inputs.

## KPI Definition (Key Performance Indicators)

- **Primary KPI**  
  - What metric directly reflects project success? (e.g., RMSE?, accuracy, F1, uplift).  
- **Secondary KPIs**  
  - Capture trade-offs: precision vs. recall, fairness metrics, latency, cost.  
- **Baseline definition**  
  - Use the same models as your Back-of-the-Envelope model test but record both primary and secondary KPIs now that you have defined them.
  
## Deliverables

- **Written / Conceptual**  
    
  - A **data audit summary**: key distributional facts, missingness, correlations.  
  - A **list of dropped features** with justification (low information, leakage, redundancy, irrelevance).  
  - A **list of engineered features** with rationale (domain knowledge, lags, interactions, transformations).


- **Code / Repo Artifacts**  
    
  - **`notebooks/eda.ipynb`**:  
    - Visualizations and descriptive stats.  
    - Missingness analysis.  
    - Correlation heatmaps, scatterplots, outlier checks.  
    - Exploratory lag analysis (ACF/PACF, lag vs. target plots).  
  - **`notebooks/feature_selection.ipynb`**:  
    - Shows feature elimination decisions (variance threshold, correlation pruning, leakage checks).  
    - Logs results in a table (`results/feature_selection.csv`).  
  - **`src/features/transformers.py`**:  
    - Custom transformers implementing engineered features (e.g., lag features, ratios, domain-driven encodings).  
  - **`src/features/preprocessing.py`**:  
    - Main preprocessing pipeline that drops unused features, integrates engineered features, and can be reused in modeling.  
  - **`notebooks/pipeline_demo.ipynb`**:  
    - Demonstrates the pipeline fitting/transforming data.  
  - **`results/eda/` folder**:  
    - Key plots saved as `.png` or `.html`.  
  - **Updated schema** (`schema.json` or `schema.yaml`):  
    - Defines available features, their types, and any transformations applied.  
  - **(Optional) Tests in `tests/test_pipeline.py`**:  
    - Verify engineered features are generated correctly.  
    - Ensure pipeline respects train/test splits (no future leakage).
