# Checkpoint 1: Problem Definition, Data Gathering, KPIs

## Problem Definition

* **Question:**  
  To what extent does the EPA walkability index (and its components, see below) impact the following factors in a given US “census tract” (see [definition](https://www.census.gov/programs-surveys/geography/about/glossary.html#par_textimage_13) \~ 1,200 and 8,000 people):  
  * Obesity proportion  
  * Mental health  
  * Diabetes  
  * Hypertension  
  * Stroke rate  
  * ???

Components of the EPA walkability index:

* [Short version](https://gis.cancer.gov/research/WalkIndex_Methods.pdf)  
  * [Long version](https://www.epa.gov/sites/default/files/2021-06/documents/national_walkability_index_methodology_and_user_guide_june2021.pdf)

* **What decision or action will this analysis inform?**  
  This will support decisions to implement walkability improvements in a given census tract.

* **Who are the stakeholders and what do they care about?**  
  Public health departments, policymakers, city planners, health insurance providers, ???

* **Specify the unit of analysis.**  
  * Unit \= individual US census tract (in the year 2019? 2020? More years?)  
  * Features \= EPA walkability index (and its components)  
  * Outcome \= health outcomes (Obesity, MH, Diabetes, Hypertension, Stroke, ???)  
  * Weight \= Should we weight each census tract by its population?  
  * Other essential features \= demographics (age, sex, education, ???)

* **Define the scope and boundaries.**  
  * Time horizon: 2019? 2020? More years?  
  * Geographic region: US  
  * Population: information at census tract level (no individual info)  
  * Excluded feature: ???

* **Identify anti-goals**  
  * Our project will not address …???

## Data Gathering

* EPA walkability index  
  * [cancer.gov](https://gis.cancer.gov/research/files.html) based on EPA data  
    * [Codebook](https://gis.cancer.gov/research/WalkIndex_Codebook.pdf) (explains each feature)  
    * [.csv census tract 2019](https://gis.cancer.gov/research/WalkabilityIndex_Tract_2019.csv)  
    * [.csv census tract 2013](https://gis.cancer.gov/research/WalkIndex_USTracts.csv)  
  * [EPA](https://catalog.data.gov/dataset/walkability-index8)  
    * We mainly use 2019 census tract data which uses the 2018 survey for our analysis. The EPA walkability index calculated using four major factors:  
1. Street intersection density (pedestrian-oriented intersections). This variable was calculated as a weighted sum of different intersection types with zero weight for automobile oriented intersections and lower weights for 3- vs. 4-way intersections: directly correlated to walkability  
2. The mix of employment types and occupied housing: directly correlated to walkability

   

3. The mix of employment types  (such as retail, office or industrial): directly correlated to walkability

   

4. Distance from the population-weighted centroid to nearest transit stop (meters): indirectly correlated to walkability

   

 


* Health data [CDC 500 Cities & Places](https://data.cdc.gov/browse?q=&sortBy=relevance&pageSize=20&category=500+Cities+%26+Places&page=1)

  * For each year, there is:  
    * One wide format is used for tract-level, city-level, and county-level data. Each census tract (or city or county, depending on the level chosen) is assigned to a unique row, and a specific column is allocated to each type of measurement. This seems better for our analysis.  
    * One long format: each row is a given measurement (e.g., obesity rate) in a given census tract. In particular, a given census tract may appear on multiple rows if different measurements were made on it (e.g., obesity, cancer rate, etc.). This could be useful in some instances if we want to remove all the measurements under a specific value without having to do it column by column. It is possible to convert this long format to a wide format later on.

  * Important:  
    * **Every data point is a model-based estimate**. In practice, given a tract census, we would only know certain people are obese, while others are not. The model infers the measurement of the entire census tract based on this smaller sample. **The database contains confidence intervals for each measurement**, corresponding to each census tract.

      Ref:  
      * [Estimating Regression Models in Which the Dependent Variable Is Based on Estimates](https://www.jstor.org/stable/pdf/25791822.pdf?casa_token=N0BnCWKeyXEAAAAA:zpUTCEulSLZaUusXK78zRF6oIMlStssy-Q8E0MgtPalPAsdhX10pAM3BlexT-Dgp9ZuE3HSiKWeZGZNoF_d4tcJ_tTp8Q57ZVxYtY0znSW3Ewu38Xod2zA)  
      * [Usage of an estimated coefficient as a dependent variable](https://www.sciencedirect.com/science/article/pii/S0165176512001231)

    * Do I need to adjust for age, sex, and race/ethnicity in a model that examines the association of area-level factors (e.g., park accessibility in the neighborhood) with a measure estimated in PLACES? [FAQ](https://www.cdc.gov/places/faqs/using-data/index.html?utm_source=chatgpt.com)

      “If researchers choose to include adjustments for area-level demographic characteristics in an analysis using model-based PLACES estimates, caution should be taken when interpreting results. The PLACES approach incorporates age, race or ethnicity, sex, education, and poverty to generate the model-based estimates. This approach should be considered when planning, conducting, and interpreting any regression analyses using the model-based PLACES estimates.”

      Ref: [The Use of Small Area Estimates in Place-Based Health Research](https://pmc.ncbi.nlm.nih.gov/articles/PMC7204458/) See the part “Other Considerations in particular”

  * [Census tract 2019 (wide format)](https://data.cdc.gov/d/k86t-wghb) **public**  
    This dataset includes model-based estimates for 27 measures from 2016 and 2017\. Data sources used to generate these measures include the Behavioral Risk Factor Surveillance System (BRFSS) data (2017, 2016), 2010 Census population data from the Census Bureau, and American Community Survey (ACS) estimates for 2013-2017 and 2012-2016.

    Praniti: PS, there is another dataset: [Census tract 2020](https://data.cdc.gov/500-Cities-Places/PLACES-Census-Tract-Data-GIS-Friendly-Format-2020-/ib3w-k9rq/about_data): uses 2018 BRFSS data for 23 measures and 2017 BRFSS data for 4 measures (high blood pressure, taking high blood pressure medication, high cholesterol, and cholesterol screening). Four measures are based on the 2017 BRFSS data because the relevant questions are only asked every other year in the BRFSS.

  * [Census tract 2022 (wide format)](https://dev.socrata.com/foundry/data.cdc.gov/shc3-fzig) **public**  
    This dataset contains model-based census tract-level estimates. Data sources used to generate these model-based estimates include the 2020 or 2019 Behavioral Risk Factor Surveillance System (BRFSS) data, 2010 Census Bureau population estimates, and American Community Survey (ACS) estimates from 2015 to 2019\.  
  * [Census tract 2024 (wide format)](https://data.cdc.gov/500-Cities-Places/PLACES-Census-Tract-Data-GIS-Friendly-Format-2024-/yjkw-uj5s/about_data) **public**  
    This dataset contains model-based estimates of census tracts. The data sources used to generate these model-based estimates include the 2022 or 2021 Behavioral Risk Factor Surveillance System (BRFSS) data, the 2020 Census Bureau population data, and American Community Survey estimates from 2018 to 2022\.

* Demographics  
  * [census.gov](https://www.census.gov/programs-surveys/acs/data.html?utm_source=chatgpt.com) (Maryam)  
    I created a Python script to fetch ACS data using the Census API. We had discussed including features such as age, employment, and education. Since there are many other possible features, I decided to start with some basic ones. Specifically, I included: “ % unemployed, % below poverty level, % population over 65, % population with a bachelor’s degree or higher, % commuting by public transportation, % commuting by car ” All features are at the tract level, and I also added a column with the tract-level GEOID (constructed using the state \+ county \+ tract IDs). Attached are the Python script and the initial draft of the CSV data.

* **Acquisition strategy**  
  * One-time download vs. automated pipeline.  
  * Handling rate limits or access restrictions.  
* **Documentation of provenance**  
  * Record URLs, API calls, and database queries.  
  * Save raw data before transformations.  
* **Ethical and legal considerations**  
  * Licensing, privacy concerns, and handling sensitive data.

## Data Assessment

* **Volume and coverage**  
  * Is there enough data to support modeling?  
* **Granularity**  
  * Does the level of detail match the unit of analysis?  
* **Bias and representativeness**  
  * Consider missing subpopulations and selection bias.

## Assessing Learnability

* **Signal vs. noise**  
  * Do the features plausibly contain information about the target?  
* **Data sufficiency**  
  * Are there enough examples overall and per class?  
  * For time series, do you have enough cycles to capture seasonality or trends?  
* **Feature-target alignment**  
  * Are features actually available at prediction time (avoid leakage)?  
  * Do you have variables that could plausibly explain the target? I suppose this may actually be an issue, as the PLACES data set is a model based on demographic data. If we include Demographics, then features may indeed explain the target. I am not sure how we will account for this.  
* **Back-of-the-envelope model test**  
  * Quickly fit some models without investing too much work:  
    * Include very basic cleaning and imputation in your pipelines (so that the models can actually run), but no feature selection or engineering.  
    * Trivial Baselines  
      * [DummyRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyRegressor.html)  
      * [DummyClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html)  
    * Linear Models  
      * [LogisticRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html)  
      * [LinearRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html)  
    * Tree-Based Models  
      * [RandomForestClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)  
      * [RandomForestRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html)  
  * Always evaluate with **cross-validation**:  
    * [KFold](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.KFold.html)  
    * [cross\_val\_score](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_val_score.html)  
  * If performance is indistinguishable from trivial baselines across folds, the problem may not be learnable with the current data.  
* **Domain sanity check**  
  * Ask subject experts whether the target is realistically predictable given the inputs.

## KPI Definition (Key Performance Indicators)

* **Primary KPI**  
  * What metric directly reflects project success? (e.g., RMSE?, accuracy, F1, uplift).  
* **Secondary KPIs**  
  * Capture trade-offs: precision vs. recall, fairness metrics, latency, cost.  
* **Baseline definition**  
  * Use the same models as your Back-of-the-Envelope model test but record both primary and secondary KPIs now that you have defined them.

## Deliverables

* **`README.md`**: Contains the written problem statement and links to notebooks/scripts.  
* **`data_inventory.csv` or `data_inventory.md`**: Tabular list of data sources, access methods, licensing, limitations. Should be generated or updated by scripts when possible.  
* **Data acquisition scripts** in `src/data/`: One-off downloads, API calls, scraping scripts, or database query files. Each should log provenance (URLs, queries, timestamps).  
* **Raw data snapshot** in `data/raw/`: A small immutable sample, or instructions for secure download if too large/sensitive.  
* **Baseline modeling notebook** in `notebooks/baseline.ipynb`:  
  * Implements trivial, linear, and tree-based baselines.  
  * Evaluates with cross-validation.  
  * Reports both primary and secondary KPIs in a table.  
* **KPI definition file** (`kpis.md`): Explicit metrics, formulas, and improvement directions.  
* **Environment specification** (`environment.yml` or `requirements.txt`): Reproducible package list including `pandas`, `numpy`, `scikit-learn`, and any acquisition libraries used.  
* **(Optional) Provenance log** in `logs/`: Script-generated record of data pulls (timestamps, queries, file hashes, rate-limit notes).

Note: Treat these as suggestions rather than demands. Not all of these deliverables will make sense for all teams. For example, if your data is a single dataframe sourced from Kaggle you will not need to have `data_inventory.csv`:  you can just link to the data source in the project README.



# Checkpoint 2 Guide: EDA, Feature Selection, and Feature Engineering

## Exploratory Data Analysis (EDA)

- **Understand distributions**  
    
  - Inspect univariate distributions (histograms, KDEs, boxplots).


- **Check for missing data**  
    
  - Quantify missingness, visualize patterns.  
  - Tools:  
    - [`pandas.isna`](https://pandas.pydata.org/docs/reference/api/pandas.isna.html)  
    - [`missingno`](https://github.com/ResidentMario/missingno) (matrix, heatmap, dendrogram visualizations)


- **Relationships between variables**  
    
  - Scatterplots, correlation heatmaps, group summaries.


- **Outlier detection**  
    
  - Identify points that may distort modeling.  
  - Tools:  
    - [`scipy.stats.zscore`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.zscore.html)  
    - [`sklearn.ensemble.IsolationForest`](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)  
    - Boxplots via [`seaborn.boxplot`](https://seaborn.pydata.org/generated/seaborn.boxplot.html)


- **Time-series and lag structure**  
    
  - Create exploratory lag features *in a notebook only* to inspect autocorrelation, partial autocorrelation, or lag-target scatterplots.  
  - Tools:  
    - [`pandas.DataFrame.shift`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.shift.html)  
    - [`statsmodels.graphics.tsaplots.plot_acf`](https://www.statsmodels.org/stable/generated/statsmodels.graphics.tsaplots.plot_acf.html)  
    - [`statsmodels.graphics.tsaplots.plot_pacf`](https://www.statsmodels.org/stable/generated/statsmodels.graphics.tsaplots.plot_pacf.html)  
    - Interactive plotting with [`plotly.express.line`](https://plotly.com/python/line-charts/)

---

## Feature Selection

- **Domain knowledge (primary filter)**  
    
  - Do not include variables just because they exist.  
  - Keep features with a plausible, defensible connection to the target.  
  - This step combats the **curse of dimensionality**: too many irrelevant predictors leads to overfitting.


- **Leakage check**  
    
  - Drop variables known only post-outcome or that encode the target directly.


- **Low-information features**  
    
  - Drop near-constant or high-missingness columns.  
    - **Note:** “Near constant” is not a fixed threshold — it’s contextual. Use domain knowledge to decide whether small variation is meaningful. For example, if request latency varies only from 2.3 ms to 2.4 ms, it’s implausible this explains differences in click-through rate; you should treat it as constant. But a drug dosage shift from 2.3 mg/kg to 2.4 mg/kg may have clinically significant effects and must not be discarded. The same numerical range can be irrelevant in one setting and critical in another.


- **Redundancy checks**  
    
  - Remove highly collinear features; keep one representative.  
  - Tools: [`pandas.DataFrame.corr`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.corr.html), VIF via [`statsmodels`](https://www.statsmodels.org/stable/generated/statsmodels.stats.outliers_influence.variance_inflation_factor.html)


- **Model-based diagnostics**  
    
  - Use feature importances as *supporting evidence* but not as the main decision tool.  
  - Tools: [`SelectFromModel`](https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SelectFromModel.html), tree-based models (`RandomForest*`, `XGB*`).

---

## Feature Engineering

- **Domain-driven transformations**  
  - Ratios, differences, interaction terms suggested by subject knowledge.  
- **Dimensionality reduction**  
  - Tools: [`PCA`](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html), [`UMAP`](https://umap-learn.readthedocs.io/en/latest/)  
- **Time features**  
  - Extract lags, rolling statistics, seasonality components.

---

## Iteration Between EDA and Feature Work

- **Expect to loop**  
    
  - EDA, feature selection, and feature engineering are not one-time steps. They should inform each other in cycles.


- **Workflow**  
    
  1. Explore data distributions and relationships in EDA.  
  2. Propose engineered features based on patterns or domain ideas.  
  3. Test them quickly with simple models or diagnostics.  
  4. If results are unhelpful (no signal, redundancy, instability), discard or revise.  
  5. Go back to EDA with new questions (e.g., “Why didn’t lag-7 help? Maybe seasonality is longer”).


- **Mindset**  
    
  - Don’t hoard features “just in case.” Keep the pipeline clean and only include features that survive scrutiny.  
  - Each iteration should strengthen your understanding of the data, not just expand the feature set.

---

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



