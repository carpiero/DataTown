import pandas as pd
import numpy as np


def raw_cesel():

########### coste pestana 1 y 2 de los excels
    CCAA = ['01' , '02' , '03' , '04' , '05' , '06' , '07' , '08' , '09' , '10' , '11' , '12' , '13' , '16' , '17']

    df_total_coste = pd.DataFrame()

    for x in CCAA:
        for y in range(2):
            df = pd.read_excel(f'./data/main_raw_excel/CESEL_2018_{x}.xlsx' , sheet_name=y , header=10)
            df_total_coste = pd.concat([df_total_coste , df] , axis=0)


    df_coste = df_total_coste[['Provincia' , 'Código Ente Principal' , 'Tipo Ente Principal'
        , 'Nombre Ente Principal' , 'Descripción' , 'coste_efectivo']]

    df_total_coste[df_total_coste.select_dtypes(['object']).columns] = \
        df_total_coste.select_dtypes(['object']).apply(lambda x: x.astype('category'))


    df_coste.to_parquet(f'./data/main_raw/df_coste.parquet')


############ indicadores pestaña 3 y 4 de los excels

    df_total_indicadores = pd.DataFrame()

    for x in CCAA:
        for y in range(2 , 4):
            df = pd.read_excel(f'./data/main_raw_excel/CESEL_2018_{x}.xlsx' , sheet_name=y , header=10)
            df_total_indicadores = pd.concat([df_total_indicadores , df] , axis=0)


    df_indicadores=df_total_indicadores[['Provincia', 'Código Ente Principal','Tipo Ente Principal',
                                     'Nombre Ente Principal','Descripción',  'Unidades físicas de referencia', 'Nº unidades']]

    df_total_indicadores[df_total_indicadores.select_dtypes(['object']).columns] = \
                df_total_indicadores.select_dtypes(['object']).apply(lambda x: x.astype('category'))

    df_indicadores.to_parquet(f'./data/main_raw/df_indicadores.parquet')