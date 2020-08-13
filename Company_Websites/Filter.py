import pandas as pd
#import glob
import warnings
warnings.filterwarnings('ignore')
#import datetime

keys = pd.read_csv('keywords.csv')

keys_keywords = list(keys['Keywords'])


df = pd.read_csv('Company_Websites/spiders/results.csv')
df= df[df.publish_date.notnull() & (df.publish_date != 'publish_date')]
df.dropna(subset=['text'], inplace=True)
final_df = pd.DataFrame()
start_date = '08-01-2020'                               # date range to filter the dataframe
end_date  = '08-12-2020'
for key in keys_keywords:                                          # filtering the dataframe keyword wise
    data = df[df['text'].str.contains(key)]
    final_df = final_df.append(data, ignore_index=True)
final_df.drop_duplicates(['text'],inplace=True)
final_df['publish_date'] = pd.to_datetime(final_df['publish_date'])
#mask = (final_df['publish_date'] == start_date )
mask = (final_df['publish_date'] >= start_date ) & (final_df['publish_date'] <= end_date )  # creating a boolean mask to filter data
final_df = final_df.loc[mask]
final_df.to_csv('Filtered_output.csv', index=False)
print(final_df)