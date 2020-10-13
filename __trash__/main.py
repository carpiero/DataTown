import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

year = int(input('Enter the year: '))
title = 'Top 10 Manufacturers by Fuel Efficiency ' + str(year)

def acquire():
    data = pd.read_csv('./data/raw/vehicles.csv')
    return data

def wrangle(df):
    filtered = data[data['Year']==year]
    return filtered

def analyze(df):
    grouped = filtered.groupby('Make').agg({'Combined MPG':'mean'}).reset_index()
    results = grouped.sort_values('Combined MPG', ascending=False).head(10)
    return results

def visualize(df):
    fig, ax = plt.subplots(figsize=(15,8))
    barchart = sns.barplot(data=results, x='Make', y='Combined MPG')
    plt.title(title + "\n", fontsize=16)
    return barchart

def save_viz(barchart):
    fig = barchart.get_figure()
    fig.savefig('./data/results/' + title + '.png')

if __name__ == '__main__':
    data = acquire()
    filtered = wrangle(data)
    results = analyze(filtered)
    barchart = visualize(results)
    save_viz(barchart)
    print('Pipeline is complete. You may find the results in the folder ./data/results')