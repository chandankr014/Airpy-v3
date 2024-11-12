import pandas as pd
import tqdm
import glob

def summarize_count_file(files: list):
    summaries = []

    for file in tqdm.tqdm(files):
        try:
            df = pd.read_csv(file)
            df['month'] = pd.to_datetime(df['Timestamp']).dt.month
            # df['dates'] = pd.to_datetime(df['dates'])
            df_group = df.groupby('month')
            for month in df_group:
                month = month[1]
                temp = month.reset_index().rename(columns={'index':'timestamp'})
                summary = temp.describe().loc['count'].to_dict()
                summary['site_id'] = temp['site_id'][0]
                summary['site_name'] = temp['site_name'][0]
                summary['year'] = temp['year'][0]
                summary['month'] = temp['month'][0]
                summaries.append(summary)
        except Exception as e: 
            print('failed for file: ',file, file=open('files/errors.txt','a'))   
            raise e
    summaries_df = pd.DataFrame(summaries)
    print(summaries_df.shape)
    print(summaries_df.columns)
    return summaries_df


if __name__ == '__main__':
    import os
    files = glob.glob('data/After_Cleaning_Mumbai/*')
    final_site_list = pd.read_csv('files/final_site_list_new.csv')
    # files = list(filter(lambda x: '_'.join(os.path.basename(x).split('_')[0:2]) in final_site_list['site_id'].values, files))
    df = summarize_count_file(files)
    df.to_csv('files/monthly_condensed_new.csv', index=False)
    print(df.columns)
    