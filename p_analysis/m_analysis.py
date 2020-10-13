import numpy as np

# analysis functions

def quantity(df_quantity):

    df_quantity['Quantity'] = 1
    list_group = ['Country' , 'Job Title' , 'gender']
    df_quantity = df_quantity[['Country' , 'Job Title' , 'gender' , 'Quantity']]\
                                            .groupby(list_group ,as_index=False).count()

    df_quantity['Quantity'] = df_quantity['Quantity'].fillna(0)
    df_quantity['Quantity'] = df_quantity['Quantity'].astype('int64')

    return df_quantity


def percentage(df_percentage):

    ''' Add a new column 'Total People' to the Groupby ['Country', 'Job Title', 'gender', 'Quantity'] DataFrame with all the people surveyed for each country '''

    list_country = df_percentage['Country'].unique().tolist()
    df_percentage['Total People'] = 0
    for x in list_country:
        df_percentage.loc[df_percentage['Country'] == x , 'Total People'] = \
            df_percentage.loc[df_percentage['Country'].str.contains(x) , 'Quantity'].sum()

    ''' Add a new column 'Percentage' to the Groupby ['Country', 'Job Title', 'gender', 'Quantity', 'Total People'] 
    DataFrame with the percentage of people from the same country with the same gender and jobs. '''

    df_percentage['Percentage'] = np.where(df_percentage['Quantity'] == 0 , 12345.12345 ,
                                         round(df_percentage['Quantity'] / df_percentage['Total People'] * 100))

    df_percentage['Percentage'] = np.where(df_percentage['Percentage'] == 12345.12345 ,
                                         'Does not apply' , df_percentage['Percentage'].apply(lambda x: f'{int(x)} %'))

    df_percentage['Percentage'] = df_percentage['Percentage'].str.replace(r'\b0 %' , 'less than 1 %')


    return df_percentage


def final_table(df_final_table):

    df_final_table['Gender (1)'] = df_final_table['gender']
    df_final_table = df_final_table.loc[df_final_table['Quantity']>0].reset_index()
    df_final_table = df_final_table[['Country' , 'Job Title' , 'Gender (1)' , 'Quantity' , 'Percentage']]

    return df_final_table


def analyze(filtered):

    df_quantity= quantity(filtered)
    df_percentage= percentage(df_quantity)

    return final_table(df_percentage)