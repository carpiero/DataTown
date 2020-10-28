import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings('ignore')



# acquisition functions

def get_tables(df_coste,df_indicadores):
    df_coste.loc[(df_coste['Descripción'] == 'Abastos, mercados, lonjas ') & (
                df_coste['Nombre Ente Principal'] == 'Huércal de Almería') , 'coste_efectivo'] = 0

    df_coste.loc[(df_coste['Descripción'] == 'Urbanismo: planeamiento, gestión, ejecución y disciplina urbanística') & (
                df_coste['Nombre Ente Principal'] == 'Rianxo') , 'coste_efectivo'] = 78388.85

    df_indicadores.loc[ (df_indicadores['Descripción'] == 'Policía local') & (df_indicadores['Unidades físicas de referencia'] == \
         'Nº efectivos asignados al servicio') & (df_indicadores['Código Ente Principal'] == '05-35-021-AA-000') , 'Nº unidades'] = 0

#####   homónimos

    ff = [df_coste, df_indicadores]

    for x in ff:
        x['Nombre Ente Principal'] = x['Nombre Ente Principal'].astype('object')
        x.loc[x['Código Ente Principal'] == '07-47-232-AA-000' , 'Nombre Ente Principal'] = 'Zarza (La) (Valladolid)'
        x.loc[x['Código Ente Principal'] == '10-06-162-AA-000' , 'Nombre Ente Principal'] = 'Zarza (La) (Badajoz)'
        x.loc[x['Código Ente Principal'] == '01-21-018-AA-000' , 'Nombre Ente Principal'] = 'Campillo (El) (Huelva)'
        x.loc[x['Código Ente Principal'] == '07-47-031-AA-000' , 'Nombre Ente Principal'] = 'Campillo (El) (Valladolid)'
        x.loc[x['Código Ente Principal'] == '09-17-197-AA-000' , 'Nombre Ente Principal'] = 'Torrent (Girona)'
        x.loc[x['Código Ente Principal'] == '17-46-244-AA-000' , 'Nombre Ente Principal'] = 'Torrent (Valencia)'
        x.loc[x['Código Ente Principal'] == '03-33-037-AA-000' , 'Nombre Ente Principal'] = 'Mieres (Asturias)'
        x.loc[x['Código Ente Principal'] == '09-17-105-AA-000' , 'Nombre Ente Principal'] = 'Mieres (Girona)'
        x.loc[x['Código Ente Principal'] == '06-39-099-AA-000' , 'Nombre Ente Principal'] = 'Villaescusa (Cantabria)'
        x.loc[x['Código Ente Principal'] == '07-49-241-AA-000' , 'Nombre Ente Principal'] = 'Villaescusa (Zamora)'
        x.loc[x['Código Ente Principal'] == '07-37-279-AA-000' , 'Nombre Ente Principal'] = 'Sancti-Spíritus (Salamanca)'
        x.loc[x['Código Ente Principal'] == '10-06-118-AA-000' , 'Nombre Ente Principal'] = 'Sancti-Spíritus (Badajoz)'
        x.loc[x['Código Ente Principal'] == '09-17-030-AA-000' , 'Nombre Ente Principal'] = 'Cabanes (Girona)'
        x.loc[x['Código Ente Principal'] == '17-12-033-AA-000' , 'Nombre Ente Principal'] = 'Cabanes (Castellón)'
        x['Nombre Ente Principal'] = x['Nombre Ente Principal'].astype('category')

