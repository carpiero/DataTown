import pandas as pd
import geopandas

# df_indicadores_pob = pd.read_parquet(f'./data/processed/df_indicadores_pob.parquet')
# df_final_pob = pd.read_parquet('./data/processed/df_final_pob.parquet')
# df_final_pob_melt = pd.read_parquet('./data/processed/df_final_pob_melt.parquet')
# df_final_pob_melt_PC = pd.read_parquet('./data/processed/df_final_pob_melt_PC.parquet')
# df_indicadores_pob_pivot = pd.read_parquet('./data/processed/df_indicadores_pob_pivot.parquet')

df_indicadores_pob = pd.read_parquet(f'./data/main_processed/df_indicadores_pob.parquet')
df_final_pob = pd.read_parquet('./data/main_processed/df_final_pob.parquet')
df_final_pob_melt = pd.read_parquet('./data/main_processed/df_final_pob_melt.parquet')
df_final_pob_melt_PC = pd.read_parquet('./data/main_processed/df_final_pob_melt_PC.parquet')
df_indicadores_pob_pivot = pd.read_parquet('./data/main_processed/df_indicadores_pob_pivot.parquet')

########## dropdown

df_final_pob_dropdown=pd.read_parquet('./data/main_processed/df_final_pob_dropdown.parquet')
df_final_pob_dropdown_c=pd.read_parquet('./data/main_processed/df_final_pob_dropdown_c.parquet')

######### text

df_final_pob_poblaciontext=pd.read_parquet('./data/main_processed/df_final_pob_poblaciontext.parquet')




#################

# df_final_pob_melt_PC['Descripción'] = df_final_pob_melt_PC['Descripción'].str.replace(r'^...' , '')


CCAA=sorted(df_final_pob['CCAA'].unique().to_list())
CCAA.insert(0, 'TODAS')
CCAA_dict = dict(zip(CCAA, CCAA))

prov=sorted(df_final_pob['Provincia'].unique().to_list())
prov.insert(0, 'TODAS')
PROV = dict(zip(prov, prov))

mun=sorted(df_final_pob['Nombre Ente Principal'].unique().to_list())
mun.insert(0, 'TODOS')
MUNICIPIOS = dict(zip(mun, mun))

pdc=sorted(list(df_final_pob_melt['Descripción'].unique()))
pdc.insert(0, 'TODOS')
PDC = dict(zip(pdc, pdc))

###########################   main graph

df_table_c = df_indicadores_pob.pivot_table(index=['CCAA','Descripción' , 'Unidades físicas de referencia'] ,
                                                      values=['Nº unidades'] ,
                                                      aggfunc=sum).reset_index()



df_table_n = df_indicadores_pob.pivot_table(index=['Descripción','Unidades físicas de referencia'],values=['Nº unidades'],
                                                      aggfunc=sum).reset_index()




df_table_p=df_indicadores_pob.pivot_table(index=['Provincia','Descripción' , 'Unidades físicas de referencia'] ,
                                                      values=['Nº unidades'] ,
                                                      aggfunc=sum).reset_index()

df_table_m=df_indicadores_pob_pivot


###########################   individual graph

df_n = df_final_pob_melt.pivot_table(index=['Descripción'] , values=['coste_efectivo'] , aggfunc=sum).sort_values(
            by='coste_efectivo' , ascending=False).reset_index()
div = df_final_pob['Población 2018'].sum()
df_n['coste_efectivo_new'] = df_n.apply(lambda new: round(new['coste_efectivo'] / div , ) , axis=1)

df_c= df_final_pob_melt.pivot_table(index=['CCAA' , 'Descripción'] , values=['coste_efectivo'] ,
                    aggfunc=sum).sort_values(by='coste_efectivo' , ascending=False).reset_index()

df_p = df_final_pob_melt.pivot_table(index=['Provincia' , 'Descripción'] , values=['coste_efectivo'] ,
                                           aggfunc=sum).sort_values(by='coste_efectivo' , ascending=False).reset_index()


