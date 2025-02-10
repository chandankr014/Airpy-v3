import pandas as pd
import numpy as np

breakpoints = {
    'PM10' : [(0, 50, 0, 50), (50, 100, 50, 100), (100, 250, 100, 200), (250, 350, 201, 300), (350, 430, 300, 400), (430, 511, 400, 500)],
    'PM25' : [(0, 30, 0, 50), (30, 60, 50, 100), (60, 90, 100, 200), (90, 120, 201, 300), (120, 250, 300, 400), (250, 381, 400, 500)],
    'NO2' : [(0, 40, 0, 50), (40, 80, 50, 100), (80, 180, 100, 200), (180, 280, 201, 300), (280, 400, 300, 400), (400, 521, 400, 500)],
    'O3' : [(0, 50, 0, 50), (50, 100, 50, 100), (100, 168, 100, 200), (168, 208, 201, 300), (208, 748, 300, 400), (748, 1288, 400, 500)]
}

# Function to calculate sub-index for a single pollutant
def calculate_sub_index(concentration, breakpoints):
    for breakpoint in breakpoints:
        if (breakpoint[0] <= concentration <= breakpoint[1]):
            return (breakpoint[2] + (concentration - breakpoint[0]) * (breakpoint[3] - breakpoint[2]) / (breakpoint[1] - breakpoint[0]))
    return None

def calculate_sub_index_vectorized(values_input: pd.Series, breakpoints):
    values = pd.Series(index=values_input.index, dtype='float64')
    for breakpoint in breakpoints:
        values.loc[values_input.between(breakpoint[0], breakpoint[1], inclusive='both')] = breakpoint[2] + (values_input - breakpoint[0]) * (breakpoint[3] - breakpoint[2]) / (breakpoint[1] - breakpoint[0])
        # print(values.iloc[325])
    return values

# Function to calculate GVAQI
def calculate_gvaqi(df_input: pd.DataFrame, cols = ['NO2_CPCB', 'PM10_clean', 'PM25_clean', 'Ozone_clean']):
    df_output = df_input
    # df = df_input.rolling(window=360, min_periods=4).mean()
    # df_output['NO2_sub_index'] = df['NO2_CPCB'].apply(lambda x: calculate_sub_index(x, breakpoints['NO2']))
    # df_output['PM10_sub_index'] = df['PM10_clean'].apply(lambda x: calculate_sub_index(x, breakpoints['PM10']))
    # df_output['PM25_sub_index'] = df['PM25_clean'].apply(lambda x: calculate_sub_index(x, breakpoints['PM25']))
    # df_output['O3_sub_index'] = df['Ozone_clean'].apply(lambda x: calculate_sub_index(x, breakpoints['O3']))
    df_output['NO2_sub_index'] = calculate_sub_index_vectorized(df_input[cols[0]], breakpoints['NO2'])
    df_output['PM10_sub_index'] = calculate_sub_index_vectorized(df_input[cols[1]], breakpoints['PM10'])
    df_output['PM25_sub_index'] = calculate_sub_index_vectorized(df_input[cols[2]], breakpoints['PM25'])
    df_output['O3_sub_index'] = calculate_sub_index_vectorized(df_input[cols[3]], breakpoints['O3'])
    
    df_output['AQI'] = df_output[['NO2_sub_index', 'PM10_sub_index', 'PM25_sub_index','O3_sub_index']].max(axis=1)
    df_output['AQI'].loc[df_output['PM10_sub_index'].isna() & df_output['PM10_sub_index'].isna()] = np.nan
    df_output['Index_pollutant'] = df_output[['NO2_sub_index', 'PM10_sub_index', 'PM25_sub_index','O3_sub_index']].idxmax(axis=1)
    # print(df_output.columns)
    return df_output


# if __name__ == '__main__':
#     df = pd.read_csv(r"CPCB_Issues\AirPy_v2\new_data\After_Cleaning_New\site_251_ICRISAT_Patancheru_Hyderabad_TSPCB_2019.csv")
#     df = calculate_gvaqi(df)
#     print(df[['dates', 'NO2_CPCB', 'PM10_clean','PM25_clean', 'Ozone_clean', 'NO2_sub_index', 'PM10_sub_index', 'PM25_sub_index', 'O3_sub_index', 'AQI', 'Index_pollutant']][df['AQI'] > 0][300:310])
