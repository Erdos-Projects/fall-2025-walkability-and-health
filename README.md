# Walkability and Health
This data science project explores/models the impact of the **EPA walkability index** on **health outcomes** at the **census-tract level in the USA**.

## Dataset
Our dataset GitHub repository can be accessed [here](https://github.com/Erdos-Projects/fall-2025-walkability-and-health/tree/main/data) and is publicly available.

## Stakeholders
- Public health departments
- Policymakers
- City planners

## Analysis
- Unit: US census tract (see [definition](https://www.census.gov/programs-surveys/geography/about/glossary.html#par_textimage_13))
- Time horizon: year 2019
- Geographic region: US
- Features: [components](https://www.epa.gov/sites/default/files/2021-06/documents/national_walkability_index_methodology_and_user_guide_june2021.pdf) of the EPA walkability index
- Outcome: health outcomes (see [definition](https://data.cdc.gov/500-Cities-Places/PLACES-Census-Tract-Data-GIS-Friendly-Format-2021-/mb5y-ytti/about_data))
    1. Arthritis among adults, `ARTHRITIS`
    2. High blood pressure among adults, `BPHIGH`
    3. Cancer (non-skin) or melanoma among adults, `CANCER`
    4. Current asthma among adults, `CASTHMA`
    5. Coronary heart disease among adults, `CHD`
    6. Chronic obstructive pulmonary disease among adults, `COPD`
    7. Diagnosed diabetes among adults, `DIABETES`
    8. High cholesterol among adults who have ever been screened, `HIGHCOL`
    9. Chronic kidney disease among adults, `KIDNEY`
    10. Depression among adults, `DEPRESSION` 
    11. Obesity among adults, `OBESITY`
    12. Stroke among adults, `STROKE`
    13. All teeth lost among adults aged ≥65 years, `TEETHLOST`
- Weight: Census tracts will be weighted by their population
- Other essential features: demographics (age, sex, education, etc.)

## KPIs
- RMSE of our model in predicting a given health outcome, knowing the walkability.

# Our Pipeline

## Modeling Approach
The health dataset we are using [CDC PLACES 2021](https://data.cdc.gov/500-Cities-Places/PLACES-Census-Tract-Data-GIS-Friendly-Format-2021-/mb5y-ytti/about_data) is based on a predictive model taking demographics into account (see [model description](https://www.cdc.gov/places/methodology/index.html#:~:text=PLACES%20methodology,census%20tract%2C%20and%20ZCTA%20levels.)). For each measure, the CDC PLACES dataset provides a 95 % confidence interval. This matters for the two reasons below (mentioned in [The Use of Small Area Estimates in Place-Based Health Research](https://pmc.ncbi.nlm.nih.gov/articles/PMC7204458/)):
1. We may not include demographic features in our regression (see [CDC PLACES FAQ](https://www.cdc.gov/places/faqs/using-data/index.html?utm_source=chatgpt.com)),
2. Our outcome is noisy (with known confidence intervals), so we need to take this into account in our approach. The following papers provide some guidance for this scenario:
    - [Estimating Regression Models in Which the Dependent Variable Is Based on Estimates](https://www.jstor.org/stable/pdf/25791822.pdf?casa_token=N0BnCWKeyXEAAAAA:zpUTCEulSLZaUusXK78zRF6oIMlStssy-Q8E0MgtPalPAsdhX10pAM3BlexT-Dgp9ZuE3HSiKWeZGZNoF_d4tcJ_tTp8Q57ZVxYtY0znSW3Ewu38Xod2zA)
    - [Usage of an estimated coefficient as a dependent variable](https://www.sciencedirect.com/science/article/pii/S0165176512001231)
