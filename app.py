# Import required libraries
from plotly.subplots import make_subplots
import geopandas
import json
import dash
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.express as px
import re
import locale
import plotly.graph_objects as go
import warnings

warnings.filterwarnings('ignore')

#####   controls
from controls import  CCAA_dict, PROV,  MUNICIPIOS, PDC, df_final_pob_melt, df_final_pob, df_indicadores_pob, df_final_pob_dropdown,\
    df_final_pob_dropdown_c, df_final_pob_poblaciontext, df_final_pob_melt_PC, df_table_c, df_table_n, df_table_p, df_table_m,  df_n, \
    df_c, df_p, df_m, df_count_c, df_count_cn, df_count_c_pc, df_count_p, df_count_p_pc, df_count_c_new_n, df_count_p_new_n,df_count_m_pc,\
    counties, CCAA_CO, PROV_CO, MUNI_CO, df_zoom_pob, df_final_pob_round, df_final_pob_round_melt_PC, df_final_pob_round_melt_PC_object, df_cohorte,\
    df_final_pob_round_color, df_final_pob_round_melt_PC_object_color


############# RUN APP
app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])
server = app.server

################### google analytics

app.index_string = '''<!DOCTYPE html>
<html>
<head>
  <!-- Global site tag (gtag.js) - Google Analytics -->
    <script>(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
    (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
    })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

    ga('create', 'UA-180754723-1', 'auto');
    ga('send', 'pageview');
    </script>
  <!-- End Global Google Analytics -->
{%metas%}
<title>{%title%}</title>
{%favicon%}
{%css%}
    <meta name="description" content="DataTown | CESEL Interactive Dashboard" />
    <meta name="title" property="og:title" content="DataTown | CESEL Interactive Dashboard" />
    <meta property="og:type" content="DataTown | CESEL Interactive Dashboard" />
    <meta name="image" property="og:image" content="https://i.ibb.co/G7YqcK6/Captura-de-pantalla-2020-11-16-173417.jpg" />
    <meta name="description" property="og:description" content="DataTown | CESEL Interactive Dashboard" />
    <meta name="author" content="DataTown | CESEL Interactive Dashboard" />
</head>
<body>
{%app_entry%}
<footer>
{%config%}
{%scripts%}
{%renderer%}
</footer>
</body>
</html>
'''



##################    Create controls

CCAA_options = [ {"label": CCAA_dict[x], "value": x}for x in CCAA_dict]

PROV_type_options = [ {"label": PROV[x], "value":x}for x in PROV ]

mun_type_options = [{"label": MUNICIPIOS[x], "value": x}for x in MUNICIPIOS]

pdc_type_options = [{"label": PDC[x], "value": x} for x in PDC ]

locale.setlocale(locale.LC_ALL, '')

#####################################################3

# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                # html.Div(
                #     [
                #         html.Img(
                #             src=app.get_asset_url("25231.svg"),
                #             id="plotly-image",
                #             style={
                #                 "height": "60px",
                #                 "width": "auto",
                #                 "margin-bottom": "25px",
                #             },
                #         )
                #     ],
                #     className="one-third column",
                # ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Municipios",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Coste efectivo 2018", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),

                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("github.svg"),
                            id="plotly-image",
                            style={
                                "height": "25px",
                                "width": "auto",
                                'float': 'right','margin-top':'35px'
                            },
                        ),
                        html.A(
                            html.Button("Learn More", id="learn-more-button"),
                            href="https://github.com/carpiero/DataTown",
                        ),

                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "0px"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            "Comunidad Autónoma",
                            className="control_label",
                        ),
                        dcc.Dropdown(
                            id="CCAA_types" ,
                            options=CCAA_options ,
                            value=list(CCAA_dict.keys())[0] ,
                            className="dcc_control" ,
                        ) ,
                        html.P("Provincia", className="control_label"),
                        dcc.Dropdown(
                            id="PROV_types" ,
                            # options=well_type_options,
                            # value=list(WELL_TYPES.keys()),
                            className="dcc_control" ,
                        ) ,
                         html.P("Municipio", className="control_label"),
                        dcc.Dropdown(
                            id="municipio_types" ,
                            # options=mun_type_options,
                            # value=list(MUNICIPIOS.keys()),
                            className="dcc_control" ,
                        ) ,
                        html.P("Partida de Coste" , className="control_label") ,
                        dcc.Dropdown(
                            id="partida_de_coste_types" ,
                            # options=pdc_type_options,
                            # value=list(PDC.keys()),
                            className="dcc_control" ,
                        ) ,
                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.H6(id="Población_text") , html.P('Población')] ,
                                    id="Población" ,
                                    className="mini_container" ,
                                ) ,
                                html.Div(
                                    [html.H6(id="Coste_efectivo_Total_text") , html.P("Coste Total")] ,
                                    id="Coste_efectivo_Total" ,
                                    className="mini_container" ,
                                ) ,
                                html.Div(
                                    [html.H6(id='Coste_efectivo_por_Habitante_text') ,
                                     html.P("Coste por habitante")] ,
                                    id="Coste_efectivo_por_Habitante" ,
                                    className="mini_container" ,
                                ) ,
                                html.Div(
                                    [html.H6(id="Coste_efectivo_Medio_por_Habitante_text") ,
                                     html.P("Coste Medio por habitante nacional (estrato)")] ,
                                    id="Coste_efectivo_Medio_por_Habitante" ,
                                    className="mini_container" ,
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                        html.Div(
                            [dcc.Graph(id="percentil_graph",config = {'displayModeBar': False})],
                            id="countGraphContainer",
                            className="pretty_container",style={'min-height': '280px'},
                        ),
                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="indicadores_table",config = {'displayModeBar': False})],
                    className="pretty_container four columns",#style={'width': '34.2%'}
                ),
                html.Div(
                    [dcc.Graph(id="coste_bars_graph",config = {'displayModeBar': False})],
                    className="pretty_container eight columns",#style={'width': '65.8%'}
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="map_graph",config={'modeBarButtonsToRemove': ['lasso2d','pan2d'],'displaylogo': False})],
                    className="pretty_container eight columns",style={'min-height': '680px'},
                ),
                html.Div(
                    [dcc.Graph(id="box_graph",config = {'displayModeBar': False})],
                    className="pretty_container four columns",style={'min-height': '680px'},
                )
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

####################################################
app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="resize"),
    Output("output-clientside", "children"),
    [Input("percentil_graph", "figure")],
)


############# dropdown

@app.callback(
    [Output("PROV_types", "value"),Output("PROV_types", "options")], [Input("CCAA_types", "value")]
)
def display_status(CCAA_types):
    if CCAA_types == 'TODAS':
        value = list(PROV.keys())[0]
        options = PROV_type_options
    else:
        # prov_def=sorted(df_final_pob_melt.loc[df_final_pob_melt['CCAA']==CCAA_types,'Provincia'].unique().to_list())
        prov_def = sorted(df_final_pob_dropdown.loc[df_final_pob_dropdown['CCAA'] == CCAA_types , 'Provincia'].unique().to_list())
        prov_def.insert(0, 'TODAS')
        PROV_def = dict(zip(prov_def, prov_def))
        options = [ {"label": PROV_def[x], "value":x}for x in PROV_def ]
        value=list(PROV_def.keys())[0]

    return (value,options)



@app.callback(
    [Output("municipio_types", "value"),Output("municipio_types", "options")], [Input("CCAA_types", "value"),Input("PROV_types", "value")]
)
def display_status(CCAA_types, PROV_types):
    if CCAA_types == 'TODAS' and PROV_types == 'TODAS':
        value = list(MUNICIPIOS.keys())[0]
        options = mun_type_options

    elif CCAA_types != 'TODAS' and PROV_types == 'TODAS':
        # mun_def = sorted(df_final_pob_melt.loc[df_final_pob_melt['CCAA'] == CCAA_types ,'Nombre Ente Principal'].unique().to_list())
        mun_def = sorted(df_final_pob_dropdown.loc[df_final_pob_dropdown['CCAA'] == CCAA_types , 'Nombre Ente Principal'].unique().to_list())
        mun_def.insert(0 , 'TODOS')
        MUN_def = dict(zip(mun_def , mun_def))
        options = [{"label": MUN_def[x] , "value": x} for x in MUN_def]
        value = list(MUN_def.keys())[0]

    else:
        # mun_def =sorted(df_final_pob_melt.loc[df_final_pob_melt['Provincia']==PROV_types,'Nombre Ente Principal'].unique().to_list())
        mun_def = sorted(df_final_pob_dropdown.loc[df_final_pob_dropdown['Provincia'] == PROV_types , 'Nombre Ente Principal'].unique().to_list())
        mun_def.insert(0, 'TODOS')
        MUN_def = dict(zip(mun_def, mun_def))
        options = [ {"label": MUN_def[x], "value":x}for x in MUN_def ]
        value=list(MUN_def.keys())[0]

    return (value,options)


@app.callback(
    [Output("partida_de_coste_types", "value"),Output("partida_de_coste_types", "options")],
    [Input("CCAA_types", "value"), Input("PROV_types", "value"), Input("municipio_types", "value") ]
)
def display_status(CCAA_types, PROV_types,municipio_types):
    if  municipio_types != 'TODOS':
        pdc_def = sorted(list(df_final_pob_dropdown_c.loc[df_final_pob_dropdown_c['Nombre Ente Principal'] == municipio_types,
        'Descripción'].unique()))

        pdc_def.insert(0 , 'TODOS')
        PDC_def = dict(zip(pdc_def , pdc_def))
        options = [{"label": PDC_def[x] , "value": x} for x in PDC_def]
        value = list(PDC_def.keys())[0]

    else:
        value = list(PDC.keys())[0]
        options = pdc_type_options

    return (value,options)

@app.callback(Output("Población_text", "children"),
    [
        Input("CCAA_types" , "value") , Input("PROV_types" , "value") , Input("municipio_types" , "value")

    ],
)
def update_text(CCAA_types, PROV_types,municipio_types ):
    if CCAA_types == 'TODAS' and PROV_types == 'TODAS' and municipio_types == 'TODOS':
        value=df_final_pob_poblaciontext['Población 2018'].sum()

    elif CCAA_types != 'TODAS' and PROV_types == 'TODAS' and municipio_types == 'TODOS':
        value = df_final_pob_poblaciontext.loc[df_final_pob_poblaciontext['CCAA'] == CCAA_types,'Población 2018'].sum()

    elif PROV_types != 'TODAS' and municipio_types == 'TODOS':
        value = df_final_pob_poblaciontext.loc[df_final_pob_poblaciontext['Provincia']==PROV_types,'Población 2018'].sum()

    else:
        value=df_final_pob_poblaciontext.loc[df_final_pob_poblaciontext['Nombre Ente Principal'] == municipio_types,'Población 2018'].sum()

    value=locale.format_string('%.0f', value, True)

    return f'{value} hab.'


@app.callback (Output("Coste_efectivo_Total_text", "children"),
    [
        Input("CCAA_types" , "value") , Input("PROV_types" , "value") , Input("municipio_types" , "value"),
        Input("partida_de_coste_types" , "value")

    ],
)

def update_text(CCAA_types, PROV_types,municipio_types,partida_de_coste_types ):
    if partida_de_coste_types== 'TODOS':

        if CCAA_types == 'TODAS' and PROV_types == 'TODAS' and municipio_types == 'TODOS':
            value=df_final_pob_melt['coste_efectivo'].sum()

        elif CCAA_types != 'TODAS' and PROV_types == 'TODAS' and municipio_types == 'TODOS':
            value = df_final_pob_melt.loc[df_final_pob_melt['CCAA'] == CCAA_types,'coste_efectivo'].sum()

        elif PROV_types != 'TODAS' and municipio_types == 'TODOS':
            value = df_final_pob_melt.loc[df_final_pob_melt['Provincia']==PROV_types,'coste_efectivo'].sum()

        else:
            value=df_final_pob_melt.loc[df_final_pob_melt['Nombre Ente Principal'] == municipio_types,'coste_efectivo'].sum()

    else:
        if CCAA_types == 'TODAS' and PROV_types == 'TODAS' and municipio_types == 'TODOS':
            value=df_final_pob_melt.loc[df_final_pob_melt['Descripción'] == partida_de_coste_types,'coste_efectivo'].sum()

        elif CCAA_types != 'TODAS' and PROV_types == 'TODAS' and municipio_types == 'TODOS':
            value = df_final_pob_melt.loc[(df_final_pob_melt['Descripción'] == partida_de_coste_types) &(df_final_pob_melt['CCAA'] == CCAA_types),'coste_efectivo'].sum()

        elif PROV_types != 'TODAS' and municipio_types == 'TODOS':
            value = df_final_pob_melt.loc[(df_final_pob_melt['Descripción'] == partida_de_coste_types) &(df_final_pob_melt['Provincia']==PROV_types),'coste_efectivo'].sum()

        else:
            value=df_final_pob_melt.loc[(df_final_pob_melt['Descripción'] == partida_de_coste_types) &(df_final_pob_melt['Nombre Ente Principal'] == municipio_types),'coste_efectivo'].sum()



    value=locale.format_string('%.0f', round(value,0), True)

    return f'{value} €'