#####   Cambio Descripción

    for x in ff:

        x['Descripción'] = x['Descripción'].astype('object')

        x.loc[x['Descripción'] == 'Abastecimiento domiciliario de agua potable' , 'Descripción'] = 'Abastecimiento de agua potable'

        x.loc[x['Descripción'] == 'Conservación, mantenimiento y vigilancia de los edificios de titularidad local destinados a centros públicos de educación infantil, de educación primaria o de educación especial' , 'Descripción'] = 'Conservación, mantenimiento y vigilancia de los edificios destinados a educación'

        x.loc[x['Descripción'] == 'Cooperar con las Administraciones educativas correspondientes en la obtención de los solares necesarios para la construcción de nuevos centros docentes' ,
                     'Descripción'] = 'Cooperar con las Administraciones educativas en la obtención de solares'

        x.loc[x['Descripción'] == 'Evaluación e información de situaciones de necesidad social y la atención inmediata a personas en situación o riesgo de exclusión social' ,
                     'Descripción'] = 'Necesidad social y atención inmediata a personas en riesgo de exclusión social'

        x.loc[x['Descripción'] == 'Medio ambiente urbano: Protección contra la contaminación acústica, lumínica y atmosférica en las zonas urbanas' ,
                     'Descripción'] = 'Protección contra contaminación acústica, lumínica y atmosférica'

        x.loc[x['Descripción'] == 'Promoción en su término municipal de la participación de los ciudadanos en el uso eficiente y sostenible de las tecnologías de la información y las comunicaciones' ,
                     'Descripción'] = 'Promoción de la participación de los ciudadanos en las T.I.C.'

        x.loc[x['Descripción'] == 'Promoción y gestión de la vivienda de protección pública con criterios de sostenibilidad financiera' ,
                     'Descripción'] = 'Promoción y gestión de la vivienda de protección pública'

        x['Descripción'] = x['Descripción'].astype('category')

#####   Df_coste PIVOT

    df_coste_pivot = df_coste.pivot_table(index=['Código Ente Principal'] , values=['coste_efectivo'] ,
                                          columns=['Descripción'] , aggfunc=np.sum)
    df_coste_pivot.columns = df_coste_pivot.columns.droplevel()
    df_coste_pivot.columns = df_coste_pivot.columns.tolist()
    df_coste_pivot.reset_index(inplace=True)
    more_columns = df_coste.groupby(by=['Código Ente Principal' ])[
        ['Provincia' , 'Tipo Ente Principal' , 'Nombre Ente Principal']].min().reset_index()
    df_coste_pivot['Provincia'] = more_columns['Provincia']
    df_coste_pivot['Tipo Ente Principal'] = more_columns['Tipo Ente Principal']
    df_coste_pivot['Nombre Ente Principal'] = more_columns['Nombre Ente Principal']

    cols = df_coste_pivot.columns.tolist()
    cols = cols[-3:] + cols[:-3]
    df_coste_pivot = df_coste_pivot[cols]


    df_coste_pivot['codigoM'] = df_coste_pivot['Código Ente Principal']
    df_coste_pivot['codigoM'] = df_coste_pivot['codigoM'].str.replace(r'^.{3}|.{7}$|-' , '')
    df_indicadores['codigoM'] = df_indicadores['Código Ente Principal']
    df_indicadores['codigoM'] = df_indicadores['codigoM'].str.replace(r'^.{3}|.{7}$|-' , '')

    df_final = df_coste_pivot.loc[(df_coste_pivot['Tipo Ente Principal'] == 'Ayuntamiento')].reset_index()
    df_final = df_final.drop(columns=['index'])
    df_indicadores = df_indicadores.loc[(df_indicadores['Tipo Ente Principal'] == 'Ayuntamiento')].reset_index()
    df_indicadores = df_indicadores.drop(columns=['index'])

#####   Población

    df_pob = pd.read_excel(f'./data/main_raw/Datos municipios.xlsx' , sheet_name=0 , header=0)
    df_pob = df_pob[['Población 2018' , 'superficie' , 'entidades singulares menores' , ' ']]
    df_pob['codigoM'] = df_pob[' ']
    df_pob['codigoM'] = df_pob['codigoM'].str.replace(r'\D' , '')

    df_pob.rename(columns={' ': 'Municipio'} , inplace=True)

    df_final_pob = pd.merge(df_final , df_pob , on='codigoM' , how='left')
    df_indicadores_pob = pd.merge(df_indicadores , df_pob , on='codigoM' , how='left')

    df_final_pob = df_final_pob.drop(columns=['superficie' ,'entidades singulares menores' , 'Municipio'])
    df_indicadores_pob = df_indicadores_pob.drop(columns=['superficie' ,'entidades singulares menores' , 'Municipio'])

    df_final_pob['TOTAL'] = range(df_final_pob.shape[0])
    df_final_pob['TOTAL'] = df_final_pob.apply(lambda new: df_final_pob.iloc[new['TOTAL'] , 4:47].sum() , axis=1)

    df_final_pob['Población 2018'] = df_final_pob['Población 2018'].astype('float64')
    df_indicadores_pob['Población 2018'] = df_indicadores_pob['Población 2018'].astype('float64')

