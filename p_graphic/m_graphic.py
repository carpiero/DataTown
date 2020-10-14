import pandas as pd
import numpy as np

#####   Graphics

def graphic():
    df_final_pob = pd.read_parquet('./data/main_processed/df_final_pob.parquet')
    df_final_pob_dropdown=df_final_pob[['CCAA','Provincia','Nombre Ente Principal']]

    df_final_pob_dropdown.to_parquet('./data/main_processed/df_final_pob_dropdown.parquet')