@app.callback (Output("Coste_efectivo_por_Habitante_text", "children"),
    [
        Input("Población_text", "children") , Input("Coste_efectivo_Total_text", "children")

    ],
)
def update_text(Población_text, Coste_efectivo_Total_text):
    if int(''.join(re.findall(r'\d' , Coste_efectivo_Total_text))) > 0:

        pob=int(''.join(re.findall(r'\d' , Población_text)))
        cost=int(''.join(re.findall(r'\d' , Coste_efectivo_Total_text)))

        value= cost/pob

    else:
        value=0

    value = locale.format_string('%.0f' , round(value,0) , True)

    return f'{value} €/hab.'


@app.callback (Output("Coste_efectivo_Medio_por_Habitante_text", "children"),
    [
        Input("CCAA_types" , "value") , Input("PROV_types" , "value") , Input("municipio_types" , "value") ,
        Input("partida_de_coste_types" , "value")

    ],
)
def update_text(CCAA_types, PROV_types,municipio_types,partida_de_coste_types ):
    if partida_de_coste_types== 'TODOS':

        if CCAA_types == 'TODAS' and PROV_types == 'TODAS' and municipio_types == 'TODOS':
            value=df_final_pob_melt['coste_efectivo'].sum()/df_final_pob['Población 2018'].sum()

        elif CCAA_types != 'TODAS' and PROV_types == 'TODAS' and municipio_types == 'TODOS':
            value = df_final_pob_melt['coste_efectivo'].sum()/df_final_pob['Población 2018'].sum()

        elif CCAA_types != 'TODAS' and PROV_types != 'TODAS' and municipio_types == 'TODOS':
            value = df_final_pob_melt.loc[df_final_pob_melt['CCAA'] == CCAA_types,'coste_efectivo'].sum()\
            / df_final_pob.loc[df_final_pob['CCAA'] == CCAA_types,'Población 2018'].sum()

        elif CCAA_types == 'TODAS' and PROV_types != 'TODAS' and municipio_types == 'TODOS':
            value = df_final_pob_melt['coste_efectivo'].sum()/df_final_pob['Población 2018'].sum()

        else:
            cohorte=df_cohorte.loc[df_cohorte['Nombre Ente Principal'] == municipio_types , 'cohorte_pob']\
                          .unique().to_list()[0]

            value=df_final_pob_melt.loc[df_final_pob_melt['cohorte_pob'] == cohorte,'coste_efectivo'].sum() \
                    /df_final_pob.loc[df_final_pob['cohorte_pob'] == cohorte , 'Población 2018'].sum()

    else:
        if CCAA_types == 'TODAS' and PROV_types == 'TODAS' and municipio_types == 'TODOS':
            value=df_final_pob_melt.loc[df_final_pob_melt['Descripción'] == partida_de_coste_types,'coste_efectivo'].sum()\
                   /df_final_pob['Población 2018'].sum()

        elif CCAA_types != 'TODAS' and PROV_types == 'TODAS' and municipio_types == 'TODOS':
            value = df_final_pob_melt.loc[df_final_pob_melt['Descripción'] == partida_de_coste_types,'coste_efectivo'].sum()\
                   /df_final_pob['Población 2018'].sum()

        elif CCAA_types != 'TODAS' and PROV_types != 'TODAS' and municipio_types == 'TODOS':
             value = df_final_pob_melt.loc[(df_final_pob_melt['CCAA'] == CCAA_types)&(df_final_pob_melt['Descripción'] == partida_de_coste_types), 'coste_efectivo'].sum() \
                    / df_final_pob.loc[df_final_pob['CCAA'] == CCAA_types , 'Población 2018'].sum()

        elif CCAA_types == 'TODAS' and PROV_types != 'TODAS' and municipio_types == 'TODOS':
            value= df_final_pob_melt.loc[df_final_pob_melt['Descripción'] == partida_de_coste_types , 'coste_efectivo'].sum() \
            / df_final_pob['Población 2018'].sum()

        else:
            cohorte =df_cohorte.loc[df_cohorte['Nombre Ente Principal'] == municipio_types , 'cohorte_pob'] \
                .unique().to_list()[0]
            value = np.median(df_final_pob_melt_PC.loc[(df_final_pob_melt_PC['cohorte_pob'] == cohorte) & \
                    (df_final_pob_melt_PC['Descripción'] == f'{partida_de_coste_types}') & (df_final_pob_melt_PC['coste_efectivo_PC'] > 0) , 'coste_efectivo_PC'])

            # value=df_final_pob_melt.loc[(df_final_pob_melt['cohorte_pob'] == cohorte) & (df_final_pob_melt['Descripción'] == partida_de_coste_types), 'coste_efectivo'].sum() \
            #                     / df_final_pob.loc[df_final_pob['cohorte_pob'] == cohorte , 'Población 2018'].sum()

    value=locale.format_string('%.0f', round(value,0), True)

    return f'{value} €/hab.'