#####   CCAA
    fff = [df_final_pob, df_indicadores_pob]

    for y in fff:

        y['CCAA'] = y['Código Ente Principal']

        y['CCAA'] = y['CCAA'].str.replace(r'.{14}$' , '')

        y.loc[y['CCAA'] == '01' , 'CCAA'] = 'Andalucía'
        y.loc[y['CCAA'] == '02' , 'CCAA'] = 'Aragón'
        y.loc[y['CCAA'] == '03' , 'CCAA'] = 'Principado de Asturias'
        y.loc[y['CCAA'] == '04' , 'CCAA'] = 'Illes Balears'
        y.loc[y['CCAA'] == '05' , 'CCAA'] = 'Canarias'
        y.loc[y['CCAA'] == '06' , 'CCAA'] = 'Cantabria'
        y.loc[y['CCAA'] == '07' , 'CCAA'] = 'Castilla y León'
        y.loc[y['CCAA'] == '08' , 'CCAA'] = 'Castilla-La Mancha'
        y.loc[y['CCAA'] == '09' , 'CCAA'] = 'Cataluña'
        y.loc[y['CCAA'] == '10' , 'CCAA'] = 'Extremadura'
        y.loc[y['CCAA'] == '11' , 'CCAA'] = 'Galicia'
        y.loc[y['CCAA'] == '12' , 'CCAA'] = 'Comunidad de Madrid'
        y.loc[y['CCAA'] == '13' , 'CCAA'] = 'Región de Murcia'
        y.loc[y['CCAA'] == '16' , 'CCAA'] = 'La Rioja'
        y.loc[y['CCAA'] == '17' , 'CCAA'] = 'Comunitat Valenciana'

    cols = df_final_pob.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df_final_pob = df_final_pob[cols]



#####   Por habitante

    cols = df_final_pob.columns.tolist()
    cols = cols[5:48] + cols[50:51]

    for x in cols:
        df_final_pob[f'PC_{x}'] = df_final_pob.apply(lambda new: new[x] / new['Población 2018'] , axis=1)

#####   Bidding

    df_final_pob['cohorte_pob'] = pd.cut(df_final_pob['Población 2018'] ,bins=[0 , 1000 , 2000 , 5000 , 10000 , 20000 , 50000 ,
                                        100000 , 200000 , 500000 , 6000000] ,
                            labels=['0-1.000' , '1.000-2.000' , '2.000-5.000' , '5.000-10.000' ,'10.000-20.000' ,'20.000-50.000' ,
                                    '50.000-100.000' , '100.000-200.000' , '200.000-500.000' , 'más de 500.000'])

#####   MAP
    ffff = [df_final_pob , df_indicadores_pob]

    for z in ffff:
        z['codigo_geo'] = z['codigoM']
        z['codigo_geo'] = z['codigo_geo'].str.replace(r'^0{1}' , '')

        z[z.select_dtypes(['object']).columns] = \
            z.select_dtypes(['object']).apply(lambda x: x.astype('category'))


#########################
    df_indicadores_pob=df_indicadores_pob.loc[df_indicadores_pob['Nº unidades']>0]

    df_final_pob.to_parquet('./data/main_processed/df_final_pob.parquet')
    df_indicadores_pob.to_parquet('./data/main_processed/df_indicadores_pob.parquet')

#########################

