import os 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gc
from datetime import datetime as time
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")
from scripts.formatting import *
from scripts.NO_Count_Mismatch import *
from scripts.unit_inconsistency import *
from scripts.plot_diurnal import *
from HTML.init_html import *
from scripts.data_cleaning import *
from scripts.functions import *


""" 
This is used for data cleaning of CPCB data for specific city.
Set the paths below and run the code.
"""
CITY_NAME = 'pune'

data_dir = Path(f'data/LIVE/')
save_dir = Path(f'data/airpy_clean/')

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

sites = pd.read_csv('files/sites.csv')
files = os.listdir(data_dir)

# years = [2019,2020,2021,2022,2023]


for idx, file in enumerate(files):
    print(file)
    try:
        filepath = os.path.join(data_dir, file)
        mixed_unit_identification = False
        
        site_id, site_name, year, city = get_siteId_Name_Year_City_LIVE(file, sites)
        print("FILE:", file)
        
        # gc.collect()
        true_df, station_name, city, state = get_formatted_df(filepath, site_name, city, city)
        # if pd.api.types.is_datetime64_any_dtype(true_df['Timestamp'])==False:
        #     true_df['Timestamp'] = pd.to_datetime(true_df['Timestamp'])
        #     true_df = true_df[true_df['Timestamp'].dt.year == year] #sort for the year
        print(true_df.columns)
        true_df = true_df.loc[~true_df.index.duplicated(keep='first')]
        print("LOG: TRUE DF", true_df.shape)
        
        df = true_df.copy()

        filename = station_name+"_"+str(year) 

        # make every html related code runnable (uncomment if any)
        start_html(filename)

        local_df = df.copy()
        local_df['date'] =  pd.to_datetime(local_df['Timestamp']).dt.date
        # local_df = local_df.sort_values(by=['Timestamp'])
        # local_df = local_df[local_df['date'].notna()]
        print("LOG:", local_df.shape)
        local_df['site_id'] = site_id
        local_df['site_name'] = site_name
        local_df['city'] = city
        local_df['state'] = state

        pollutants = ['PM25', 'PM10', 'NOx', 'NO2', 'NO', 'Ozone']
        # pollutants = ['PM25', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'SO2', 'CO', 'Ozone']
        for pollutant in pollutants:
            if len(df[pollutant].value_counts()) == 0:
                print("Not available ", pollutant, " data")
                continue
            else:
                # DATA CLEANING 
                local_df = group_plot(local_df, pollutant, pollutant, station_name, filename, plot=True, year=year)           
                local_df[pollutant + '_hourly'] = local_df.groupby("site_id")[pollutant].rolling(window = 4*1, min_periods = 1).mean().values
                local_df[pollutant + '_clean'] = local_df[pollutant + '_outliers']
                local_df[pollutant + '_clean'].mask(local_df[pollutant+ '_hourly'] < 0, np.nan, inplace=True)
                local_df.drop(columns=[f"{pollutant}_hourly"], inplace=True)

                print("successfully cleaned ", pollutant, station_name)
        
        if df['NOx'].isnull().all() or df['NO2'].isnull().all() or df['NO'].isnull().all():
            print("No available NOx, NO2, NO data | Not checking for unit inconsistency")
        else:
            print("finding unit inconsistencies: ", station_name)
            local_df = correct_unit_inconsistency(local_df,filename, mixed_unit_identification, plot=True)
        
        local_df = NO_count_mismatch(local_df)
        local_df = local_df.reindex()
        local_df = local_df[local_df.columns.drop(list(local_df.filter(regex='_int')))]
        local_df = local_df[local_df.columns.drop(list(local_df.filter(regex='(?<!_)consecutives')))]
        local_df = local_df.drop(columns=['t', 'std', 'med', 'date','ratio','Benzene', 'Toluene', 'Xylene', 'O Xylene', 'Eth-Benzene','MP-Xylene', 'AT', 'RH', 'WS', 'WD', 'RF', 'TOT-RF', 'SR', 'BP', 'VWS'], errors='ignore')
        local_df = local_df[['Timestamp', 'site_id', 'city','state'] + [col for col in local_df.columns if col not in ['dates', 'Timestamp', 'site_id', 'city','state']]]
        local_df['year'] = year
        print("LOG: DONE LOCAL DF")

        # SAVING -----------------------
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        if file.endswith('.csv'):
            fn = str(save_dir) + '/' + str(site_id) + '_' + str(year)+ ".csv"
            local_df.to_csv(fn, index=False)
        if file.endswith('.xlsx'):
            fn = str(save_dir) + '/' + str(site_id) + '_' + str(year)+ ".xlsx"
            local_df.drop(columns=['To Date', 'Timestamp'], inplace=True)
            local_df.rename(columns={'From Date':'Timestamp'}, inplace=True)
            local_df.to_excel(fn, index=False)
        
        print('Saved successfully for: '  + str(site_id) + '_' + str(year))
        plt.close('all')
        print("----------------------------------------------------------")

    except Exception as e:
        print("Error Occured in [main.py]- ", e)
        print("----------------------------------------------------------")