################   percentil_graph graph
@app.callback(
    Output("percentil_graph", "figure"),
    [
        Input("CCAA_types" , "value") , Input("PROV_types" , "value") , Input("municipio_types" , "value") ,
        Input("partida_de_coste_types" , "value")
    ],[State("indicadores_table", "relayoutData")]
    # [State("lock_selector", "value"), State("indicadores_table", "relayoutData")],
)
def make_percentil_graph_figure(CCAA_types, PROV_types,municipio_types,partida_de_coste_types, indicadores_table):
    if partida_de_coste_types == 'TODOS':
        if CCAA_types == 'TODAS' and PROV_types == 'TODAS' and municipio_types == 'TODOS':
            df = df_count_cn
            df1=df.iloc[[0]]
            df2=df.iloc[[1]]
            df3=df.iloc[[2]]
            df4=df.iloc[[3]]

            fig = go.Figure()
            fig.add_trace(go.Bar(x=df1['CCAA'] , y=df1['PC_TOTAL'],name='Percentil 90',marker_color='#D62728'))
            fig.add_trace(go.Bar(x=df2['CCAA'] , y=df2['PC_TOTAL'],name='Percentil 75',marker_color='#3366CC'))
            fig.add_trace(go.Bar(x=df3['CCAA'] , y=df3['PC_TOTAL'],name='Percentil 25',marker_color='#2CA02C'))
            fig.add_trace(go.Bar(x=df4['CCAA'] , y=df4['PC_TOTAL'],name='Mediana',marker_color='rgb(217, 95, 2)'))


            fig.update_layout(title=f'Coste por habitante Total, Comunidades Autónomas')

        elif CCAA_types != 'TODAS' and PROV_types == 'TODAS' and municipio_types == 'TODOS':
            df = df_count_c_new_n
            df = df.append(df_count_c.loc[df_count_c['CCAA']==CCAA_types])
            df.iloc[3,0]=f'{CCAA_types}.'

            df1 = df.iloc[[0]]
            df2 = df.iloc[[1]]
            df3 = df.iloc[[2]]
            df4 = df.iloc[[3]]

            fig = go.Figure()
            fig.add_trace(go.Bar(x=df1['CCAA'] , y=df1['PC_TOTAL'] , name='Percentil 75' , marker_color='#D62728'))
            fig.add_trace(go.Bar(x=df2['CCAA'] , y=df2['PC_TOTAL'] , name='Mediana' , marker_color='#3366CC'))
            fig.add_trace(go.Bar(x=df3['CCAA'] , y=df3['PC_TOTAL'] , name='Percentil 25' , marker_color='#2CA02C'))
            fig.add_trace(go.Bar(x=df4['CCAA'] , y=df4['PC_TOTAL'] , name='Elección' , marker_color='rgb(217, 95, 2)'))
            fig.update_layout(title=f'Coste por habitante Total, Comunidades Autónomas')

        elif CCAA_types != 'TODAS' and PROV_types != 'TODAS' and municipio_types == 'TODOS':
            df = df_count_p_new_n
            df = df.append(df_count_p.loc[df_count_p['Provincia'] == PROV_types])

            df.iloc[3 , 0] = f'{PROV_types}.'

            df1 = df.iloc[[0]]
            df2 = df.iloc[[1]]
            df3 = df.iloc[[2]]
            df4 = df.iloc[[3]]

            fig = go.Figure()
            fig.add_trace(go.Bar(x=df1['Provincia'] , y=df1['PC_TOTAL'] , name='Percentil 75' , marker_color='#D62728'))
            fig.add_trace(go.Bar(x=df2['Provincia'] , y=df2['PC_TOTAL'] , name='Mediana' , marker_color='#3366CC'))
            fig.add_trace(go.Bar(x=df3['Provincia'] , y=df3['PC_TOTAL'] , name='Percentil 25' , marker_color='#2CA02C'))
            fig.add_trace(go.Bar(x=df4['Provincia'] , y=df4['PC_TOTAL'] , name='Elección' , marker_color='rgb(217, 95, 2)'))
            fig.update_layout(title=f'Coste por habitante Total, Provincias')

        elif CCAA_types == 'TODAS' and PROV_types != 'TODAS' and municipio_types == 'TODOS':
            df = df_count_p_new_n
            df = df.append(df_count_p.loc[df_count_p['Provincia'] == PROV_types])

            df.iloc[3 , 0] = f'{PROV_types}.'

            df1 = df.iloc[[0]]
            df2 = df.iloc[[1]]
            df3 = df.iloc[[2]]
            df4 = df.iloc[[3]]

            fig = go.Figure()
            fig.add_trace(go.Bar(x=df1['Provincia'] , y=df1['PC_TOTAL'] , name='Percentil 75' , marker_color='#D62728'))
            fig.add_trace(go.Bar(x=df2['Provincia'] , y=df2['PC_TOTAL'] , name='Mediana' , marker_color='#3366CC'))
            fig.add_trace(go.Bar(x=df3['Provincia'] , y=df3['PC_TOTAL'] , name='Percentil 25' , marker_color='#2CA02C'))
            fig.add_trace(go.Bar(x=df4['Provincia'] , y=df4['PC_TOTAL'] , name='Elección' , marker_color='rgb(217, 95, 2)'))
            fig.update_layout(title=f'Coste por habitante Total, Provincias')

        else:
            cohorte = df_cohorte.loc[df_cohorte['Nombre Ente Principal'] == municipio_types , 'cohorte_pob'].unique().to_list()[0]

            df = df_final_pob[['Nombre Ente Principal' , 'cohorte_pob' , 'PC_TOTAL']].loc[
                (df_final_pob['cohorte_pob'] == cohorte) & (df_final_pob['PC_TOTAL'] > 0)].sort_values(by='PC_TOTAL' ,ascending=False)
            df['Nombre Ente Principal'] = df['Nombre Ente Principal'].astype('object')
            df2 = df.loc[(df['PC_TOTAL'] == df['PC_TOTAL'].quantile(0.77 , interpolation='nearest')) | \
                         (df['PC_TOTAL'] == df['PC_TOTAL'].quantile(0.51 , interpolation='nearest')) | \
                         (df['PC_TOTAL'] == df['PC_TOTAL'].quantile(0.25 , interpolation='nearest'))]

            df2.drop_duplicates(subset='PC_TOTAL' , keep='last' , inplace=True)
            df2 = df2.append(df.loc[df['Nombre Ente Principal'] == municipio_types])
            df = df2
            df['PC_TOTAL'] = round(df['PC_TOTAL'] , )
            df.iloc[3 , 0] = f'{municipio_types}.'

            df1 = df.iloc[[0]]
            df2 = df.iloc[[1]]
            df3 = df.iloc[[2]]
            df4 = df.iloc[[3]]

            fig = go.Figure()
            fig.add_trace(go.Bar(x=df1['Nombre Ente Principal'] , y=df1['PC_TOTAL'] , name='Percentil 75' , marker_color='#D62728'))
            fig.add_trace(go.Bar(x=df2['Nombre Ente Principal'] , y=df2['PC_TOTAL'] , name='Mediana' , marker_color='#3366CC'))
            fig.add_trace(go.Bar(x=df3['Nombre Ente Principal'] , y=df3['PC_TOTAL'] , name='Percentil 25' , marker_color='#2CA02C'))
            fig.add_trace(go.Bar(x=df4['Nombre Ente Principal'] , y=df4['PC_TOTAL'] , name='Elección' , marker_color='rgb(217, 95, 2)'))
            fig.update_layout(xaxis=dict(title=f' Municipios con {cohorte} hab.'))
            fig.update_layout(title=f'Coste Mediano por habitante Total')



    else:
        if CCAA_types == 'TODAS' and PROV_types == 'TODAS' and municipio_types == 'TODOS':
            df = df_count_c_pc

            df = df.loc[df['Descripción'] == partida_de_coste_types].sort_values(by='PC_TOTAL' , ascending=False)

            df8 = df.loc[(df['PC_TOTAL'] == df['PC_TOTAL'].quantile(0.90 , interpolation='nearest')) | \
                        (df['PC_TOTAL'] == df['PC_TOTAL'].quantile(0.75 , interpolation='nearest')) | \
                        (df['PC_TOTAL'] == df['PC_TOTAL'].quantile(0.25 , interpolation='nearest'))]
            df8=df8.sort_values(by='PC_TOTAL' , ascending=False)

            df8=df8.append(df.loc[df['PC_TOTAL'] == df['PC_TOTAL'].quantile(0.50 , interpolation='nearest')])
            df8['PC_TOTAL'] = round(df8['PC_TOTAL'] , )
            df1 = df8.iloc[[0]]
            df2 = df8.iloc[[1]]
            df3 = df8.iloc[[2]]
            df4 = df8.iloc[[3]]

            fig = go.Figure()
            fig.add_trace(go.Bar(x=df1['CCAA'] , y=df1['PC_TOTAL'] , name='Percentil 90' , marker_color='#D62728'))
            fig.add_trace(go.Bar(x=df2['CCAA'] , y=df2['PC_TOTAL'] , name='Percentil 75' , marker_color='#3366CC'))
            fig.add_trace(go.Bar(x=df3['CCAA'] , y=df3['PC_TOTAL'] , name='Percentil 25' , marker_color='#2CA02C'))
            fig.add_trace(go.Bar(x=df4['CCAA'] , y=df4['PC_TOTAL'] , name='Mediana' , marker_color='rgb(217, 95, 2)'))
            fig.update_layout(title=f'Coste por hab. Total, CCCAA, {partida_de_coste_types}')


        elif CCAA_types != 'TODAS' and PROV_types == 'TODAS' and municipio_types == 'TODOS':
            df = df_count_c_pc

            df = df.loc[df['Descripción'] == partida_de_coste_types].sort_values(by='PC_TOTAL' , ascending=False)

            df8 = df.loc[(df['PC_TOTAL'] == df['PC_TOTAL'].quantile(0.75 , interpolation='nearest')) | \
                         (df['PC_TOTAL'] == df['PC_TOTAL'].quantile(0.50 , interpolation='nearest')) | \
                         (df['PC_TOTAL'] == df['PC_TOTAL'].quantile(0.25 , interpolation='nearest'))]
            df8 = df8.sort_values(by='PC_TOTAL' , ascending=False)

            df8 = df8.append(df.loc[df['CCAA'] == CCAA_types])
            df8['PC_TOTAL'] = round(df8['PC_TOTAL'] , )
            df8.iloc[3,0] = f'{CCAA_types}.'

            df1 = df8.iloc[[0]]
            df2 = df8.iloc[[1]]
            df3 = df8.iloc[[2]]
            df4 = df8.iloc[[3]]

            fig = go.Figure()
            fig.add_trace(go.Bar(x=df1['CCAA'] , y=df1['PC_TOTAL'] , name='Percentil 75' , marker_color='#D62728'))
            fig.add_trace(go.Bar(x=df2['CCAA'] , y=df2['PC_TOTAL'] , name='Mediana' , marker_color='#3366CC'))
            fig.add_trace(go.Bar(x=df3['CCAA'] , y=df3['PC_TOTAL'] , name='Percentil 25' , marker_color='#2CA02C'))
            fig.add_trace(go.Bar(x=df4['CCAA'] , y=df4['PC_TOTAL'] , name='Elección' , marker_color='rgb(217, 95, 2)'))
            fig.update_layout(title=f'Coste por hab. Total, CCCAA, {partida_de_coste_types}')

        elif CCAA_types != 'TODAS' and PROV_types != 'TODAS' and municipio_types == 'TODOS':
            df = df_count_p_pc

            df = df.loc[df['Descripción'] == partida_de_coste_types].sort_values(by='PC_TOTAL' , ascending=False)

            df8 = df.loc[(df['PC_TOTAL'] == df['PC_TOTAL'].quantile(0.75 , interpolation='nearest')) | \
                         (df['PC_TOTAL'] == df['PC_TOTAL'].quantile(0.50 , interpolation='nearest')) | \
                         (df['PC_TOTAL'] == df['PC_TOTAL'].quantile(0.25 , interpolation='nearest'))]
            df8 = df8.sort_values(by='PC_TOTAL' , ascending=False)

            df8 = df8.append(df.loc[df['Provincia'] == PROV_types])
            df8['PC_TOTAL'] = round(df8['PC_TOTAL'] , )
            df8.iloc[3 , 0] = f'{PROV_types}.'

            df1 = df8.iloc[[0]]
            df2 = df8.iloc[[1]]
            df3 = df8.iloc[[2]]
            df4 = df8.iloc[[3]]

            fig = go.Figure()
            fig.add_trace(go.Bar(x=df1['Provincia'] , y=df1['PC_TOTAL'] , name='Percentil 75' , marker_color='#D62728'))
            fig.add_trace(go.Bar(x=df2['Provincia'] , y=df2['PC_TOTAL'] , name='Mediana' , marker_color='#3366CC'))
            fig.add_trace(go.Bar(x=df3['Provincia'] , y=df3['PC_TOTAL'] , name='Percentil 25' , marker_color='#2CA02C'))
            fig.add_trace(go.Bar(x=df4['Provincia'] , y=df4['PC_TOTAL'] , name='Elección' , marker_color='rgb(217, 95, 2)'))
            fig.update_layout(title=f'Coste por hab. Total, Provincias, {partida_de_coste_types}')



        elif CCAA_types == 'TODAS' and PROV_types != 'TODAS' and municipio_types == 'TODOS':
            df = df_count_p_pc

            df = df.loc[df['Descripción'] == partida_de_coste_types].sort_values(by='PC_TOTAL' , ascending=False)

            df8 = df.loc[(df['PC_TOTAL'] == df['PC_TOTAL'].quantile(0.75 , interpolation='nearest')) | \
                         (df['PC_TOTAL'] == df['PC_TOTAL'].quantile(0.50 , interpolation='nearest')) | \
                         (df['PC_TOTAL'] == df['PC_TOTAL'].quantile(0.25 , interpolation='nearest'))]
            df8 = df8.sort_values(by='PC_TOTAL' , ascending=False)

            df8 = df8.append(df.loc[df['Provincia'] == PROV_types])
            df8['PC_TOTAL'] = round(df8['PC_TOTAL'] , )
            df8.iloc[3 , 0] = f'{PROV_types}.'

            df1 = df8.iloc[[0]]
            df2 = df8.iloc[[1]]
            df3 = df8.iloc[[2]]
            df4 = df8.iloc[[3]]

            fig = go.Figure()
            fig.add_trace(go.Bar(x=df1['Provincia'] , y=df1['PC_TOTAL'] , name='Percentil 75' , marker_color='#D62728'))
            fig.add_trace(go.Bar(x=df2['Provincia'] , y=df2['PC_TOTAL'] , name='Mediana' , marker_color='#3366CC'))
            fig.add_trace(go.Bar(x=df3['Provincia'] , y=df3['PC_TOTAL'] , name='Percentil 25' , marker_color='#2CA02C'))
            fig.add_trace(
                go.Bar(x=df4['Provincia'] , y=df4['PC_TOTAL'] , name='Elección' , marker_color='rgb(217, 95, 2)'))
            fig.update_layout(title=f'Coste por hab. Total, Provincias, {partida_de_coste_types}')

        else:
            cohorte = df_cohorte.loc[df_cohorte['Nombre Ente Principal'] == municipio_types , 'cohorte_pob'].unique().to_list()[0]

            df = df_count_m_pc.loc[(df_count_m_pc['cohorte_pob'] == cohorte)  & (df_count_m_pc['Descripción'] == partida_de_coste_types)].sort_values(by='coste_efectivo_PC' , ascending=False)
            # df['Nombre Ente Principal'] = df['Nombre Ente Principal'].astype('object')

            df2 = df.loc[(df['coste_efectivo_PC'] == df['coste_efectivo_PC'].quantile(0.76 , interpolation='nearest')) | \
                         (df['coste_efectivo_PC'] == df['coste_efectivo_PC'].quantile(0.53 , interpolation='nearest')) | \
                         (df['coste_efectivo_PC'] == df['coste_efectivo_PC'].quantile(0.22 , interpolation='nearest'))]

            df2 = df2.sort_values(by='coste_efectivo_PC' , ascending=False)
            df2.drop_duplicates(subset='coste_efectivo_PC' , keep='last' , inplace=True)
            df = df2.append(df.loc[df['Nombre Ente Principal'] == municipio_types])

            df.iloc[3 , 0] = f'{municipio_types}.'
            df['coste_efectivo_PC'] = round(df['coste_efectivo_PC'] , )

            df1 = df.iloc[[0]]
            df2 = df.iloc[[1]]
            df3 = df.iloc[[2]]
            df4 = df.iloc[[3]]

            fig = go.Figure()
            fig.add_trace(go.Bar(x=df1['Nombre Ente Principal'] , y=df1['coste_efectivo_PC'] , name='Percentil 75' , marker_color='#D62728'))
            fig.add_trace(go.Bar(x=df2['Nombre Ente Principal'] , y=df2['coste_efectivo_PC'] , name='Mediana' , marker_color='#3366CC'))
            fig.add_trace(go.Bar(x=df3['Nombre Ente Principal'] , y=df3['coste_efectivo_PC'] , name='Percentil 25' , marker_color='#2CA02C'))
            fig.add_trace(go.Bar(x=df4['Nombre Ente Principal'] , y=df4['coste_efectivo_PC'] , name='Elección' , marker_color='rgb(217, 95, 2)'))
            fig.update_layout(xaxis=dict(title=f'Municipios con {cohorte} hab.'))
            fig.update_layout(title=f'Coste Mediano por hab., {partida_de_coste_types}')

    fig.update_traces(texttemplate="%{y:,} €/h" , textposition='inside',textfont_size=13,
                      #marker_color=['#D62728', '#3366CC',  '#2CA02C', 'rgb(217, 95, 2)']
                      )
    fig.update_traces(marker_line_color='rgb(8,48,107)')




    fig.update_layout(margin=dict(l=10 , r=50 , t=50 , b=10),
                      xaxis_tickfont_size=12 ,
                      # xaxis_tickangle=90 ,
                      yaxis=dict(
                          title='Coste efectivo €/hab.' ,
                          titlefont_size=16 ,
                          tickfont_size=12 ,showticklabels=True,
                          color='rgb(50, 50, 50)',
                             ) ,
                      xaxis=dict(
                          titlefont_size=16 ,
                          tickfont_size=14 , showticklabels=True ,
                          gridcolor='black',
                          color='rgb(50, 50, 50)',
                            showgrid=False,showline=False,
                             ) ,

                      legend=dict(
                          x=1 ,
                          y=1 ,font_color='rgb(50, 50, 50)',
                          # bgcolor='rgba(255, 255, 255, 0)' ,
                          bgcolor='#eeeeee',
                          font_size=14, #bgcolor="#e5ecf6",bordercolor="Black",
                      ) ,
                      barmode='relative' ,
                      bargap=0.55 ,  # gap between bars of adjacent location coordinates.
                      # bargroupgap=0.1,  # gap between bars of the same location coordinate.
                      autosize=True,showlegend=True,paper_bgcolor="#F9F9F9",title_font_color='rgb(50, 50, 50)')

    fig.update_layout(yaxis=dict(gridcolor='#cacaca') ,
                      xaxis=dict(showline=True ,linecolor='#929292' ,linewidth=0.5),
                      plot_bgcolor="#F9F9F9")

    return fig




