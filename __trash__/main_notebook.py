import pandas as pd
from zipfile import ZipFile

zip_data = ZipFile('./data/raw/vehicles.zip')
data = pd.read_csv(zip_data.open('vehicles/vehicles.csv'))

print('DATAFRAME SHAPE \n - rows: {} \n - columns: {}'.format(data.shape[0],data.shape[1]),'\n')
print('DATAFRAME NULLS COUNT: \n{}'.format(data.isnull().sum()),'\n')
print('DATAFRAME COLUMNS TYPE: \n{}'.format(data.dtypes,'\n'))

zip_data = ZipFile('../data/raw/vehicles.zip')
data = pd.read_csv(zip_data.open('vehicles/vehicles.csv'))
data

filtered = data[data['Year']==2012]
filtered

filtered.to_csv('../data/processed/filtered.csv', index=False)
filtered.to_json('../data/processed/filtered.json')

data = pd.read_csv('../data/processed/filtered.csv')
data

grouped = data.groupby('Make').agg({'Combined MPG':'mean'}).reset_index()
grouped

results = grouped.sort_values('Combined MPG', ascending=False)
results

results.to_csv('../data/results/results.csv', index=False)
results.to_json('../data/results/results.json')

data = pd.read_csv('../data/results/results.csv')
data

year = 2012
title = 'Top 10 Manufacturers by Fuel Efficiency ' + str(year)
fig, ax = plt.subplots(figsize=(15,8))
barchart = sns.barplot(data=data, x='Make', y='Combined MPG')
plt.title(title + "\n", fontsize=16)

file_name = '../data/results/' + title + '.png'
fig = barchart.get_figure()
fig.savefig(file_name)