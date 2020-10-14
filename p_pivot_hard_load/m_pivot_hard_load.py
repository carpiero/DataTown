import pandas as pd
import numpy as np

#####   Pivot indicadores

def pivot():
    df_indicadores_pob=pd.read_parquet('./data/main_processed/df_indicadores_pob.parquet')

    print('last')
    df_indicadores_pob_pivot = df_indicadores_pob.pivot_table(index=['Nombre Ente Principal' , 'Descripción' ,
                'Unidades físicas de referencia'] , values=['Nº unidades'] ,aggfunc=np.sum).reset_index()

    df_indicadores_pob_pivot = df_indicadores_pob_pivot.loc[df_indicadores_pob_pivot['Nº unidades'] > 0]

    df_indicadores_pob_pivot.to_parquet('./data/main_processed/df_indicadores_pob_pivot.parquet')
    print('last')
