import pandas as pd
import geopandas

df_indicadores_pob = pd.read_parquet(f'../data/processed/df_indicadores_pob.parquet')
df_final_pob = pd.read_parquet('../data/processed/df_final_pob.parquet')
df_final_pob_melt = pd.read_parquet('../data/processed/df_final_pob_melt.parquet')
df_final_pob_melt_PC = pd.read_parquet('../data/processed/df_final_pob_melt_PC.parquet')


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

###########################    main graph

df_table_c = df_indicadores_pob.pivot_table(index=['CCAA','Descripción' , 'Unidades físicas de referencia'] ,
                                                      values=['Nº unidades'] ,
                                                      aggfunc=sum).reset_index()



df_table_n = df_indicadores_pob.pivot_table(index=['Descripción','Unidades físicas de referencia'],values=['Nº unidades'],
                                                      aggfunc=sum).reset_index()




df_table_p=df_indicadores_pob.pivot_table(index=['Provincia','Descripción' , 'Unidades físicas de referencia'] ,
                                                      values=['Nº unidades'] ,
                                                      aggfunc=sum).reset_index()


############################ individual graph

df_n = df_final_pob_melt.pivot_table(index=['Descripción'] , values=['coste_efectivo'] , aggfunc=sum).sort_values(
            by='coste_efectivo' , ascending=False).reset_index()
div = df_final_pob['Población 2018'].sum()
df_n['coste_efectivo_new'] = df_n.apply(lambda new: round(new['coste_efectivo'] / div , ) , axis=1)

df_c= df_final_pob_melt.pivot_table(index=['CCAA' , 'Descripción'] , values=['coste_efectivo'] ,
                    aggfunc=sum).sort_values(by='coste_efectivo' , ascending=False).reset_index()

df_p = df_final_pob_melt.pivot_table(index=['Provincia' , 'Descripción'] , values=['coste_efectivo'] ,
                                           aggfunc=sum).sort_values(by='coste_efectivo' , ascending=False).reset_index()


############################################# count graph

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

################################### map

import json

with open('../data/processed/shapefiles_espana_municipios.geojson') as response:
    counties = json.load(response)

CCAA_CO = pd.read_parquet('../data/processed/CCAA_CO.parquet')
PROV_CO = pd.read_parquet('../data/processed/PROV_CO.parquet')
MUNI_CO = pd.read_parquet('../data/processed/MUNI_CO.parquet')

df_zoom_pob = geopandas.read_file('../data/processed/shapefiles_espana_municipios.geojson')

df_muni_co_zoom=df_final_pob[['CCAA','Provincia','Nombre Ente Principal','codigo_geo']]
df_muni_co_zoom[df_muni_co_zoom.select_dtypes(['category']).columns] = \
            df_muni_co_zoom.select_dtypes(['category']).apply(lambda x: x.astype('object'))

df_muni_co_zoom['codigo_geo'] = df_muni_co_zoom['codigo_geo'].astype('int64')
df_zoom_pob['codigo_geo']= df_zoom_pob['f_codmun']
df_zoom_pob = pd.merge(df_zoom_pob , df_muni_co_zoom, on='codigo_geo', how='left')



# flake8: noqa

# # In[]:
# # Controls for webapp
# COUNTIES = {
#     "001": "Albany",
#     "003": "Allegany",
#     "005": "Bronx",
#     "007": "Broome",
#     "009": "Cattaraugus",
#     "011": "Cayuga",
#     "013": "Chautauqua",
#     "015": "Chemung",
#     "017": "Chenango",
#     "019": "Clinton",
#     "021": "Columbia",
#     "023": "Cortland",
#     "025": "Delaware",
#     "027": "Dutchess",
#     "029": "Erie",
#     "031": "Essex",
#     "033": "Franklin",
#     "035": "Fulton",
#     "037": "Genesee",
#     "039": "Greene",
#     "041": "Hamilton",
#     "043": "Herkimer",
#     "045": "Jefferson",
#     "047": "Kings",
#     "049": "Lewis",
#     "051": "Livingston",
#     "053": "Madison",
#     "055": "Monroe",
#     "057": "Montgomery",
#     "059": "Nassau",
#     "061": "New York",
#     "063": "Niagara",
#     "065": "Oneida",
#     "067": "Onondaga",
#     "069": "Ontario",
#     "071": "Orange",
#     "073": "Orleans",
#     "075": "Oswego",
#     "077": "Otsego",
#     "079": "Putnam",
#     "081": "Queens",
#     "083": "Rensselaer",
#     "085": "Richmond",
#     "087": "Rockland",
#     "089": "St. Lawrence",
#     "091": "Saratoga",
#     "093": "Schenectady",
#     "095": "Schoharie",
#     "097": "Schuyler",
#     "099": "Seneca",
#     "101": "Steuben",
#     "103": "Suffolk",
#     "105": "Sullivan",
#     "107": "Tioga",
#     "109": "Tompkins",
#     "111": "Ulster",
#     "113": "Warren",
#     "115": "Washington",
#     "117": "Wayne",
#     "119": "Westchester",
#     "121": "Wyoming",
#     "123": "Yates",
# }

# WELL_STATUSES = dict(
#     AC="Active",
#     AR="Application Received to Drill/Plug/Convert",
#     CA="Cancelled",
#     DC="Drilling Completed",
#     DD="Drilled Deeper",
#     DG="Drilling in Progress",
#     EX="Expired Permit",
#     IN="Inactive",
#     NR="Not Reported on AWR",
#     PA="Plugged and Abandoned",
#     PI="Permit Issued",
#     PB="Plugged Back",
#     PM="Plugged Back Multilateral",
#     RE="Refunded Fee",
#     RW="Released - Water Well",
#     SI="Shut-In",
#     TA="Temporarily Abandoned",
#     TR="Transferred Permit",
#     UN="Unknown",
#     UL="Unknown Located",
#     UM="Unknown Not Found",
#     VP="Voided Permit",
# )
#
# WELL_TYPES = dict(
#     BR="Brine",
#     Confidential="Confidential",
#     DH="Dry Hole",
#     DS="Disposal",
#     DW="Dry Wildcat",
#     GD="Gas Development",
#     GE="Gas Extension",
#     GW="Gas Wildcat",
#     IG="Gas Injection",
#     IW="Oil Injection",
#     LP="Liquefied Petroleum Gas Storage",
#     MB="Monitoring Brine",
#     MM="Monitoring Miscellaneous",
#     MS="Monitoring Storage",
#     NL="Not Listed",
#     OB="Observation Well",
#     OD="Oil Development",
#     OE="Oil Extension",
#     OW="Oil Wildcat",
#     SG="Stratigraphic",
#     ST="Storage",
#     TH="Geothermal",
#     UN="Unknown",
# )
#
# WELL_COLORS = dict(
#     GD="#FFEDA0",
#     GE="#FA9FB5",
#     GW="#A1D99B",
#     IG="#67BD65",
#     OD="#BFD3E6",
#     OE="#B3DE69",
#     OW="#FDBF6F",
#     ST="#FC9272",
#     BR="#D0D1E6",
#     MB="#ABD9E9",
#     IW="#3690C0",
#     LP="#F87A72",
#     MS="#CA6BCC",
#     Confidential="#DD3497",
#     DH="#4EB3D3",
#     DS="#FFFF33",
#     DW="#FB9A99",
#     MM="#A6D853",
#     NL="#D4B9DA",
#     OB="#AEB0B8",
#     SG="#CCCCCC",
#     TH="#EAE5D9",
#     UN="#C29A84",
# )