################    indicadores_table graph
@app.callback(
    Output("indicadores_table", "figure"),
    [
        Input("CCAA_types" , "value") , Input("PROV_types" , "value") , Input("municipio_types" , "value") ,
        Input("partida_de_coste_types" , "value")
    ],[State("indicadores_table", "relayoutData")]
    # [State("lock_selector", "value"), State("indicadores_table", "relayoutData")],
)
def make_indicadores_table_figure(CCAA_types, PROV_types,municipio_types,partida_de_coste_types, indicadores_table):
    if partida_de_coste_types == 'TODOS':
        # if partida_de_coste_types == 'TODOS' and municipio_types != 'TODOS':
        #
        #     df_table = df_indicadores_pob.loc[(df_indicadores_pob['Nombre Ente Principal'] == municipio_types)&\
        #                     (df_indicadores_pob['Nº unidades']>0)]
        #     df_table['Nº unidades'] =  df_table['Nº unidades'].apply(lambda x: round(x,0))
        #
        #     df_table['Nº unidades'] = (df_table['Nº unidades'].map('{:,.0f}'.format).str.replace("," , "~").str.replace("." ,
        #                           ",").str.replace("~" , "."))
        #
        #     fig = go.Figure()
        #
        #     fig.add_trace(go.Table(
        #         columnwidth=[105,105, 90],
        #         header=dict(values=list(df_indicadores_pob[['Descripción','Unidades físicas de referencia' , 'Nº unidades']].columns) ,
        #                     fill_color='rgb(55, 83, 109)' ,
        #                     align=['left','center'] ,
        #                     font=dict(color='white' , size=13)) ,
        #         cells=dict(values=[df_table['Descripción'],df_table['Unidades físicas de referencia'] , df_table['Nº unidades']] ,
        #                    fill_color='rgb(243, 240, 255)' ,
        #                    align=['left','center']))
        #     )
        #
        # else:

            df_table = {'Seleccionar Partida de coste, para ver indicadores.': [1]}
            df_table = pd.DataFrame(data=df_table)

            fig = go.Figure()

            fig.add_trace(go.Table(
                columnwidth=[500] ,
                header=dict(values=list(df_table.columns) ,
                            fill_color='rgb(55, 83, 109)' ,
                            align=['center'] ,
                            font=dict(color='white' , size=15)) ,
                cells=dict(values=[df_table] ,
                           fill_color='#f9f9f9' ,
                           font=dict(color='white' , size=13) ,
                           align=['left' , 'center']))
            )

    else:
        if CCAA_types == 'TODAS' and PROV_types == 'TODAS' and municipio_types == 'TODOS':
            df_table = df_table_n
            df_table = df_table.loc[(df_table['Descripción'] == partida_de_coste_types) &\
                                              (df_table['Nº unidades'] > 0)]

            # df_table['Nº unidades'] = df_table['Nº unidades'].apply(lambda x: round(x , 0))
            df_table['Nº unidades'] = df_table['Nº unidades'].map('{:,.0f}'.format).str.replace("," , "~").str.replace(
                "." , ",").str.replace("~" , ".")

            fig = go.Figure()

            fig.add_trace(go.Table(
                columnwidth=[200 , 90] ,
                header=dict(
                    values=['Unidades físicas de referencia', 'Nº unidades'] ,
                    fill_color='rgb(55, 83, 109)' ,line_width=5,height=35,
                    align=['left' , 'center'] ,
                    font=dict(color='white' , size=15)) ,
                cells=dict(values=[df_table['Unidades físicas de referencia'] , df_table['Nº unidades']] ,
                           fill_color='#f2f2f2' ,font=dict(color='rgb(50, 50, 50)' , size=13),line_width=5,height=30,
                           align=['left' , 'center']))
            )


        elif CCAA_types != 'TODAS' and PROV_types == 'TODAS' and municipio_types == 'TODOS':
            df_table = df_table_c
            df_table = df_table.loc[(df_table['CCAA'] == CCAA_types) & (df_table['Descripción'] == partida_de_coste_types) & \
                                    (df_table['Nº unidades'] > 0)]

            # df_table['Nº unidades'] = df_table['Nº unidades'].apply(lambda x: round(x , 0))
            df_table['Nº unidades'] = df_table['Nº unidades'].map('{:,.0f}'.format).str.replace("," , "~").str.replace(
                "." , ",").str.replace("~" , ".")

            fig = go.Figure()

            fig.add_trace(go.Table(
                columnwidth=[200 , 90] ,
                header=dict(
                    values=['Unidades físicas de referencia', 'Nº unidades'] ,
                    fill_color='rgb(55, 83, 109)' ,line_width=5,height=35,
                    align=['left' , 'center'] ,
                    font=dict(color='white' , size=15)) ,
                cells=dict(values=[df_table['Unidades físicas de referencia'] , df_table['Nº unidades']] ,
                           fill_color='#f2f2f2' ,font=dict(color='rgb(50, 50, 50)' , size=13),line_width=5,height=30,
                           align=['left' , 'center']))
            )

        elif CCAA_types != 'TODAS' and PROV_types != 'TODAS' and municipio_types == 'TODOS':
            df_table = df_table_p
            df_table = df_table.loc[
                (df_table['Provincia'] == PROV_types) & (df_table['Descripción'] == partida_de_coste_types) & \
                (df_table['Nº unidades'] > 0)]

            # df_table['Nº unidades'] = df_table['Nº unidades'].apply(lambda x: round(x , 0))
            df_table['Nº unidades'] = df_table['Nº unidades'].map('{:,.0f}'.format).str.replace("," , "~").str.replace(
                "." , ",").str.replace("~" , ".")

            fig = go.Figure()

            fig.add_trace(go.Table(
                columnwidth=[200 , 90] ,
                header=dict(
                    values=['Unidades físicas de referencia', 'Nº unidades'] ,
                    fill_color='rgb(55, 83, 109)' ,line_width=5,height=35,
                    align=['left' , 'center'] ,
                    font=dict(color='white' , size=15)) ,
                cells=dict(values=[df_table['Unidades físicas de referencia'] , df_table['Nº unidades']] ,
                           fill_color='#f2f2f2' ,font=dict(color='rgb(50, 50, 50)' , size=13),line_width=5,height=30,
                           align=['left' , 'center']))
            )

        elif CCAA_types == 'TODAS' and PROV_types != 'TODAS' and municipio_types == 'TODOS':
            df_table = df_table_p
            df_table = df_table.loc[
                (df_table['Provincia'] == PROV_types) & (df_table['Descripción'] == partida_de_coste_types) & \
                (df_table['Nº unidades'] > 0)]

            # df_table['Nº unidades'] = df_table['Nº unidades'].apply(lambda x: round(x , 0))
            df_table['Nº unidades'] = df_table['Nº unidades'].map('{:,.0f}'.format).str.replace("," , "~").str.replace(
                "." , ",").str.replace("~" , ".")

            fig = go.Figure()

            fig.add_trace(go.Table(
                columnwidth=[200 , 90] ,
                header=dict(
                    values=['Unidades físicas de referencia', 'Nº unidades'] ,
                    fill_color='rgb(55, 83, 109)' ,line_width=5,height=35,
                    align=['left' , 'center'] ,
                    font=dict(color='white' , size=15)) ,
                cells=dict(values=[df_table['Unidades físicas de referencia'] , df_table['Nº unidades']] ,
                           fill_color='#f2f2f2' ,font=dict(color='rgb(50, 50, 50)' , size=13),line_width=5,height=30,
                           align=['left' , 'center']))
            )


        elif municipio_types != 'TODOS':
            df_table=df_table_m
            df_table= df_table.loc[(df_table['Descripción']==partida_de_coste_types)&\
                           (df_table['Nombre Ente Principal']==municipio_types)]

            # df_table['Nº unidades'] = df_table['Nº unidades'].apply(lambda x: round(x , 0))
            df_table['Nº unidades'] = df_table['Nº unidades'].map('{:,.0f}'.format).str.replace(",", "~").str.replace(".", ",").str.replace("~", ".")

            fig = go.Figure()

            fig.add_trace(go.Table(
                columnwidth=[200 , 90],
                header=dict(values=['Unidades físicas de referencia', 'Nº unidades'] ,
                            fill_color='rgb(55, 83, 109)' ,line_width=5,height=35,
                            align=['left','center'],
                            font=dict(color='white', size=15)) ,
                cells=dict(values=[df_table['Unidades físicas de referencia'],df_table['Nº unidades']] ,
                           fill_color='#f2f2f2' ,font=dict(color='rgb(50, 50, 50)' , size=13),line_width=5,height=30,
                           align=['left','center']))
            )








    fig.update_layout(margin=dict(l=20 , r=20 , t=60 , b=20),title='Indicadores por Partida de coste')
    fig.update_layout(plot_bgcolor="#F9F9F9" ,paper_bgcolor="#F9F9F9" , title_font_color='rgb(50, 50, 50)')

    return fig


################    coste_bars graph

