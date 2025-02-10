import pandas as pd
import glob
import tqdm
from aqi_calculator import calculate_gvaqi
import warnings
warnings.simplefilter(action='ignore')


def summarize_count_file(files: list):
    summaries = []
    for file in tqdm.tqdm(files):
        try:
            df = pd.read_csv(file)
            print("count_file: ", df.shape)
            summary = df.reset_index().rename(columns={'index':'timestamp'}).describe().loc['count'].to_dict()
            summary['site_id'] = df['site_id'][0]
            summary['site_name'] = df['site_name'][0]
            summary['year'] = df['year'][0]
            summary['mismatch'] = df['mismatch'].sum() 
            summary['prevalent_error'] = df['error'].value_counts().idxmax()
            summary['errors'] = df['error'].value_counts().sort_index().index.str.cat(sep=',')
            summary['errors'] = ''

            if len(df['error'].dropna()) > 0:
                summary['errors'] = df['error'].value_counts().sort_index().index.str.cat(sep=',') 
                summary['prevalent_error'] = df['error'].value_counts().idxmax()
            else:
                summary['errors'] = ''
                summary['prevalent_error'] = ''

            # print(summary)
            summaries.append(summary)
            print(f"DONE: {summary['site_id']}")

        except KeyError as e:
            summary[e.args[0]] = ''
        except Exception as e: 
            print('failed for file: ',e)
            raise e
    summaries_df = pd.DataFrame(summaries)
    return summaries_df


def summarize_mean_file(files: list):
    summaries = []
    
    for file in tqdm.tqdm(files):
        try:
            print(file)
            df = pd.read_csv(file)
            print("mean_file: ", df.shape)
            summary = df.reset_index().rename(columns={'index':'timestamp'}).describe().loc['mean'].to_dict()
            summary['site_id'] = df['site_id'][0]
            summary['site_name'] = df['site_name'][0]
            summary['year'] = df['year'][0]
            summary['mismatch'] = df['mismatch'].sum()
            summary['AQI_before_cleaning'] = calculate_gvaqi(df, cols=['NO2','PM10','PM25','Ozone'])['AQI'].mean()
            summary['AQI_after_cleaning'] = calculate_gvaqi(df)['AQI'].mean()
            if len(df['error'].dropna()) > 0:
                summary['errors'] = df['error'].value_counts().sort_index().index.str.cat(sep=',') 
                summary['prevalent_error'] = df['error'].value_counts().idxmax()
            else:
                summary['errors'] = ''
                summary['prevalent_error'] = ''
            print(f"DONE: {summary['site_id']}")

        except Exception as e: 
            print('failed for file: ',e)
            raise e
        finally:
            summaries.append(summary)  
    summaries_df = pd.DataFrame(summaries)
    return summaries_df


def create_site_list(files):
    pollutants = ['Ozone','NO2', 'PM25', 'PM10']
    records = []
    for p in pollutants:
        for f in files:
            site_id = "_".join(f.split("\\")[-1].split('_')[0:2])
            records.append({'site_id': site_id, 'pollutant': p})
    df = pd.DataFrame(records)
    return df


if __name__ == '__main__':
    files = glob.glob('data/After_Cleaning_Mumbai/*')
    print(len(files))
    
    sites_list_df = create_site_list(files)
    sites_list_df.to_csv('files/sites_list.csv')
    final_site_list = pd.read_csv('files/sites_list.csv')
    # summarize_count_file(files).to_csv('CPCB_Issues/AirPy_v2/new_data/summary/summary_count_AQI.csv', index=False)
    # summarize_mean_file(files).to_csv('Summary/summary_mean_AQI.csv', index=False)
    
    summary_count = summarize_count_file(files)
    # summary_count.to_csv('Summary/summary_count_final.csv', index=False)
    summary_count[summary_count['site_id'].isin(final_site_list['site_id'])].to_csv('Summary/summary_count_final.csv', index=False)
    
    summary_mean = summarize_mean_file(files)
    # summary_mean.to_csv('Summary/summary_mean_final.csv', index=False)
    summary_mean[summary_mean['site_id'].isin(final_site_list['site_id'])].to_csv('Summary/summary_mean_final.csv', index=False)

    