#####   Melt

    vars_melt=df_final_pob.columns[0:5].to_list()+df_final_pob.columns[95:96].to_list()+df_final_pob.columns[96:97].to_list()
    df_final_pob_melt=pd.melt(df_final_pob, id_vars=vars_melt,value_vars=df_final_pob.columns[5:48],
            var_name='Descripción',value_name='coste_efectivo')
    df_final_pob_melt['Descripción'] = df_final_pob_melt['Descripción'].astype('category')

    df_final_pob_melt=df_final_pob_melt.loc[df_final_pob_melt['coste_efectivo'] > 0]

    df_final_pob_melt.to_parquet('./data/main_processed/df_final_pob_melt.parquet')


    vars_melt = df_final_pob.columns[0:5].to_list() + df_final_pob.columns[95:96].to_list() + df_final_pob.columns[96:97].to_list()
    df_final_pob_melt_PC = pd.melt(df_final_pob , id_vars=vars_melt , value_vars=df_final_pob.columns[51:94].to_list() ,
                                   var_name='Descripción' , value_name='coste_efectivo_PC')

    df_pob_melt_PC = df_final_pob[['Código Ente Principal' , 'Población 2018']]
    df_final_pob_melt_PC = pd.merge(df_final_pob_melt_PC , df_pob_melt_PC , on='Código Ente Principal' , how='left')
    df_final_pob_melt_PC['Descripción'] = df_final_pob_melt_PC['Descripción'].str.replace(r'^...' , '')
    df_final_pob_melt_PC['Descripción'] = df_final_pob_melt_PC['Descripción'].astype('category')

    df_final_pob_melt_PC=df_final_pob_melt_PC.loc[df_final_pob_melt_PC['coste_efectivo_PC'] > 0]

    df_final_pob_melt_PC.to_parquet('./data/main_processed/df_final_pob_melt_PC.parquet')

######   MAP

    CCAA_CO = pd.read_csv('./data/main_raw/comunidades-autonomas-espanolas.csv', sep=';')

    CCAA_CO['LAT']=CCAA_CO['Geo Point']
    CCAA_CO['LON']=CCAA_CO['Geo Point']
    CCAA_CO['CCAA']=CCAA_CO['Comunidade Autónoma']

    CCAA_CO['LAT'] = CCAA_CO['LAT'].str.replace(r',.*', '')
    CCAA_CO['LON'] = CCAA_CO['LON'].str.replace(r'.*,', '')

    CCAA_CO.loc[CCAA_CO['Codigo']==1,'CCAA']='Andalucía'
    CCAA_CO.loc[CCAA_CO['Codigo']==2,'CCAA']='Aragón'
    CCAA_CO.loc[CCAA_CO['Codigo']==3,'CCAA']='Principado de Asturias'
    CCAA_CO.loc[CCAA_CO['Codigo']==4,'CCAA']='Illes Balears'
    CCAA_CO.loc[CCAA_CO['Codigo']==5,'CCAA']='Canarias'
    CCAA_CO.loc[CCAA_CO['Codigo']==6,'CCAA']='Cantabria'
    CCAA_CO.loc[CCAA_CO['Codigo']==7,'CCAA']='Castilla y León'
    CCAA_CO.loc[CCAA_CO['Codigo']==8,'CCAA']='Castilla-La Mancha'
    CCAA_CO.loc[CCAA_CO['Codigo']==9,'CCAA']='Cataluña'
    CCAA_CO.loc[CCAA_CO['Codigo']==11,'CCAA']='Extremadura'
    CCAA_CO.loc[CCAA_CO['Codigo']==12,'CCAA']='Galicia'
    CCAA_CO.loc[CCAA_CO['Codigo']==13,'CCAA']='Comunidad de Madrid'
    CCAA_CO.loc[CCAA_CO['Codigo']==14,'CCAA']='Región de Murcia'
    CCAA_CO.loc[CCAA_CO['Codigo']==17,'CCAA']='La Rioja'
    CCAA_CO.loc[CCAA_CO['Codigo']==10,'CCAA']='Comunitat Valenciana'

    CCAA_CO['LAT'] = CCAA_CO['LAT'].astype('float64')
    CCAA_CO['LON'] = CCAA_CO['LON'].astype('float64')

###########

    CCAA_CO.to_parquet('./data/main_processed/CCAA_CO.parquet')

##########

    MUNI_CO = pd.read_excel('./data/main_raw/MUNICIPIOS.xlsx')

    MUNI_CO['codigo_geo']=MUNI_CO['CODIGO']
    MUNI_CO=MUNI_CO[['codigo_geo', 'LONGITUD_ETRS89', 'LATITUD_ETRS89']]

    df_muni_co=df_final_pob[['Provincia','Nombre Ente Principal','codigo_geo']]
    df_muni_co['codigo_geo'] = df_muni_co['codigo_geo'].astype('int64')

    MUNI_CO = pd.merge(df_muni_co, MUNI_CO, on='codigo_geo', how='left')

    MUNI_CO.rename(columns={'LONGITUD_ETRS89': 'LON', 'LATITUD_ETRS89': 'LAT'},inplace=True)

