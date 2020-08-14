
import pandas as pd
import glob
import warnings
warnings.filterwarnings('ignore')
import datetime

# Company and date wise filtering
keys = pd.read_csv('keys.csv')      # keywords and company names to filter
keys_company_name = list(keys['Company_Name'])      # creating a list of company name, those are used to filter the articles


df = pd.read_csv('News_Portals/spiders/results.csv')    # reading the csv file
df= df[df.publish_date.notnull() & (df.publish_date != 'publish_date')]
final_df = pd.DataFrame()

clean_text = ['Source:', 'Source', 'Last', 'Updated :', ' Updated:', 'Published:', 'Updated:', '|']
df['title'] = df ['title'].str.replace('\n\t\t\t\t\t\t\t\t',"")
for cl in clean_text:
    df['publish_date'] = df['publish_date'].str.replace(cl,'')
print(df.shape)
for key in keys_company_name:                         # filtering the dataframe company account wise
    df.dropna(subset=['title'], inplace=True)
    data = df[df['title'].str.contains(key)]
    final_df = final_df.append(data, ignore_index=True)


final_df.drop_duplicates(['title'],inplace=True)
print(final_df.shape)
print(final_df.company)

#     date = final_df['publish_date'].str.split('/', expand=True)
#     final_df['date'] = date[0]
#     final_df.drop(columns=['publish_date'], axis=1, inplace=True)
# else:

date = final_df['publish_date'].str.split(',', expand=True)
final_df['dates'], final_df['year'] = date[0], date[1]
final_df['date'] = final_df['dates'] + final_df['year']
final_df.drop(columns=['publish_date','dates','year'], axis=1, inplace=True)

final_df['date'] = pd.to_datetime(final_df['date']).dt.date
final_df['date'] = pd.to_datetime(final_df['date'])
final_df = final_df[(final_df.date >= '2020-08-01') & (final_df.date <= '2020-08-11')]  # change the date
final_df.to_csv('Filtered_output.csv', index=False)      # converting the dataframes into excel for each news portal