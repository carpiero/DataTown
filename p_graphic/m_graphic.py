import pandas as pd
import numpy as np

#####   Graphics

def graphic():
    df_final_pob = pd.read_parquet('./data/main_processed/df_final_pob.parquet')
    df_final_pob_dropdown=df_final_pob[['CCAA','Provincia','Nombre Ente Principal']]

    df_final_pob_dropdown.to_parquet('./data/main_processed/df_final_pob_dropdown.parquet')


    df_final_pob_dropdown_c = pd.read_parquet('./data/main_processed/df_final_pob_melt_PC.parquet')
    df_final_pob_dropdown_c = df_final_pob_dropdown_c.loc[df_final_pob_dropdown_c['coste_efectivo_PC']>=1]
    df_final_pob_dropdown_c = df_final_pob_dropdown_c[['Nombre Ente Principal','Descripción']]
    df_final_pob_dropdown_c['Descripción'] = df_final_pob_dropdown_c['Descripción'].str.replace(r'^...' , '')

    df_final_pob_dropdown_c.to_parquet('./data/main_processed/df_final_pob_dropdown_c.parquet')


########   Población Text

    df_final_pob_poblaciontext=df_final_pob[['CCAA','Provincia','Nombre Ente Principal','Población 2018']]
    df_final_pob_poblaciontext.to_parquet('./data/main_processed/df_final_pob_poblaciontext.parquet')












