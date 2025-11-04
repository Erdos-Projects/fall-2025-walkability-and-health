# Walkability and Health

A data science project aimed at determining which specific walkability features most significantly influence health outcomes at the census-tract level in the United States.

## Datasets

Our merged_data.csv file can be accessed [here](https://github.com/Erdos-Projects/fall-2025-walkability-and-health/tree/581bda73dad71a676170da5d09e27014340fa36a/datasets/merged_data) and consists of publicly available data described below.

- **Walkability data**: We used the Walkability Index data publicly available on [data.gov](https://catalog.data.gov/dataset/walkability-index8). This data set provides the four Walkability components of the Walkability index at the census-tract level in the United States for the year 2019:
    * Street intersection density (pedestrian-oriented intersections),
    * The mix of employment types and occupied housing,
    * The mix of employment types (such as retail, office, or industrial),
    * Distance from the population-weighted centroid to nearest transit stop (meters).

- **Health data**: The health dataset we are using [CDC PLACES 2021](https://data.cdc.gov/500-Cities-Places/PLACES-Census-Tract-Data-GIS-Friendly-Format-2021-/mb5y-ytti/about_data) contains health outcome prevalence rates (both physical and mental health) at the census-tract level in the United States for the year 2019. It is based on a predictive model that takes demographics and BRFSS surveys into account (see [model description](https://www.cdc.gov/places/methodology/index.html#:~:text=PLACES%20methodology,census%20tract%2C%20and%20ZCTA%20levels)).

- **Demographic data**: We wrote a Python script (see [here](https://github.com/Erdos-Projects/fall-2025-walkability-and-health/blob/581bda73dad71a676170da5d09e27014340fa36a/datasets/ACS_demographics_data/CensusAPI-Query.py)) to fetch [ACS data](https://www.census.gov/programs-surveys/acs/data.html) using the Census API. All features are at the census-tract level in the United States. As the health outcomes are partly estimated from demographic data, we only used our demographic data as part of our EDA.

## Stakeholders

- US public health departments
- Policymakers
- City planners
- Health insurance providers

## KPIs

- Test RMSE (root mean squared error) in predicting health outcome prevalence rates.
- Test $R^2$ score in predicting health outcome prevalence rates.

## Data Cleaning and EDA (Exploratory Data Analysis)

The main observation of our data cleaning phase (see our [data cleaning Jupyter notebook](https://github.com/Erdos-Projects/fall-2025-walkability-and-health/blob/581bda73dad71a676170da5d09e27014340fa36a/data%20cleaning%20and%20EDA/data_cleaning/data_cleaning.ipynb)) is that New Jersey health data was entirely missing. After finding an explanation for this missing data, we decided to exclude it from our analysis. Our code generates the final CSV file, which we will use for the remainder of our analysis.

Our exploratory data analysis revealed the strongest correlation between the walkability index and the following five health outcomes:

- High cholesterol,
- Obesity,
- High blood pressure,
- Depression,
- Cancer.

See our [EDA Jupyter notebook](https://github.com/Erdos-Projects/fall-2025-walkability-and-health/blob/581bda73dad71a676170da5d09e27014340fa36a/data%20cleaning%20and%20EDA/data_eda/exploratory_analysis.ipynb) for more details.

## Model Selection

We used the four components of the walkability index as our features:
- `employment_mix_ranked`,
- `employment_residential_mix_ranked`,
- `intersection_density_ranked`,
- `transit_accessibility_ranked`.

For our outcomes, we selected the five health outcomes most closely correlated with the walkability index obtained above:
- `high_cholesterol_prevalence`,
- `depression_prevalence`,
- `high_blood_pressure_prevalence`,
- `obesity_prevalence`,
- `cancer_prevalence`.

First, we split our data set using a county-aware GroupShuffleSplit in our [train-test-split Jupiter notebook](https://github.com/Erdos-Projects/fall-2025-walkability-and-health/blob/581bda73dad71a676170da5d09e27014340fa36a/model%20selection/train_test_split/train_test_split.ipynb).

In our [model evaluation Jupiter notebook](https://github.com/Erdos-Projects/fall-2025-walkability-and-health/blob/581bda73dad71a676170da5d09e27014340fa36a/model%20selection/model_evaluation/model_evaluation.ipynb), we first evaluated baseline models: Dummy (mean baseline), Linear Regression, and regularized linear regressions (Ridge and Lasso).

For our more sophisticated models, we added versions of our linear regressor that include principal component analysis (PCA) and versions that incorporate interaction terms. We also evaluated an ensemble of trees model (Random Forest Regressor) and a Poisson Regressor model.

To account for errors in health outcomes (each health outcome is estimated using BRFSS and demographic data and accompanied by confidence intervals), we manually implement a feasible generalized least squares (FGLS) model. We also detail the approach, which is based on the following [paper](https://www.jstor.org/stable/pdf/25791822.pdf?casa_token=N0BnCWKeyXEAAAAA:zpUTCEulSLZaUusXK78zRF6oIMlStssy-Q8E0MgtPalPAsdhX10pAM3BlexT-Dgp9ZuE3HSiKWeZGZNoF_d4tcJ_tTp8Q57ZVxYtY0znSW3Ewu38Xod2zA) mentioned by the CDC as a recommendation to tackle problems where the outcomes are estimated from a model.

Each model was evaluated on the training set via a county-aware GroupKFold across five splits, and hyperparameters were tuned using GridSearchCV. The table below summarizes our results, providing the overall average RMSE across both cross-validation and all outcomes.

| Model                       | Overall average RMSE |
| --------------------------- | -------------------- |
| Random Forest               | 4.403                |
| Linear + interactions       | 4.466                |
| Ridge + interactions        | 4.467                |
| Lasso + interactions        | 4.467                |
| PCA + linear + interactions | 4.467                |
| Linear                      | 4.503                |
| FGLS                        | 4.504                |
| PCA + linear                | 4.505                |
| Ridge                       | 4.505                |
| Lasso                       | 4.505                |
| Poisson                     | 4.505                |
| Dummy                       | 4.804                |

The Random Forest Regressor achieved the best performance among the tested models and was chosen as our final model. However, we observe that none of the models showed significant improvement over the dummy baseline.

## Results

In our [results Jupiter notebook](https://github.com/Erdos-Projects/fall-2025-walkability-and-health/blob/581bda73dad71a676170da5d09e27014340fa36a/results/results.ipynb), we fit our Random Forest Regressor on the entire training set and evaluate its performance on the testing set we had saved for this final step.

| Health Outcome                 | rmse_random_forest | r2_test | rmse_test_dummy |
| ------------------------------ | ------------------ | ------- | --------------- |
| cancer_prevalence              | 1.936              | 0.169   | 2.137           |
| depression_prevalence          | 3.947              | 0.049   | 4.382           |
| high_cholesterol_prevalence    | 4.368              | 0.205   | 5.024           |
| obesity_prevalence             | 6.554              | 0.115   | 7.31            |
| high_blood_pressure_prevalence | 6.695              | 0.129   | 7.452           |

The table below provides the permutation importance scores for `cancer_prevalence`, `depression_prevalence`, and `high_blood_pressure_prevalence`.

| feature                           | cancer_prevalence | depression_prevalence | high_blood_pressure_prevalence |
| --------------------------------- | ----------------- | --------------------- | ------------------------------ |
| employment_mix_ranked             | 0.01              | 0.07                  | 0.12                           |
| employment_residential_mix_ranked | 0.03              | 0.03                  | 0.41                           |
| intersection_density_ranked       | 0.15              | 0.17                  | 0.31                           |
| transit_accessibility_ranked      | 0.1               | 0.29                  | 0.43                           |

The table below provides the permutation importance scores for `high_cholesterol_prevalence` and `obesity_prevalence`.

| feature                           | high_cholesterol_prevalence | obesity_prevalence |
| --------------------------------- | --------------------------- | ------------------ |
| employment_mix_ranked             | 0.05                        | 0.13               |
| employment_residential_mix_ranked | 0.04                        | 0.66               |
| intersection_density_ranked       | 0.36                        | 0.19               |
| transit_accessibility_ranked      | 0.39                        | 0.63               |

Our notebook also provides partial dependency plots (PDP) with confidence intervals obtained using a bootstrap resampling method.

**Conclusion**: Our model does not score significantly higher than the Dummy baseline for any outcomes. Although we did not exhaust all possible models, it appears that the predictive power of walkability features in predicting health outcomes within a census tract is limited.

## Future Directions

It is possible that our model would achieve higher prediction scores if we had access to more features. It is also possible that, even with more features, the census-tract level is too large to predict anything accurately. In the future, it would be interesting to explore the following directions:
- Add more walkability features to our covariates, such as proximity to food, healthcare, and nature. It would also be interesting to have access to safety and climate scores at the census-tract level. 
- Explore the same problem using individual-level health data.
- Explore the same problem in a different country.