@app.callback(Output("coste_bars_graph", "figure"),
    [
        Input("CCAA_types" , "value") , Input("PROV_types" , "value") , Input("municipio_types" , "value"),Input("partida_de_coste_types" , "value")
    ],[State("indicadores_table", "relayoutData")]
    # [State("lock_selector", "value"), State("indicadores_table", "relayoutData")],
)
def make_coste_bars_figure(CCAA_types, PROV_types,municipio_types, partida_de_coste_types,indicadores_table):

    if CCAA_types == 'TODAS' and PROV_types == 'TODAS' and municipio_types == 'TODOS':

        df = df_n

        fig = go.Figure()

        # fig.add_trace(go.Bar(x=df['Descripción'] ,y=df['coste_efectivo_new'] ,name='Total Nacional' ,marker_color='rgb(55, 83, 109)'))
        # fig.add_trace(go.Bar(x=df['Descripción'] ,y=df['coste_efectivo_new'] ,name='Total Nacional' ,marker_color='rgb(26, 118, 255)'))

        if partida_de_coste_types !='TODOS':
            colors = ['rgb(55, 83, 109)'] * df['Descripción'].shape[0]

            for pos , item in enumerate(df['Descripción'].to_list()):
                if item == partida_de_coste_types:
                    colors[pos] = 'rgb(217, 95, 2)'
            fig.add_trace(go.Bar(x=df['Descripción'] , y=df['coste_efectivo_new'] , name='Total Nacional',
                                 marker_color=colors))

            line = int(df.loc[df['Descripción'] == partida_de_coste_types , 'coste_efectivo_new'])
            fig.add_trace(go.Scatter(x=df['Descripción'] , y=[line] * df['Descripción'].shape[0] , showlegend=False ,hoverinfo='skip',
                                     line=dict(color='rgb(217, 95, 2)' , width=0.8 , dash='solid')))


        else:
            fig.add_trace(go.Bar(x=df['Descripción'] , y=df['coste_efectivo_new'] , name='Total Nacional',
                                 marker_color='rgb(55, 83, 109)'))

        fig.add_trace(go.Bar(x=df['Descripción'] , y=df['coste_efectivo_new'] , name='Total Nacional' ,
                             marker_color='rgb(26, 118, 255)'))









    elif CCAA_types != 'TODAS' and PROV_types == 'TODAS' and municipio_types == 'TODOS':

        df = df_n

        df2 = df_c

        div = df_final_pob.loc[df_final_pob['CCAA'] == CCAA_types , 'Población 2018'].sum()
        df2 = df2.loc[df2['CCAA'] == CCAA_types]
        df2['coste_efectivo_new'] = round(df2['coste_efectivo'] / div,)


        fig = go.Figure()
        # fig.add_trace(go.Bar(x=df2['Descripción'] , y=df2['coste_efectivo_new'] , name=f'{CCAA_types}' ,
        #                      marker_color='rgb(55, 83, 109)'))
        # fig.add_trace(go.Bar(x=df['Descripción'] , y=df['coste_efectivo_new'] , name='Total Nacional' ,
        #                      marker_color='rgb(26, 118, 255)'))

        if partida_de_coste_types !='TODOS':
            colors = ['rgb(55, 83, 109)'] * df2['Descripción'].shape[0]

            for pos , item in enumerate(df2['Descripción'].to_list()):
                if item == partida_de_coste_types:
                    colors[pos] = 'rgb(217, 95, 2)'
            fig.add_trace(go.Bar(x=df2['Descripción'] , y=df2['coste_efectivo_new'] , name=f'{CCAA_types}' ,
                                 marker_color=colors))

            line=int(df2.loc[df2['Descripción'] == partida_de_coste_types , 'coste_efectivo_new'])
            fig.add_trace(go.Scatter(x=df['Descripción'] , y=[line] * df['Descripción'].shape[0] , showlegend=False ,hoverinfo='skip',
                                     line=dict(color='rgb(217, 95, 2)' , width=0.8 , dash='solid')))

        else:
            fig.add_trace(go.Bar(x=df2['Descripción'] , y=df2['coste_efectivo_new'] , name=f'{CCAA_types}' ,
                                 marker_color='rgb(55, 83, 109)'))

        fig.add_trace(go.Bar(x=df['Descripción'] , y=df['coste_efectivo_new'] , name='Total Nacional' ,
                             marker_color='rgb(26, 118, 255)'))


    elif CCAA_types != 'TODAS' and PROV_types != 'TODAS' and municipio_types == 'TODOS':

        df = df_p
        div = df_final_pob.loc[df_final_pob['Provincia'] == PROV_types , 'Población 2018'].sum()
        df = df.loc[df['Provincia'] == PROV_types]
        df['coste_efectivo_new'] = round(df['coste_efectivo'] / div,)


        df2 = df_c
        div = df_final_pob.loc[df_final_pob['CCAA'] == CCAA_types , 'Población 2018'].sum()
        df2 = df2.loc[df2['CCAA'] == CCAA_types]
        df2['coste_efectivo_new'] = round(df2['coste_efectivo'] / div,)


        fig = go.Figure()
        # fig.add_trace(go.Bar(x=df['Descripción'] , y=df['coste_efectivo_new'] , name=f'{PROV_types}' ,
        #                      marker_color='rgb(55, 83, 109)'))
        # fig.add_trace(go.Bar(x=df2['Descripción'] , y=df2['coste_efectivo_new'] , name=f'{CCAA_types}' ,
        #                      marker_color='rgb(26, 118, 255)'))


        if partida_de_coste_types !='TODOS':
            colors = ['rgb(55, 83, 109)'] * df['Descripción'].shape[0]

            for pos , item in enumerate(df['Descripción'].to_list()):
                if item == partida_de_coste_types:
                    colors[pos] = 'rgb(217, 95, 2)'
            fig.add_trace(go.Bar(x=df['Descripción'] , y=df['coste_efectivo_new'] , name=f'{PROV_types}',
                                 marker_color=colors))

            line = int(df.loc[df['Descripción'] == partida_de_coste_types , 'coste_efectivo_new'])
            fig.add_trace(go.Scatter(x=df2['Descripción'] , y=[line] * df2['Descripción'].shape[0], showlegend=False ,hoverinfo='skip',
                                     line=dict(color='rgb(217, 95, 2)' ,width=0.8 , dash='solid')))

        else:
            fig.add_trace(go.Bar(x=df['Descripción'] , y=df['coste_efectivo_new'] , name=f'{PROV_types}' ,
                                 marker_color='rgb(55, 83, 109)'))

        fig.add_trace(go.Bar(x=df2['Descripción'] , y=df2['coste_efectivo_new'] , name=f'{CCAA_types}' ,
                             marker_color='rgb(26, 118, 255)'))






    elif CCAA_types == 'TODAS' and PROV_types != 'TODAS' and municipio_types == 'TODOS':

        df = df_p
        div = df_final_pob.loc[df_final_pob['Provincia'] == PROV_types , 'Población 2018'].sum()
        df = df.loc[df['Provincia'] == PROV_types]
        df['coste_efectivo_new'] = round(df['coste_efectivo'] / div,0)


        df2 = df_n

        fig = go.Figure()
        # fig.add_trace(go.Bar(x=df['Descripción'] , y=df['coste_efectivo_new'] , name=f'{PROV_types}' ,
        #                      marker_color='rgb(55, 83, 109)'))
        # fig.add_trace(go.Bar(x=df2['Descripción'] , y=df2['coste_efectivo_new'] , name=f'Total Nacional' ,
        #                      marker_color='rgb(26, 118, 255)'))

        if partida_de_coste_types !='TODOS':
            colors = ['rgb(55, 83, 109)'] * df['Descripción'].shape[0]

            for pos , item in enumerate(df['Descripción'].to_list()):
                if item == partida_de_coste_types:
                    colors[pos] = 'rgb(217, 95, 2)'
            fig.add_trace(go.Bar(x=df['Descripción'] , y=df['coste_efectivo_new'] , name=f'{PROV_types}',
                                 marker_color=colors))

            line = int(df.loc[df['Descripción'] == partida_de_coste_types , 'coste_efectivo_new'])
            fig.add_trace(go.Scatter(x=df2['Descripción'] , y=[line] * df2['Descripción'].shape[0] , showlegend=False ,hoverinfo='skip',
                                     line=dict(color='rgb(217, 95, 2)' , width=0.8 , dash='solid')))

        else:
            fig.add_trace(go.Bar(x=df['Descripción'] , y=df['coste_efectivo_new'] , name=f'{PROV_types}' ,
                                 marker_color='rgb(55, 83, 109)'))

        fig.add_trace(go.Bar(x=df2['Descripción'] , y=df2['coste_efectivo_new'] , name=f'Total Nacional' ,
                             marker_color='rgb(26, 118, 255)'))


    else:
        df =df_m.loc[df_m['Nombre Ente Principal'] == municipio_types].sort_values(by='coste_efectivo_PC',ascending=False)
        # df['coste_efectivo_PC'] = round(df['coste_efectivo_PC'] , )



        cohorte = df_cohorte.loc[df_cohorte['Nombre Ente Principal'] == municipio_types , 'cohorte_pob'] \
            .unique().to_list()[0]

        # df2 = df_final_pob_melt_PC.loc[ df_final_pob_melt_PC['coste_efectivo_PC'] > 0]
        df2 = df_m.pivot_table(index=['cohorte_pob','Descripción'],values=['coste_efectivo_PC'],aggfunc=np.median).reset_index()
        df2= df2.loc[df2['cohorte_pob'] == cohorte]
        # df2['coste_efectivo_PC'] = round(df2['coste_efectivo_PC'] , )


        fig = go.Figure()
        # fig.add_trace(go.Bar(x=df['Descripción'] , y=df['coste_efectivo_PC'] , name=f'{municipio_types}' ,
        #                      marker_color='rgb(55, 83, 109)'))
        # fig.add_trace(go.Bar(x=df2['Descripción'] , y=df2['coste_efectivo_PC'] , name=f'Media Municipios con {cohorte} hab.' ,
        #                      marker_color='rgb(26, 118, 255)'))


        if partida_de_coste_types !='TODOS':
            colors = ['rgb(55, 83, 109)'] * df['Descripción'].shape[0]

            for pos , item in enumerate(df['Descripción'].to_list()):
                if item == partida_de_coste_types:
                    colors[pos] = 'rgb(217, 95, 2)'
            fig.add_trace(go.Bar(x=df['Descripción'] , y=df['coste_efectivo_PC'] , name=f'{municipio_types}',
                                 marker_color=colors))

            line = int(df.loc[df['Descripción'] == partida_de_coste_types , 'coste_efectivo_PC'])


            fig.add_trace(go.Scatter(x=df2['Descripción'] , y=[line] * df2['Descripción'].shape[0], showlegend=False ,hoverinfo='skip',
                                     line=dict(color='rgb(217, 95, 2)' , width=0.8 , dash='solid')))

        else:
            fig.add_trace(go.Bar(x=df['Descripción'] , y=df['coste_efectivo_PC'] , name=f'{municipio_types}' ,
                                 marker_color='rgb(55, 83, 109)'))

        fig.add_trace(
            go.Bar(x=df2['Descripción'] , y=df2['coste_efectivo_PC'] , name=f'Media Municipios con {cohorte} hab.' ,
                   marker_color='rgb(26, 118, 255)'))


    # fig.update_traces( marker_line_color='rgb(8,48,107)')
    fig.update_layout(margin=dict(l=20 , r=50 , t=50 , b=50) ,#plot_bgcolor="white",
                          title='Costes €/hab. por Partida de coste' ,
                          xaxis_tickfont_size=12 ,
                          xaxis_tickangle=-45 ,
                          yaxis=dict(
                              title='Coste €/hab.' ,
                              titlefont_size=16 ,
                              tickfont_size=12 ,showticklabels=True,color='rgb(50, 50, 50)',

                          ) ,
                          xaxis=dict(
                              title='Partidas de Costes' ,
                              titlefont_size=16 ,
                              tickfont_size=14 , showticklabels=False ,color='rgb(50, 50, 50)',
                            showline=False,
                            showgrid=False,

                          ) ,

                          legend=dict(
                              x=0.40 ,
                              y=0.9 ,font_color='rgb(50, 50, 50)',
                              # bgcolor='rgba(255, 255, 255, 0)' ,
                              # bordercolor='rgba(255, 255, 255, 0)',
                              font_size=14,bgcolor='#eeeeee',
        # bordercolor="Black",
        # borderwidth=0.8
                          ) ,
                          barmode='group' ,
                          # bargap=0.30 ,
                          # bargroupgap=0.35  ,
                        bargap = 0.10 ,  # gap between bars of adjacent location coordinates.
                        bargroupgap = 0.25 , # gap between bars of the same location coordinate.

                          paper_bgcolor="#F9F9F9",title_font_color='rgb(50, 50, 50)')

    fig.update_layout(yaxis=dict(gridcolor='#cacaca') ,
                      xaxis=dict(showline=True ,linecolor='#929292' ,linewidth=0.5),
                      plot_bgcolor="#F9F9F9")

    return fig


