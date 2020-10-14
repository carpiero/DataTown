import pandas as pd
from p_acquisition import m_acquisition as mac
from p_pivot_hard_load import m_pivot_hard_load as mphl
from p_graphic import m_graphic as mg


def main(df_coste,df_indicadores):

    mac.acquire(df_coste,df_indicadores)
    mphl.pivot()
    mg.graphic()




if __name__ == '__main__':
    df_coste = pd.read_parquet(f'./data/main_raw/df_coste.parquet')
    df_indicadores = pd.read_parquet(f'./data/main_raw/df_indicadores.parquet')

    main(df_coste,df_indicadores)