###########

    MUNI_CO.to_parquet('./data/main_processed/MUNI_CO.parquet')

##########

    Filtro_PROV = (MUNI_CO['Nombre Ente Principal'] == 'Barcelona') | (MUNI_CO['Nombre Ente Principal'] == 'Madrid') | \
                  (MUNI_CO['Nombre Ente Principal'] == 'Vigo') | (
                              MUNI_CO['Nombre Ente Principal'] == 'Santiago de Compostela') | \
                  (MUNI_CO['Nombre Ente Principal'] == 'Lugo') | (MUNI_CO['Nombre Ente Principal'] == 'Maceda') | \
                  (MUNI_CO['Nombre Ente Principal'] == 'Oviedo') | (MUNI_CO['Nombre Ente Principal'] == 'Santander') | \
                  (MUNI_CO['Nombre Ente Principal'] == 'León') | (MUNI_CO['Nombre Ente Principal'] == 'Palencia') | \
                  (MUNI_CO['Nombre Ente Principal'] == 'Burgos') | (MUNI_CO['Nombre Ente Principal'] == 'Soria') | \
                  (MUNI_CO['Nombre Ente Principal'] == 'Valladolid') | (MUNI_CO['Nombre Ente Principal'] == 'Zamora') | \
                  (MUNI_CO['Nombre Ente Principal'] == 'Segovia') | (MUNI_CO['Nombre Ente Principal'] == 'Ávila') | \
                  (MUNI_CO['Nombre Ente Principal'] == 'Salamanca') | (
                              MUNI_CO['Nombre Ente Principal'] == 'Barcelona') | \
                  (MUNI_CO['Nombre Ente Principal'] == 'Logroño') | (MUNI_CO['Nombre Ente Principal'] == 'Huesca') | \
                  (MUNI_CO['Nombre Ente Principal'] == 'Zaragoza') | (MUNI_CO['Nombre Ente Principal'] == 'Teruel') | \
                  (MUNI_CO['Nombre Ente Principal'] == 'Girona') | (MUNI_CO['Nombre Ente Principal'] == 'Tarragona') | \
                  (MUNI_CO['Nombre Ente Principal'] == 'Lleida') | (MUNI_CO['Nombre Ente Principal'] == 'Barcelona') | \
                  (MUNI_CO['Nombre Ente Principal'] == 'Fuentelviejo') | (
                              MUNI_CO['Nombre Ente Principal'] == 'Cuenca') | \
                  (MUNI_CO['Nombre Ente Principal'] == 'Toledo') | (MUNI_CO['Nombre Ente Principal'] == 'Albacete') | \
                  (MUNI_CO['Nombre Ente Principal'] == 'Ciudad Real') | (MUNI_CO['Nombre Ente Principal'] == 'Huelva') | \
                  (MUNI_CO['Nombre Ente Principal'] == 'Murcia') | (MUNI_CO['Nombre Ente Principal'] == 'Cáceres') | \
                  (MUNI_CO['Nombre Ente Principal'] == 'Almendralejo') | (
                              MUNI_CO['Nombre Ente Principal'] == 'Sevilla') | \
                  (MUNI_CO['Nombre Ente Principal'] == 'Espera') | (MUNI_CO['Nombre Ente Principal'] == 'Jaén') | \
                  (MUNI_CO['Nombre Ente Principal'] == 'Córdoba') | (MUNI_CO['Nombre Ente Principal'] == 'Almería') | \
                  (MUNI_CO['Nombre Ente Principal'] == 'Málaga') | (MUNI_CO['Nombre Ente Principal'] == 'Granada') | \
                  (MUNI_CO['Nombre Ente Principal'] == 'Agost') | (MUNI_CO['Nombre Ente Principal'] == 'València') | \
                  (MUNI_CO['Nombre Ente Principal'] == 'Castelló de la Plana') | (
                              MUNI_CO['Nombre Ente Principal'] == 'Petra')

    PROV_CO = MUNI_CO.loc[Filtro_PROV]

############

    PROV_CO.to_parquet('./data/main_processed/PROV_CO.parquet')




def acquire(df_coste,df_indicadores):

    return get_tables(df_coste,df_indicadores)


















