import pandas as pd
from sqlalchemy import create_engine
from functools import reduce
import requests
from bs4 import BeautifulSoup
import re

# acquisition functions

def get_tables(path):

    engine = create_engine(f'sqlite:///{path}')
    df_personal = pd.read_sql("SELECT * FROM personal_info" , engine)
    df_country = pd.read_sql("SELECT * FROM country_info" , engine)
    df_career = pd.read_sql("SELECT * FROM career_info" , engine)
    df_poll = pd.read_sql("SELECT * FROM poll_info" , engine)
    dfs = [df_personal, df_country, df_career, df_poll]
    df_final = reduce(lambda left , right: pd.merge(left , right , on='uuid'), dfs)

    return df_final


def clean(df_clean):

    ''' cleaning age column '''

    df_clean['age'] = df_clean['age'].str.replace(' years old' , '')

    for x in range(1980, 2087):
        df_clean['age'] = df_clean['age'].str.replace(f'{x}' , f'{2016 - x}')

    df_clean['age'] = df_clean['age'].astype('int64')


    ''' cleaning gender column '''

    df_clean['gender'] = df_clean['gender'].str.replace(r'\bmale\b' , 'Male') \
                                            .str.replace(r'\bFem\b' , 'Female') \
                                            .str.replace(r'\bFeMale\b' , 'Female') \
                                            .str.replace(r'\bfemale\b' , 'Female')

    df_clean['gender'] = df_clean['gender'].astype('category')


    ''' cleaning dem_has_children column '''

    df_clean['dem_has_children'] = df_clean['dem_has_children'].str.replace(r'\bNO\b' , 'no') \
                                                                .str.replace(r'\byES\b' , 'yes') \
                                                                .str.replace(r'\bnO\b' , 'no') \
                                                                .str.replace(r'\bYES\b' , 'yes')

    df_clean['dem_has_children'] = df_clean['dem_has_children'].astype('category')


    ''' cleaning age_group column '''

    df_clean['age_group'] = df_clean['age_group'].str.replace(r'\bjuvenile\b' , '14_25')
    df_clean['age_group'] = df_clean['age_group'].astype('category')


    ''' cleaning country_code column '''

    df_clean['country_code'] = df_clean['country_code'].str.replace(r'\bGB\b' , 'UK') \
                                                        .str.replace(r'\bGR\b' , 'EL')

    df_clean['country_code'] = df_clean['country_code'].astype('category')


    ''' cleaning rural column '''

    df_clean['rural'] = df_clean['rural'].str.replace(r'\bcity\b' , 'urban') \
                                                .str.replace(r'\bNon-Rural\b' , 'urban') \
                                                .str.replace(r'\bCountry\b' , 'rural') \
                                                .str.replace(r'\bcountryside\b' , 'rural') \
                                         
    df_clean['rural'] = df_clean['rural'].astype('category')


    ''' cleaning dem_full_time_job column '''

    df_clean['dem_full_time_job'] = df_clean['dem_full_time_job'].astype('category')


    ''' cleaning question_bbi_2016wave4_basicincome_effect column '''

    df_clean['question_bbi_2016wave4_basicincome_effect'] = \
        df_clean['question_bbi_2016wave4_basicincome_effect'].str.replace(r'‰Û_' , 'I')

    return df_clean


def web_scrapping(df_web_scrapping):

    ''' Extract the information from the website'''

    url = 'https://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:Country_codes'
    html = requests.get(url).content
    soup = BeautifulSoup(html , 'lxml')
    table = soup.find_all('div' , {'class': 'mw-content-ltr'})[0]
    rows = table.find_all('table')
    rows_parsed = [row.text for row in rows]

    ''' cleaning scrapping text and create a dictionary with the codes and countries'''

    rows_without_spaces = [re.sub(r'\s' , '' , x) for x in rows_parsed]
    rows_without_star = [re.sub(r'\*' , '' , x) for x in rows_without_spaces]
    rows_without_squarebrackets = [re.sub(r'\[\d\]' , '' , x) for x in rows_without_star]
    rows_clean = ''.join(rows_without_squarebrackets)

    '''Every country consist of a 2-character code except one country that has a 7-character code,
     it is set to {0.7} to give the option that codes of 0 to 7 characters may appear in the future.'''

    rows_country_value = re.split(r'\(\w{0,7}\)' , rows_clean)
    rows_code_key = re.findall(r'\(\w{0,7}\)' , rows_clean)
    rows_code_key = [re.sub(r'\(|\)' , '' , x) for x in rows_code_key]

    dict_country = dict(zip(rows_code_key , rows_country_value))

    ''' Add a new column to the DataFrame with the information of web scrapping dictionary '''
    
    df_web_scrapping['Country'] = ''
    for key, value in dict_country.items():
        df_web_scrapping.loc[df_web_scrapping['country_code'] == key, 'Country'] = value

    return df_web_scrapping


def api_jobs(df_api_jobs):

    list_unique_jobs = df_api_jobs['normalized_job_code'].unique().tolist()

    ''' Get the information from the API and create a dictionary with the Normalized Job Code and Jobs Title'''

    list_uuid_key = []
    list_title_value = []
    for x in list_unique_jobs:
        url = f'http://api.dataatwork.org/v1/jobs/{x}'
        response = requests.get(url).json()
        if list(response.keys())[0] == 'error':
            pass
        else:
            list_uuid_key.append(response['uuid'])
            list_title_value.append(response['title'])

    dict_uuid_title = dict(zip(list_uuid_key , list_title_value))

    ''' Add a new column to the DataFrame with the information of Jobs Title API '''

    df_api_jobs['Job Title'] = df_api_jobs['normalized_job_code']
    for k , v in dict_uuid_title.items():
        df_api_jobs.loc[df_api_jobs['normalized_job_code'] == k , 'Job Title'] = v



    # df_api_jobs = pd.read_parquet(f'./data/processed/df_api_jobs.parquet')


    # df_api_jobs.to_parquet('./data/processed/df_api_jobs.parquet')

    return df_api_jobs


def acquire(path):
    df_clean= clean(get_tables(path))
    df_web_scrapping= web_scrapping(df_clean)

    return api_jobs(df_web_scrapping)

