###########################   count graph

df_count_c=df_final_pob.pivot_table(index=['CCAA'] ,values=['TOTAL','Población 2018'] ,aggfunc=sum).reset_index()
df_count_c['PC_TOTAL'] = df_count_c.apply(lambda new: round(new['TOTAL']/new['Población 2018'],), axis=1)
df_count_c=df_count_c.sort_values(by='PC_TOTAL',ascending=False)
df_count_c['CCAA'] = df_count_c['CCAA'].astype('object')


pob_c=df_final_pob.pivot_table(index=['CCAA'] ,values=['Población 2018'] ,aggfunc=sum).reset_index()
df_count_c_pc=df_final_pob_melt.pivot_table(index=['CCAA','Descripción'] ,values=['coste_efectivo'] ,aggfunc=sum).reset_index()
df_count_c_pc = pd.merge(df_count_c_pc, pob_c, on='CCAA', how='left')
df_count_c_pc['PC_TOTAL'] = df_count_c_pc.apply(lambda new: round(new['coste_efectivo']/new['Población 2018'],), axis=1)
df_count_c_pc['CCAA'] = df_count_c_pc['CCAA'].astype('object')

df_count_p=df_final_pob.pivot_table(index=['Provincia'] ,values=['TOTAL','Población 2018'] ,aggfunc=sum).reset_index()
df_count_p['PC_TOTAL'] = df_count_p.apply(lambda new: round(new['TOTAL']/new['Población 2018'],), axis=1)
df_count_p['Provincia'] = df_count_p['Provincia'].astype('object')

pob_p=df_final_pob.pivot_table(index=['Provincia'] ,values=['Población 2018'] ,aggfunc=sum).reset_index()
df_count_p_pc=df_final_pob_melt.pivot_table(index=['Provincia','Descripción'] ,values=['coste_efectivo'] ,aggfunc=sum).reset_index()
df_count_p_pc = pd.merge(df_count_p_pc, pob_p, on='Provincia', how='left')
df_count_p_pc['PC_TOTAL'] = df_count_p_pc.apply(lambda new: round(new['coste_efectivo']/new['Población 2018'],), axis=1)
df_count_p_pc['Provincia'] = df_count_p_pc['Provincia'].astype('object')

###########################   map graph

import json

# with open('./data/processed/shapefiles_espana_municipios.geojson') as response:
#     counties = json.load(response)

with open('./data/main_raw/shapefiles_espana_municipios.geojson') as response:
    counties = json.load(response)


# CCAA_CO = pd.read_parquet('./data/processed/CCAA_CO.parquet')
# PROV_CO = pd.read_parquet('./data/processed/PROV_CO.parquet')
# MUNI_CO = pd.read_parquet('./data/processed/MUNI_CO.parquet')
#
# df_zoom_pob = geopandas.read_file('./data/processed/shapefiles_espana_municipios.geojson')

CCAA_CO = pd.read_parquet('./data/main_processed/CCAA_CO.parquet')
PROV_CO = pd.read_parquet('./data/main_processed/PROV_CO.parquet')
MUNI_CO = pd.read_parquet('./data/main_processed/MUNI_CO.parquet')

df_zoom_pob = geopandas.read_file('./data/main_raw/shapefiles_espana_municipios.geojson')

df_muni_co_zoom=df_final_pob[['CCAA','Provincia','Nombre Ente Principal','codigo_geo','Población 2018']]
df_muni_co_zoom[df_muni_co_zoom.select_dtypes(['category']).columns] = \
            df_muni_co_zoom.select_dtypes(['category']).apply(lambda x: x.astype('object'))

df_muni_co_zoom['codigo_geo'] = df_muni_co_zoom['codigo_geo'].astype('int64')
df_zoom_pob['codigo_geo']= df_zoom_pob['f_codmun']
df_zoom_pob = pd.merge(df_zoom_pob , df_muni_co_zoom, on='codigo_geo', how='left')



