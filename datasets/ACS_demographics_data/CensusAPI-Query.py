from census import Census
import us
import pandas as pd
import time



#-- Configuration --#
API_KEY = 'f8b6ae081340594e426e31db8f9b65352a2e7fcf'
YEAR = 2019  # ACS year
c = Census(API_KEY)

# Variables to fetch
general_var = {
    "total_population": "B01003_001E", #Estimate!!Total
    "median_income": "B19013_001E", #Estimate!!Median household income in the past 12 months
    "unemployed": "B23025_005E", #Estimate!!Total:!!In labor force:!!Civilian labor force:!!Unemployed. #EMPLOYMENT STATUS FOR THE POPULATION 16 YEARS AND OVER
    "labor_force": "B23025_003E", # Estimate!!Total:!!In labor force:!!Civilian labor force
    "commute_total": "B08301_001E", # Total MEANS OF TRANSPORTATION TO WORK
    "commute_car": "B08301_002E", #	Estimate!!Total:!!Car, truck, or van
    "commute_transit": "B08301_010E", # Estimate!!Total:!!Public transportation (excluding taxicab)
    "below_poverty": "B17001_002E" # Estimate!!Total:!!Income in the past 12 months below poverty level
    }

#	EDUCATIONAL ATTAINMENT FOR THE POPULATION 25 YEARS AND OVER
education_var = {
    "less_hs": "B15003_002E", # Estimate!!Total:!!No schooling completed
    "hs_grad": "B15003_017E", # Estimate!!Total:!!Regular high school diploma
    "bachelor_degree": "B15003_022E", # Estimate!!Total:!!Bachelor's degree
    "grad_degree": "B15003_023E", # Estimate!!Total:!!Graduate or professional degree
    "professional_school_degree": "B15003_024E", # Estimate!!Total:!!Professional school degree
    "Doctorate_degree": "B15003_025E" # Estimate!!Total:!!Doctorate degree
}

edu_bachelor_and_higher = ['B15003_022E', 'B15003_023E', 'B15003_024E', 'B15003_025E']

# Age variables are devided into groups of age range by sex in the census data
# We will sum them up to get the total population in the age range

age_var_21_to_65 = ['B01001_009E', 'B01001_010E', 'B01001_011E', 'B01001_012E', 'B01001_013E', 'B01001_014E', 'B01001_015E', 'B01001_016E', 'B01001_017E', 'B01001_018E', 'B01001_019E',
                    'B01001_033E', 'B01001_034E', 'B01001_035E', 'B01001_036E', 'B01001_037E', 'B01001_038E', 'B01001_039E', 'B01001_040E', 'B01001_041E','B01001_042E', 'B01001_043E',]

age_var_over_65 = ['B01001_020E', 'B01001_021E', 'B01001_022E', 'B01001_023E', 'B01001_024E', 'B01001_025E',
                   'B01001_044E', 'B01001_045E', 'B01001_046E', 'B01001_047E', 'B01001_048E', 'B01001_049E']

# Race variables
race_var = {
    "white": "B02001_002E", # Estimate!!Total:!!White alone
    "black": "B02001_003E", # Estimate!!Total:!!Black or African American alone
    "native_american": "B02001_004E", # Estimate!!Total:!!American Indian and Alaska Native alone
    "asian": "B02001_005E", # Estimate!!Total:!!Asian alone
    "pacific_islander": "B02001_006E", # Estimate!!Total:!!Native Hawaiian and Other Pacific Islander alone
    "other_race": "B02001_007E", # Estimate!!Total:!!Some other race alone
}



all_vars = list(general_var.values()) + edu_bachelor_and_higher + age_var_21_to_65 + age_var_over_65 + list(race_var.values())

all_data = []
# Loop through states and fetch data
for state in us.states.STATES:
    try:

        print(f"Fetching data for {state.name}")
    
    # query trect level data for all counties in the state
        data = c.acs5.state_county_tract(all_vars, state.fips,
                                          '*', # all counties
                                          '*', # all tracts
                                          year=YEAR)

        df = pd.DataFrame(data)

        if df.empty:
            continue

    # Build GEOID
        df['GEOID'] = df['state'] + df['county'] + df['tract']

        df = df.rename(columns={v: k for k, v in general_var.items()})
        df = df.rename(columns={v: k for k, v in race_var.items()})
    
    # Derived variables
        df["age_21_to_65"] = df[age_var_21_to_65].astype(float).sum(axis=1)
        df["age_over_65"] = df[age_var_over_65].astype(float).sum(axis=1)
        df["percent_over_65"] = df["age_over_65"]/df["total_population"].astype(float) * 100
        df["edu_bachelor_and_higher"] = df[edu_bachelor_and_higher].astype(float).sum(axis=1)
        df["percent_bachelor_and_higher"] = df[edu_bachelor_and_higher].astype(float).sum(axis=1) / df["total_population"].astype(float) * 100
        df["percent_unemployed"] = df["unemployed"].astype(float) / df["labor_force"].astype(float) * 100
        df["percent_commute_car"] = df["commute_car"].astype(float) / df["commute_total"].astype(float) * 100
        df["percent_commute_transit"] = df["commute_transit"].astype(float) / df["commute_total"].astype(float) * 100
        df["percent_below_poverty"] = df["below_poverty"].astype(float) / df["total_population"].astype(float) * 100
        df["percent_white"] = df["white"].astype(float) / df["total_population"].astype(float) * 100
        df["percent_black"] = df["black"].astype(float) / df["total_population"].astype(float) * 100
        df["percent_native_american"] = df["native_american"].astype(float) / df["total_population"].astype(float) * 100
        df["percent_asian"] = df["asian"].astype(float) / df["total_population"].astype(float) * 100
        df["percent_pacific_islander"] = df["pacific_islander"].astype(float) / df["total_population"].astype(float) * 100

        # Select relevant columns to save
        df_final = df[[
            "GEOID", "median_income", "percent_unemployed", "percent_below_poverty", "percent_unemployed",
            "percent_bachelor_and_higher", "percent_over_65", "percent_commute_car", "percent_commute_transit", "percent_white", "percent_black",
            "percent_native_american", "percent_asian", "percent_pacific_islander"
        ]]

        all_data.append(df_final)

        time.sleep(0.5)  # avoid hitting API rate limits

    except Exception as e:
        print(f"Error fetching data for {state.name}: {e}")
        continue

# Combine all states data into a single DataFrame
national_acs_df = pd.concat(all_data, ignore_index=True)

# Save to CSV
national_acs_df.to_csv('data/raw/acs/national_acs_data_2019.csv', index=False)
print("Data saved to national_acs_data_2019.csv")

print(national_acs_df.head())