################    map graph
@app.callback(
    Output("map_graph", "figure"),
    [
        Input("CCAA_types" , "value") , Input("PROV_types" , "value") , Input("municipio_types" , "value") ,
        Input("partida_de_coste_types" , "value")
    ],[State("indicadores_table", "relayoutData")]
    # [State("lock_selector", "value"), State("indicadores_table", "relayoutData")],
)
def make_map_figure(CCAA_types, PROV_types,municipio_types,partida_de_coste_types, indicadores_table):
    if partida_de_coste_types == 'TODOS':
        if CCAA_types == 'TODAS' and PROV_types == 'TODAS' and municipio_types == 'TODOS':
            df = df_final_pob_round#[df_final_pob['Población']>5000]
            # df['Población'] = df['Población 2018']
            # df['PC_TOTAL'] = df.apply(lambda new: round(new['PC_TOTAL'] , ) , axis=1)
            q9 = df['PC_TOTAL'].quantile(0.90)
            q1 = df['PC_TOTAL'].quantile(0.10)
            max = df['PC_TOTAL'].max()
            min = df['PC_TOTAL'].min()
            median = df['PC_TOTAL'].median()

            # df_zoom_po = df_zoom_pob
            # df_zoom_po = df_zoom_po[df_zoom_po['Población 2018']>5000]
            # df_zoom_po.to_file('./data/main_temp/shapefiles_espana_municipiosCCAA.geojson' , driver='GeoJSON')
            # with open('./data/main_temp/shapefiles_espana_municipiosCCAA.geojson') as response:
            #     countiesNN = json.load(response)

            fig = px.choropleth_mapbox(df , geojson=counties , locations='codigo_geo' , color='PC_TOTAL' ,
                                       color_continuous_scale="haline" ,
                                       range_color=(q1 , q9) ,
                                       mapbox_style="carto-positron" ,
                                       featureidkey="properties.f_codmun" ,
                                       zoom=4.5 , center={"lat": 39.8 , "lon": -4.3} ,
                                       opacity=0.5 , labels={'PC_TOTAL': 'Coste por habitante'} ,
                                       hover_name='Nombre Ente Principal' , hover_data={'codigo_geo': False ,
                                                                                        'Población': ':,' ,
                                                                                        'PC_TOTAL': ":,€"} ,
                                       )

            fig.update_layout(coloraxis_colorbar=dict(tickmode='array' , tickvals=[q1 , (q9 + q1) / 2 , q9] ,
                                                      ticktext=[min , median , max]))




        elif CCAA_types != 'TODAS' and PROV_types == 'TODAS' and municipio_types == 'TODOS':
            df = df_final_pob_round.loc[df_final_pob_round['CCAA']==CCAA_types]
            # df['Población'] = df['Población 2018']
            # df['PC_TOTAL'] = df.apply(lambda new: round(new['PC_TOTAL'] , ) , axis=1)
            q9 = df['PC_TOTAL'].quantile(0.90)
            q1 = df['PC_TOTAL'].quantile(0.10)
            max = df['PC_TOTAL'].max()
            min = df['PC_TOTAL'].min()
            median = df['PC_TOTAL'].median()
            df_zoom_po=df_zoom_pob
            df_zoom_po=df_zoom_po[df_zoom_po['CCAA']==CCAA_types]
            df_zoom_po.to_file('./data/main_temp/shapefiles_espana_municipiosCCAA.geojson' , driver='GeoJSON')
            with open('./data/main_temp/shapefiles_espana_municipiosCCAA.geojson') as response:
                countiesCCAA = json.load(response)


            fig = px.choropleth_mapbox(df , geojson=countiesCCAA , locations='codigo_geo' , color='PC_TOTAL' ,
                                       color_continuous_scale="haline" ,
                                       range_color=(q1 , q9) ,
                                       mapbox_style="carto-positron" ,
                                       featureidkey="properties.f_codmun" ,
                                       zoom=4.5 , center={"lat": 39.8 , "lon": -4.3} ,
                                       opacity=0.5 , labels={'PC_TOTAL': 'Coste por habitante'} ,
                                       hover_name='Nombre Ente Principal' , hover_data={'codigo_geo': False ,
                                                                                        'Población': ':,' ,
                                                                                        'PC_TOTAL': ":,€"} ,
                                       )

            fig.update_layout(coloraxis_colorbar=dict(tickmode='array' , tickvals=[q1 , (q9 + q1) / 2 , q9] ,
                                                      ticktext=[min , median , max]))


            lat=CCAA_CO.loc[CCAA_CO['CCAA']==CCAA_types,'LAT'].to_list()
            lon=CCAA_CO.loc[CCAA_CO['CCAA']==CCAA_types,'LON'].to_list()

            if CCAA_types=='Canarias':
                lat = 36
                lon = -11
            else:
                lat=lat[0]
                lon=lon[0]


            fig.update_layout(mapbox_zoom=6 , mapbox_center={"lat": lat , "lon": lon},)


        elif CCAA_types != 'TODAS' and PROV_types != 'TODAS' and municipio_types == 'TODOS':

            df = df_final_pob_round.loc[df_final_pob_round['Provincia'] == PROV_types]
            # df['Población'] = df['Población 2018']
            # df['PC_TOTAL'] = df.apply(lambda new: round(new['PC_TOTAL'] , ) , axis=1)
            q9 = df['PC_TOTAL'].quantile(0.90)
            q1 = df['PC_TOTAL'].quantile(0.10)
            max = df['PC_TOTAL'].max()
            min = df['PC_TOTAL'].min()
            median = df['PC_TOTAL'].median()
            df_zoom_po = df_zoom_pob
            df_zoom_po = df_zoom_po[df_zoom_po['Provincia'] == PROV_types]
            df_zoom_po.to_file('./data/main_temp/shapefiles_espana_municipiosPROV.geojson' , driver='GeoJSON')
            with open('./data/main_temp/shapefiles_espana_municipiosPROV.geojson') as response:
                countiesPROV = json.load(response)

            fig = px.choropleth_mapbox(df , geojson=countiesPROV , locations='codigo_geo' , color='PC_TOTAL' ,
                                       color_continuous_scale="haline" ,
                                       range_color=(q1 , q9) ,
                                       mapbox_style="carto-positron" ,
                                       featureidkey="properties.f_codmun" ,
                                       zoom=4.5 , center={"lat": 39.8 , "lon": -4.3} ,
                                       opacity=0.5 , labels={'PC_TOTAL': 'Coste por habitante'} ,
                                       hover_name='Nombre Ente Principal' , hover_data={'codigo_geo': False ,
                                                                                        'Población': ':,' ,
                                                                                        'PC_TOTAL': ":,€"} ,
                                       )

            fig.update_layout(coloraxis_colorbar=dict(tickmode='array' , tickvals=[q1 , (q9 + q1) / 2 , q9] ,
                                                      ticktext=[min , median , max]))










            lat = PROV_CO.loc[PROV_CO['Provincia'] == PROV_types , 'LAT'].to_list()
            lon = PROV_CO.loc[PROV_CO['Provincia'] == PROV_types , 'LON'].to_list()

            if PROV_types == 'Santa Cruz de Tenerife' or PROV_types == 'Palmas, Las':
                lat = 36
                lon = -11
                fig.update_layout(mapbox_zoom=6 , mapbox_center={"lat": lat , "lon": lon})
            else:
                lat = lat[0]
                lon = lon[0]

                fig.update_layout(mapbox_zoom=7 , mapbox_center={"lat": lat , "lon": lon})

        elif CCAA_types == 'TODAS' and PROV_types != 'TODAS' and municipio_types == 'TODOS':
            df = df_final_pob_round.loc[df_final_pob_round['Provincia'] == PROV_types]
            # df['Población'] = df['Población 2018']
            # df['PC_TOTAL'] = df.apply(lambda new: round(new['PC_TOTAL'] , ) , axis=1)
            q9 = df['PC_TOTAL'].quantile(0.90)
            q1 = df['PC_TOTAL'].quantile(0.10)
            max = df['PC_TOTAL'].max()
            min = df['PC_TOTAL'].min()
            median = df['PC_TOTAL'].median()
            df_zoom_po = df_zoom_pob
            df_zoom_po = df_zoom_po[df_zoom_po['Provincia'] == PROV_types]
            df_zoom_po.to_file('./data/main_temp/shapefiles_espana_municipiosPROV.geojson' , driver='GeoJSON')
            with open('./data/main_temp/shapefiles_espana_municipiosPROV.geojson') as response:
                countiesPROV = json.load(response)

            fig = px.choropleth_mapbox(df , geojson=countiesPROV , locations='codigo_geo' , color='PC_TOTAL' ,
                                       color_continuous_scale="haline" ,
                                       range_color=(q1 , q9) ,
                                       mapbox_style="carto-positron" ,
                                       featureidkey="properties.f_codmun" ,
                                       zoom=4.5 , center={"lat": 39.8 , "lon": -4.3} ,
                                       opacity=0.5 , labels={'PC_TOTAL': 'Coste por habitante'} ,
                                       hover_name='Nombre Ente Principal' , hover_data={'codigo_geo': False ,
                                                                                        'Población': ':,' ,
                                                                                        'PC_TOTAL': ":,€"} ,
                                       )

            fig.update_layout(coloraxis_colorbar=dict(tickmode='array' , tickvals=[q1 , (q9 + q1) / 2 , q9] ,
                                                      ticktext=[min , median , max]))


            lat = PROV_CO.loc[PROV_CO['Provincia'] == PROV_types , 'LAT'].to_list()
            lon = PROV_CO.loc[PROV_CO['Provincia'] == PROV_types , 'LON'].to_list()

            if PROV_types == 'Santa Cruz de Tenerife' or PROV_types == 'Palmas, Las':
                lat = 36
                lon = -11
                fig.update_layout(mapbox_zoom=6 , mapbox_center={"lat": lat , "lon": lon})

            else:
                lat = lat[0]
                lon = lon[0]

                fig.update_layout(mapbox_zoom=7 , mapbox_center={"lat": lat , "lon": lon})

        else:
            PROV = MUNI_CO.loc[MUNI_CO['Nombre Ente Principal'] == municipio_types , 'Provincia'].to_list()
            PROV = PROV[0]
            df = df_final_pob_round.loc[df_final_pob_round['Provincia'] == PROV]
            # df['Población'] = df['Población 2018']
            # df['PC_TOTAL'] = df.apply(lambda new: round(new['PC_TOTAL'] , 0) , axis=1)
            q9 = df['PC_TOTAL'].quantile(0.90)
            q1 = df['PC_TOTAL'].quantile(0.10)
            max = df['PC_TOTAL'].max()
            min = df['PC_TOTAL'].min()
            median = df['PC_TOTAL'].median()
            df_zoom_po = df_zoom_pob
            df_zoom_po = df_zoom_po[df_zoom_po['Provincia'] == PROV]
            df_zoom_po.to_file('./data/main_temp/shapefiles_espana_municipiosPROV.geojson' , driver='GeoJSON')
            with open('./data/main_temp/shapefiles_espana_municipiosPROV.geojson') as response:
                countiesPROV = json.load(response)

            fig = px.choropleth_mapbox(df , geojson=countiesPROV , locations='codigo_geo' , color='PC_TOTAL' ,
                                       color_continuous_scale="haline" ,
                                       range_color=(q1 , q9) ,
                                       mapbox_style="carto-positron" ,
                                       featureidkey="properties.f_codmun" ,
                                       zoom=4.5 , center={"lat": 39.8 , "lon": -4.3} ,
                                       opacity=0.5 , labels={'PC_TOTAL': 'Coste por habitante'} ,
                                       hover_name='Nombre Ente Principal' , hover_data={'codigo_geo': False ,
                                                                                        'Población': ':,' ,
                                                                                        'PC_TOTAL': ":,€"} ,
                                       )

            fig.update_layout(coloraxis_colorbar=dict(tickmode='array' , tickvals=[q1 , (q9 + q1) / 2 , q9] ,
                                                      ticktext=[min , median , max]))






            lat = MUNI_CO.loc[MUNI_CO['Nombre Ente Principal'] == municipio_types , 'LAT'].to_list()
            lon = MUNI_CO.loc[MUNI_CO['Nombre Ente Principal'] == municipio_types, 'LON'].to_list()

            # PROV=MUNI_CO.loc[MUNI_CO['Nombre Ente Principal'] == municipio_types , 'Provincia'].to_list()
            # PROV = PROV[0]

            if PROV == 'Santa Cruz de Tenerife' or PROV == 'Palmas, Las':
                lat = 36
                lon = -11
                fig.update_layout(mapbox_zoom=6 , mapbox_center={"lat": lat , "lon": lon})

            else:
                lat = lat[0]
                lon = lon[0]

                fig.update_layout(mapbox_zoom=9 , mapbox_center={"lat": lat , "lon": lon})


    else:


        if CCAA_types == 'TODAS' and PROV_types == 'TODAS' and municipio_types == 'TODOS':

            df = df_final_pob_round_melt_PC_object#[df_final_pob_round_melt_PC['Población']>5000]
            # df['Población'] = df['Población 2018']
            df= df.loc[(df['Descripción']==partida_de_coste_types)& (df['coste_efectivo_PC'] > 0)]
            # df['coste_efectivo_PC'] = df.apply(lambda new: round(new['coste_efectivo_PC'] , ) , axis=1)
            q9 = df['coste_efectivo_PC'].quantile(0.90)
            q1 = df['coste_efectivo_PC'].quantile(0.10)
            max = df['coste_efectivo_PC'].max()
            min = df['coste_efectivo_PC'].min()
            median = df['coste_efectivo_PC'].median()

            df['codigo_geo'] = df['codigo_geo'].astype('int64')
            df_zoom_po = df_zoom_pob
            df_zoom_po = pd.merge(df_zoom_po , df , on='codigo_geo' , how='left' , suffixes=('' , '_y'))
            df_zoom_po = df_zoom_po.loc[df_zoom_po['CCAA_y'].isnull() == False]

            df_zoom_po.to_file('./data/main_temp/shapefiles_espana_municipiosCCAA_PC.geojson' , driver='GeoJSON')
            with open('./data/main_temp/shapefiles_espana_municipiosCCAA_PC.geojson') as response:
                countiesNN = json.load(response)



            fig = px.choropleth_mapbox(df , geojson=countiesNN , locations='codigo_geo' , color='coste_efectivo_PC' ,
                                       color_continuous_scale="haline" ,
                                       range_color=(q1 , q9) ,
                                       mapbox_style="carto-positron" ,
                                       featureidkey="properties.f_codmun" ,
                                       zoom=4.5 , center={"lat": 39.8 , "lon": -4.3} ,
                                       opacity=0.5 , labels={'coste_efectivo_PC': f'Coste por habitante, {partida_de_coste_types}'} ,
                                       hover_name='Nombre Ente Principal' , hover_data={'codigo_geo': False ,'Población': ':,' ,
                                                                                        'coste_efectivo_PC': ":,€"} ,
                                       )

            fig.update_layout(coloraxis_colorbar=dict(tickmode='array' , tickvals=[q1 , (q9 + q1) / 2 , q9] ,
                                                      ticktext=[min , median , max]))



        elif CCAA_types != 'TODAS' and PROV_types == 'TODAS' and municipio_types == 'TODOS':
            df = df_final_pob_round_melt_PC[df_final_pob_round_melt_PC['CCAA']==CCAA_types]
            # df['Población'] = df['Población 2018']
            df = df.loc[(df['Descripción'] == partida_de_coste_types) & (df['coste_efectivo_PC'] > 0)]
            # df['coste_efectivo_PC'] = df.apply(lambda new: round(new['coste_efectivo_PC'] , ) , axis=1)
            q9 = df['coste_efectivo_PC'].quantile(0.90)
            q1 = df['coste_efectivo_PC'].quantile(0.10)
            max = df['coste_efectivo_PC'].max()
            min = df['coste_efectivo_PC'].min()
            median = df['coste_efectivo_PC'].median()
            df_zoom_po = df_zoom_pob
            df_zoom_po = df_zoom_po[df_zoom_po['CCAA'] == CCAA_types]
            df_zoom_po.to_file('./data/main_temp/shapefiles_espana_municipiosCCAA.geojson' , driver='GeoJSON')
            with open('./data/main_temp/shapefiles_espana_municipiosCCAA.geojson') as response:
                countiesCCAA = json.load(response)

            fig = px.choropleth_mapbox(df , geojson=countiesCCAA , locations='codigo_geo' , color='coste_efectivo_PC' ,
                                       color_continuous_scale="haline" ,
                                       range_color=(q1 , q9) ,
                                       mapbox_style="carto-positron" ,
                                       featureidkey="properties.f_codmun" ,
                                       zoom=4.5 , center={"lat": 39.8 , "lon": -4.3} ,
                                       opacity=0.5 ,
                                       labels={'coste_efectivo_PC': f'Coste por habitante, {partida_de_coste_types}'} ,
                                       hover_name='Nombre Ente Principal' , hover_data={'codigo_geo': False ,'Población': ':,' ,
                                                                                        'coste_efectivo_PC': ":,€"} ,
                                       )

            fig.update_layout(coloraxis_colorbar=dict(tickmode='array' , tickvals=[q1 , (q9 + q1) / 2 , q9] ,
                                                      ticktext=[min , median , max]))



            lat = CCAA_CO.loc[CCAA_CO['CCAA'] == CCAA_types , 'LAT'].to_list()
            lon = CCAA_CO.loc[CCAA_CO['CCAA'] == CCAA_types , 'LON'].to_list()

            if CCAA_types == 'Canarias':
                lat = 36
                lon = -11
            else:
                lat = lat[0]
                lon = lon[0]

            fig.update_layout(mapbox_zoom=6 , mapbox_center={"lat": lat , "lon": lon})



        elif CCAA_types != 'TODAS' and PROV_types != 'TODAS' and municipio_types == 'TODOS':

            df = df_final_pob_round_melt_PC[df_final_pob_round_melt_PC['Provincia'] == PROV_types]
            # df['Población'] = df['Población 2018']
            df = df.loc[(df['Descripción'] == partida_de_coste_types) & (df['coste_efectivo_PC'] > 0)]
            # df['coste_efectivo_PC'] = df.apply(lambda new: round(new['coste_efectivo_PC'] , ) , axis=1)
            q9 = df['coste_efectivo_PC'].quantile(0.90)
            q1 = df['coste_efectivo_PC'].quantile(0.10)
            max = df['coste_efectivo_PC'].max()
            min = df['coste_efectivo_PC'].min()
            median = df['coste_efectivo_PC'].median()
            df_zoom_po = df_zoom_pob
            df_zoom_po = df_zoom_po[df_zoom_po['Provincia'] == PROV_types]
            df_zoom_po.to_file('./data/main_temp/shapefiles_espana_municipiosPROV.geojson' , driver='GeoJSON')
            with open('./data/main_temp/shapefiles_espana_municipiosPROV.geojson') as response:
                countiesPROV = json.load(response)

            fig = px.choropleth_mapbox(df , geojson=countiesPROV , locations='codigo_geo' , color='coste_efectivo_PC' ,
                                       color_continuous_scale="haline" ,
                                       range_color=(q1 , q9) ,
                                       mapbox_style="carto-positron" ,
                                       featureidkey="properties.f_codmun" ,
                                       zoom=4.5 , center={"lat": 39.8 , "lon": -4.3} ,
                                       opacity=0.5 ,
                                       labels={'coste_efectivo_PC': f'Coste por habitante, {partida_de_coste_types}'} ,
                                       hover_name='Nombre Ente Principal' , hover_data={'codigo_geo': False ,'Población': ':,' ,
                                                                                        'coste_efectivo_PC': ":,€"} ,
                                       )

            fig.update_layout(coloraxis_colorbar=dict(tickmode='array' , tickvals=[q1 , (q9 + q1) / 2 , q9] ,
                                                      ticktext=[min , median , max]))


            lat = PROV_CO.loc[PROV_CO['Provincia'] == PROV_types , 'LAT'].to_list()
            lon = PROV_CO.loc[PROV_CO['Provincia'] == PROV_types , 'LON'].to_list()

            if PROV_types == 'Santa Cruz de Tenerife' or PROV_types == 'Palmas, Las':
                lat = 36
                lon = -11
                fig.update_layout(mapbox_zoom=6 , mapbox_center={"lat": lat , "lon": lon})
            else:
                lat = lat[0]
                lon = lon[0]

                fig.update_layout(mapbox_zoom=7 , mapbox_center={"lat": lat , "lon": lon})



        elif CCAA_types == 'TODAS' and PROV_types != 'TODAS' and municipio_types == 'TODOS':
            df = df_final_pob_round_melt_PC[df_final_pob_round_melt_PC['Provincia'] == PROV_types]
            # df['Población'] = df['Población 2018']
            df = df.loc[(df['Descripción'] == partida_de_coste_types) & (df['coste_efectivo_PC'] > 0)]
            # df['coste_efectivo_PC'] = df.apply(lambda new: round(new['coste_efectivo_PC'] , ) , axis=1)
            q9 = df['coste_efectivo_PC'].quantile(0.90)
            q1 = df['coste_efectivo_PC'].quantile(0.10)
            max = df['coste_efectivo_PC'].max()
            min = df['coste_efectivo_PC'].min()
            median = df['coste_efectivo_PC'].median()
            df_zoom_po = df_zoom_pob
            df_zoom_po = df_zoom_po[df_zoom_po['Provincia'] == PROV_types]
            df_zoom_po.to_file('./data/main_temp/shapefiles_espana_municipiosPROV.geojson' , driver='GeoJSON')
            with open('./data/main_temp/shapefiles_espana_municipiosPROV.geojson') as response:
                countiesPROV = json.load(response)

            fig = px.choropleth_mapbox(df , geojson=countiesPROV , locations='codigo_geo' , color='coste_efectivo_PC' ,
                                       color_continuous_scale="haline" ,
                                       range_color=(q1 , q9) ,
                                       mapbox_style="carto-positron" ,
                                       featureidkey="properties.f_codmun" ,
                                       zoom=4.5 , center={"lat": 39.8 , "lon": -4.3} ,
                                       opacity=0.5 ,
                                       labels={'coste_efectivo_PC': f'Coste por habitante, {partida_de_coste_types}'} ,
                                       hover_name='Nombre Ente Principal' , hover_data={'codigo_geo': False ,'Población': ':,' ,
                                                                                        'coste_efectivo_PC': ":,€"} ,
                                       )

            fig.update_layout(coloraxis_colorbar=dict(tickmode='array' , tickvals=[q1 , (q9 + q1) / 2 , q9] ,
                                                      ticktext=[min , median , max]))

            lat = PROV_CO.loc[PROV_CO['Provincia'] == PROV_types , 'LAT'].to_list()
            lon = PROV_CO.loc[PROV_CO['Provincia'] == PROV_types , 'LON'].to_list()

            if PROV_types == 'Santa Cruz de Tenerife' or PROV_types == 'Palmas, Las':
                lat = 36
                lon = -11
                fig.update_layout(mapbox_zoom=6 , mapbox_center={"lat": lat , "lon": lon})
            else:
                lat = lat[0]
                lon = lon[0]

                fig.update_layout(mapbox_zoom=7 , mapbox_center={"lat": lat , "lon": lon})



        else:
            PROV = MUNI_CO.loc[MUNI_CO['Nombre Ente Principal'] == municipio_types , 'Provincia'].to_list()
            PROV = PROV[0]
            df = df_final_pob_round_melt_PC[df_final_pob_round_melt_PC['Provincia'] == PROV]
            # df['Población'] = df['Población 2018']
            df = df.loc[(df['Descripción'] == partida_de_coste_types) & (df['coste_efectivo_PC'] > 0)]
            # df['coste_efectivo_PC'] = df.apply(lambda new: round(new['coste_efectivo_PC'] , ) , axis=1)
            q9 = df['coste_efectivo_PC'].quantile(0.90)
            q1 = df['coste_efectivo_PC'].quantile(0.10)
            max = df['coste_efectivo_PC'].max()
            min = df['coste_efectivo_PC'].min()
            median = df['coste_efectivo_PC'].median()
            df_zoom_po = df_zoom_pob
            df_zoom_po = df_zoom_po[df_zoom_po['Provincia'] == PROV]
            df_zoom_po.to_file('./data/main_temp/shapefiles_espana_municipiosPROV.geojson' , driver='GeoJSON')
            with open('./data/main_temp/shapefiles_espana_municipiosPROV.geojson') as response:
                countiesPROV = json.load(response)

            fig = px.choropleth_mapbox(df , geojson=countiesPROV , locations='codigo_geo' , color='coste_efectivo_PC' ,
                                       color_continuous_scale="haline" ,
                                       range_color=(q1 , q9) ,
                                       mapbox_style="carto-positron" ,
                                       featureidkey="properties.f_codmun" ,
                                       zoom=4.5 , center={"lat": 39.8 , "lon": -4.3} ,
                                       opacity=0.5 ,
                                       labels={'coste_efectivo_PC': f'Coste por hab., {partida_de_coste_types}'} ,
                                       hover_name='Nombre Ente Principal' , hover_data={'codigo_geo': False ,'Población': ':,' ,
                                                                                        'coste_efectivo_PC': ":,€"} ,
                                       )

            fig.update_layout(coloraxis_colorbar=dict(tickmode='array' , tickvals=[q1 , (q9 + q1) / 2 , q9] ,
                                                      ticktext=[min , median , max]))

            lat = MUNI_CO.loc[MUNI_CO['Nombre Ente Principal'] == municipio_types , 'LAT'].to_list()
            lon = MUNI_CO.loc[MUNI_CO['Nombre Ente Principal'] == municipio_types , 'LON'].to_list()

            # PROV = MUNI_CO.loc[MUNI_CO['Nombre Ente Principal'] == municipio_types , 'Provincia'].to_list()
            # PROV = PROV[0]

            if PROV == 'Santa Cruz de Tenerife' or PROV == 'Palmas, Las':
                lat = 36
                lon = -11
                fig.update_layout(mapbox_zoom=6 , mapbox_center={"lat": lat , "lon": lon})

            else:
                lat = lat[0]
                lon = lon[0]

                fig.update_layout(mapbox_zoom=9 , mapbox_center={"lat": lat , "lon": lon})

    # [[0.0 , "rgb(165,0,38)"] ,
    #  [0.1111111111111111 , "rgb(215,48,39)"] ,
    #  [0.2222222222222222 , "rgb(244,109,67)"] ,
    #  [0.3333333333333333 , "rgb(253,174,97)"] ,
    #  [0.4444444444444444 , "rgb(254,224,144)"] ,
    #  [0.5555555555555556 , "rgb(224,243,248)"] ,
    #  [0.6666666666666666 , "rgb(171,217,233)"] ,
    #  [0.7777777777777778 , "rgb(116,173,209)"] ,
    #  [0.8888888888888888 , "rgb(69,117,180)"] ,
    #  # [1.0 , "rgb(49,54,149)"]]


    token = 'pk.eyJ1IjoiY2FycGllcm8iLCJhIjoiY2tmdXhxdnl2MWIxaDJ5bXpsb2dteW02dyJ9.Ory0CKJI2j7xMiviRyObJg'
    # fig.update_layout(mapbox_style="mapbox://styles/carpiero/ckg0zxgw42pa119ofckmup850" , mapbox_accesstoken=token)
    # fig.update_layout(mapbox_style="mapbox://styles/carpiero/ckg7tc8yh5w1g19qhuf9d1kpz" , mapbox_accesstoken=token)
    # fig.update_layout(mapbox_style="mapbox://styles/carpiero/ckg7tt9cb5vyo19mkwwg6nmf0" , mapbox_accesstoken=token)
    fig.update_layout(coloraxis_colorbar=dict(title='',title_font_size=15,tickfont_size=14,
        thicknessmode="pixels" , thickness=20 ,
        lenmode="pixels" , len=350 , bgcolor='#eeeeee',tickformat="n:,",borderwidth=0,
                ),coloraxis_reversescale=True,plot_bgcolor="#F9F9F9",paper_bgcolor="#F9F9F9",title_font_color='rgb(50, 50, 50)')

    fig.update_layout(margin={"r": 20 , "t": 40 , "l": 20 , "b": 20})
    if partida_de_coste_types == 'TODOS':
        fig.update_layout(title=f'Coste por habitante Total' )

    else:
        fig.update_layout(title=f'Coste por hab., {partida_de_coste_types}')





    return fig


################    box graph
@app.callback(
    Output("box_graph", "figure"),
    [
        Input("CCAA_types" , "value") , Input("PROV_types" , "value") , Input("municipio_types" , "value") ,
        Input("partida_de_coste_types" , "value")
    ],[State("indicadores_table", "relayoutData")]
    # [State("lock_selector", "value"), State("indicadores_table", "relayoutData")],
)

def make_box_figure(CCAA_types, PROV_types,municipio_types,partida_de_coste_types, indicadores_table):
    if partida_de_coste_types == 'TODOS':
        if CCAA_types == 'TODAS' and PROV_types == 'TODAS' and municipio_types == 'TODOS':
            df = df_final_pob_round_color

            fig = px.box(df , y='PC_TOTAL',labels={'PC_TOTAL': 'Coste por habitante'} ,
                                       hover_name='Nombre Ente Principal' , hover_data={'Población': ':,' ,'color':False,
                                                                                        'PC_TOTAL': ":,€"},template='seaborn',
                         color='color', color_discrete_map={'color': 'rgb(42, 35, 160)'})

            fig.update_layout( xaxis = dict(title='Total Municipios'))


        elif CCAA_types != 'TODAS' and PROV_types == 'TODAS' and municipio_types == 'TODOS':
            df = df_final_pob_round_color.loc[df_final_pob_round_color['CCAA']==CCAA_types]

            fig = px.box(df , y='PC_TOTAL' , labels={'PC_TOTAL': 'Coste por habitante'} ,
                         hover_name='Nombre Ente Principal' , hover_data={'Población': ':,' , 'color': False ,
                                                                          'PC_TOTAL': ":,€"} , template='seaborn' ,
                         color='color' , color_discrete_map={'color': 'rgb(42, 35, 160)'})

            fig.update_layout(xaxis=dict(title=f'Municipios de {CCAA_types}'))



        elif CCAA_types != 'TODAS' and PROV_types != 'TODAS' and municipio_types == 'TODOS':
            df = df_final_pob_round_color.loc[df_final_pob_round_color['Provincia'] == PROV_types]

            fig = px.box(df , y='PC_TOTAL' , labels={'PC_TOTAL': 'Coste por habitante'} ,
                         hover_name='Nombre Ente Principal' , hover_data={'Población': ':,' , 'color': False ,
                                                                          'PC_TOTAL': ":,€"} , template='seaborn' ,
                         color='color' , color_discrete_map={'color': 'rgb(42, 35, 160)'})

            fig.update_layout(xaxis=dict(title=f'Municipios de {PROV_types}'))



        elif CCAA_types == 'TODAS' and PROV_types != 'TODAS' and municipio_types == 'TODOS':
            df = df_final_pob_round_color.loc[df_final_pob_round_color['Provincia'] == PROV_types]

            fig = px.box(df , y='PC_TOTAL' , labels={'PC_TOTAL': 'Coste por habitante'} ,
                         hover_name='Nombre Ente Principal' , hover_data={'Población': ':,' , 'color': False ,
                                                                          'PC_TOTAL': ":,€"} , template='seaborn' ,
                         color='color' , color_discrete_map={'color': 'rgb(42, 35, 160)'})

            fig.update_layout(xaxis=dict(title=f'Municipios de {PROV_types}'))


        else:

            PROV = MUNI_CO.loc[MUNI_CO['Nombre Ente Principal'] == municipio_types , 'Provincia'].to_list()
            PROV = PROV[0]
            df = df_final_pob_round_color.loc[df_final_pob_round_color['Provincia'] == PROV]

            fig = px.box(df , y='PC_TOTAL' , labels={'PC_TOTAL': 'Coste por habitante'} ,
                         hover_name='Nombre Ente Principal' , hover_data={'Población': ':,' , 'color': False ,
                                                                          'PC_TOTAL': ":,€"} , template='seaborn' ,
                         color='color' , color_discrete_map={'color': 'rgb(42, 35, 160)'})

            fig.update_layout(xaxis=dict(title=f'Municipios de {PROV}'))


    else:
        if CCAA_types == 'TODAS' and PROV_types == 'TODAS' and municipio_types == 'TODOS':
            df = df_final_pob_round_melt_PC_object_color
            df= df.loc[(df['Descripción']==partida_de_coste_types)& (df['coste_efectivo_PC'] > 0)]

            fig = px.box(df , y='coste_efectivo_PC' , labels={'coste_efectivo_PC': 'Coste por habitante PC'} ,
                         hover_name='Nombre Ente Principal' , hover_data={'Población': ':,' , 'color': False ,
                                                                          'coste_efectivo_PC': ":,€"} , template='seaborn' ,
                         color='color' , color_discrete_map={'color': 'rgb(42, 35, 160)'})

            fig.update_layout(xaxis=dict(title='Total Municipios'))


        elif CCAA_types != 'TODAS' and PROV_types == 'TODAS' and municipio_types == 'TODOS':

            df = df_final_pob_round_melt_PC_object_color[df_final_pob_round_melt_PC_object_color['CCAA'] == CCAA_types]
            df = df.loc[(df['Descripción'] == partida_de_coste_types) & (df['coste_efectivo_PC'] > 0)]

            fig = px.box(df , y='coste_efectivo_PC' , labels={'coste_efectivo_PC': 'Coste por habitante PC'} ,
                         hover_name='Nombre Ente Principal' , hover_data={'Población': ':,' , 'color': False ,
                                                                          'coste_efectivo_PC': ":,€"} ,
                         template='seaborn' ,
                         color='color' , color_discrete_map={'color': 'rgb(42, 35, 160)'})

            fig.update_layout(xaxis=dict(title=f'Municipios de {CCAA_types}'))


        elif CCAA_types != 'TODAS' and PROV_types != 'TODAS' and municipio_types == 'TODOS':

            df = df_final_pob_round_melt_PC_object_color[df_final_pob_round_melt_PC_object_color['Provincia'] == PROV_types]
            df = df.loc[(df['Descripción'] == partida_de_coste_types) & (df['coste_efectivo_PC'] > 0)]

            fig = px.box(df , y='coste_efectivo_PC' , labels={'coste_efectivo_PC': 'Coste por habitante PC'} ,
                         hover_name='Nombre Ente Principal' , hover_data={'Población': ':,' , 'color': False ,
                                                                          'coste_efectivo_PC': ":,€"} ,
                         template='seaborn' ,
                         color='color' , color_discrete_map={'color': 'rgb(42, 35, 160)'})

            fig.update_layout(xaxis=dict(title=f'Municipios de {PROV_types}'))



        elif CCAA_types == 'TODAS' and PROV_types != 'TODAS' and municipio_types == 'TODOS':

            df = df_final_pob_round_melt_PC_object_color[df_final_pob_round_melt_PC_object_color['Provincia'] == PROV_types]
            df = df.loc[(df['Descripción'] == partida_de_coste_types) & (df['coste_efectivo_PC'] > 0)]

            fig = px.box(df , y='coste_efectivo_PC' , labels={'coste_efectivo_PC': 'Coste por habitante PC'} ,
                         hover_name='Nombre Ente Principal' , hover_data={'Población': ':,' , 'color': False ,
                                                                          'coste_efectivo_PC': ":,€"} ,
                         template='seaborn' ,
                         color='color' , color_discrete_map={'color': 'rgb(42, 35, 160)'})

            fig.update_layout(xaxis=dict(title=f'Municipios de {PROV_types}'))



        else:

            PROV = MUNI_CO.loc[MUNI_CO['Nombre Ente Principal'] == municipio_types , 'Provincia'].to_list()
            PROV = PROV[0]

            df = df_final_pob_round_melt_PC_object_color[df_final_pob_round_melt_PC_object_color['Provincia'] == PROV]
            df = df.loc[(df['Descripción'] == partida_de_coste_types) & (df['coste_efectivo_PC'] > 0)]

            fig = px.box(df , y='coste_efectivo_PC' , labels={'coste_efectivo_PC':'Coste por habitante PC'} ,
                         hover_name='Nombre Ente Principal' , hover_data={'Población': ':,' , 'color': False ,
                                                                          'coste_efectivo_PC': ":,€"} ,
                         template='seaborn' ,
                         color='color' , color_discrete_map={'color': 'rgb(42, 35, 160)'})

            fig.update_layout(xaxis=dict(title=f'Municipios de {PROV}'))





    fig.update_layout( yaxis=dict(gridcolor='#cacaca',zerolinecolor='#929292' ,
                          title='Coste €/hab.' ,
                          titlefont_size=16 ,
                          tickfont_size=12 , showticklabels=True , color='rgb(50, 50, 50)') ,
                      xaxis=dict(showline=False , linecolor='#929292' , linewidth=0.5,titlefont_size=16 ,tickfont_size=14,
                    color='rgb(50, 50, 50)'),plot_bgcolor="#F9F9F9" ,paper_bgcolor="#F9F9F9" , title_font_color='rgb(50, 50, 50)',showlegend=False)




    fig.update_layout(margin={"r": 20 , "t": 40 , "l": 20 , "b": 20})

    if partida_de_coste_types == 'TODOS':
        fig.update_layout(title=f'Coste por habitante Total',yaxis=dict(title='Coste €/hab.'))

    else:
        fig.update_layout(title=f'Coste por habitante por Partida de coste',yaxis=dict(title=f'Coste €/hab., {partida_de_coste_types}'))

    return fig




# Main
if __name__ == "__main__":
    app.run_server(debug=False)

    ########### debug FALSE
