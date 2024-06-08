#Projeto Desenvolvimento Rápido de Aplicações em Python
#Alunos: Gleyson Souza, João Pedro e João Gabriel
#PROF.: Msc Kayo Henrique de Carvalho Monteiro


#-=- Bibliotecas usadas -=-

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import json

#-=====================================================================================================-

#-=- Manipulação dos dados -=-

# df1 = pd.read_csv("datasets/HIST_PAINEL_COVIDBR_2020_Parte1_03mai2024.csv", sep=";")
# df2 = pd.read_csv("datasets/HIST_PAINEL_COVIDBR_2020_Parte2_03mai2024.csv", sep=";")
# df3 = pd.read_csv("datasets/HIST_PAINEL_COVIDBR_2021_Parte1_03mai2024.csv", sep=";")
# df4 = pd.read_csv("datasets/HIST_PAINEL_COVIDBR_2021_Parte2_03mai2024.csv", sep=";")
# df5 = pd.read_csv("datasets/HIST_PAINEL_COVIDBR_2022_Parte1_03mai2024.csv", sep=";")
# df6 = pd.read_csv("datasets/HIST_PAINEL_COVIDBR_2022_Parte2_03mai2024.csv", sep=";")
# df7 = pd.read_csv("datasets/HIST_PAINEL_COVIDBR_2023_Parte1_03mai2024.csv", sep=";")
# df8 = pd.read_csv("datasets/HIST_PAINEL_COVIDBR_2023_Parte2_03mai2024.csv", sep=";")
# df9 = pd.read_csv("datasets/HIST_PAINEL_COVIDBR_2024_Parte1_03mai2024.csv", sep=";")
# df_definitivo = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9])
# df_estados = df_definitivo[(~df_definitivo["estado"].isna()) & (df_definitivo["codmun"].isna())]
# df_brasil = df_definitivo[df_definitivo["regiao"] == "Brasil"]
# df_estados.to_csv("datasets/df_estados.csv")
# df_brasil.to_csv("datasets/df_brasil.csv")

#-=====================================================================================================-

#-=- Carregamento dos dados -=-

df_estados = pd.read_csv("datasets/df_estados.csv")
df_brasil = pd.read_csv("datasets/df_brasil.csv")

mapa = json.load(open("geojson/brasil_geo.json", "r"))

mapa["features"][0].keys()

df_estados_ = df_estados[df_estados["data"] == "2024-02-13"]
colunas_selecionadas = {"casosAcumulado": "Casos Acumulados", 
                "casosNovos": "Novos Casos", 
                "obitosAcumulado": "Óbitos Totais",
                "obitosNovos": "Óbitos por dia"}

#-=====================================================================================================-

#-=- Instânciação -=-

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])

fig = px.choropleth_mapbox(df_estados_, locations="estado",
    geojson=mapa, center={"lat": -14.95, "lon": -52.98},
    zoom=4, color="casosNovos", color_continuous_scale="brbg", opacity=0.4,
    hover_data={"casosAcumulado": True, "casosNovos": True, "obitosNovos": True, "estado": True}
    )

fig.update_layout(
    mapbox_style="carto-positron",
    autosize=True,
    margin=go.layout.Margin(l=0, r=0, t=0, b=0),
    showlegend=False,)
df_data = df_estados[df_estados["estado"] == "RO"]


fig2 = go.Figure(layout={"template":"plotly_white"})
fig2.add_trace(go.Scatter(x=df_data["data"], y=df_data["casosAcumulado"]))
fig2.update_layout(
    paper_bgcolor="#FFFFFF",
    plot_bgcolor="#FFFFFF",
    autosize=True,
    margin=dict(l=10, r=10, b=10, t=10),
    )

#-=====================================================================================================-

#-=- Layout  -=-

app.layout = dbc.Container(
    children=[
        dbc.Row([
            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=[dcc.Graph(id="choropleth-map", figure=fig, 
                            style={'height': '83vh', 'margin-right': '10px'})],
                    ),
                ], md=7),

            dbc.Col([
                    html.Div([
                        html.H5(children="Evolução COVID-19"),
                        dbc.Button("BRASIL", color="info", id="botao-localizacao", size="lg")
                    ], style={"background-color": "#F4FBF9", "margin": "-25px", "padding": "25px"}),
                    html.P("Informe a data na qual deseja obter informações:", style={"margin-top": "40px"}),
                    html.Div(
                            className="dropdown",
                            children=[
                                dcc.DatePickerSingle(
                                    id="date-picker",
                                    min_date_allowed=df_estados.groupby("estado")["data"].min().max(),
                                    max_date_allowed=df_estados.groupby("estado")["data"].max().min(),
                                    initial_visible_month=df_estados.groupby("estado")["data"].min().max(),
                                    date=df_estados.groupby("estado")["data"].max().min(),
                                    display_format="MMMM D, YYYY",
                                    style={"border": "2px solid #dbdbdb44"},
                                )
                            ],
                        ),
                    html.Div([
                        html.P("Selecione que tipo de dado deseja visualizar:", style={"margin-top": "25px"}),
                        dcc.Dropdown(
                                    id="localizacao-dropdown",
                                    options=[{"label": j, "value": i}
                                        for i, j in colunas_selecionadas.items()
                                    ],
                                    value="casosNovos",
                                    style={"margin-top": "10px"}
                                    ),
                        dcc.Graph(id="grafico-linha", figure=fig2, style={
                            "background-color": "#FFFFFF",
                            }),
                        ]),
                ], md=5, style={
                          "padding": "25px",
                          "background-color": "#F4FBF9"
                          }), 

            dbc.Row([
                    dbc.Col([dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    html.Div([
                                        html.Span("Casos recuperados", className="card-texto"),
                                        html.H3(style={"color": "#adfc92"}, id="casos-recuperados-texto"),
                                        html.Span("Em acompanhamento", className="card-texto"),
                                        html.H5(id="em-acompanhamento-texto"),
                                    ], className="col-md-6"),
                                    html.Div([
                                        dbc.CardImg(src="/assets/icons/icon-heart.png", style={"width": "50px", "height": "50px", "margin-left": "auto", "margin-right": "0"}),
                                    ], className="col-md-6 d-flex align-items-center justify-content-end")
                                ], className="row")
                            ])
                            ], color="light", outline=True, style={"margin-top": "10px",
                                    "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                    "color": "#000"})], md=4),
                    dbc.Col([dbc.Card([   
                            dbc.CardBody([
                                html.Div([
                                    html.Div([
                                        html.Span("Casos confirmados totais", className="card-texto"),
                                        html.H3(style={"color": "#389fd6"}, id="casos-confirmados-texto"),
                                        html.Span("Novos casos na data", className="card-texto"),
                                        html.H5(id="novos-casos-texto"),
                                    ], className="col-md-6"),
                                    html.Div([
                                        dbc.CardImg(src="/assets/icons/clipboard.png", style={"width": "50px", "height": "50px", "margin-left": "auto", "margin-right": "0"}),
                                    ], className="col-md-6 d-flex align-items-center justify-content-end")
                                ], className="row")
                            ])
                            ], color="light", outline=True, style={"margin-top": "10px",
                                    "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                    "color": "#000"})], md=4),
                    dbc.Col([dbc.Card([   
                            dbc.CardBody([
                                html.Div([
                                    html.Div([
                                        html.Span("Óbitos confirmados", className="card-texto"),
                                        html.H3(style={"color": "#b5b2b3"}, id="obitos-texto"),
                                        html.Span("Óbitos na data", className="card-texto"),
                                        html.H5(id="obitos-na-data-texto"),
                                    ], className="col-md-6"),
                                    html.Div([
                                        dbc.CardImg(src="/assets/icons/x.png", style={"width": "50px", "height": "50px", "margin-left": "auto", "margin-right": "0"}),
                                    ], className="col-md-6 d-flex align-items-center justify-content-end")
                                ], className="row")
                            ])
                            ], color="light", outline=True, style={"margin-top": "10px",
                                    "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                    "color": "#000"})], md=4),
                ], style={
                        "background-color": "#F4FBF9"
                        }),
            ])
    ], fluid=True, 
)

#-=====================================================================================================-

#-=- Interatividade  -=-

@app.callback(
    [
        Output("casos-recuperados-texto", "children"),
        Output("em-acompanhamento-texto", "children"),
        Output("casos-confirmados-texto", "children"),
        Output("novos-casos-texto", "children"),
        Output("obitos-texto", "children"),
        Output("obitos-na-data-texto", "children"),
    ], [Input("date-picker", "date"), Input("botao-localizacao", "children")]
)
def display_status(date, location):
    if location == "BRASIL":
        df_data_on_date = df_brasil[df_brasil["data"] == date]
    else:
        df_data_on_date = df_estados[(df_estados["estado"] == location) & (df_estados["data"] == date)]

    recuperados_novos = "-" if df_data_on_date["Recuperadosnovos"].isna().values[0] else f'{int(df_data_on_date["Recuperadosnovos"].values[0]):,}'.replace(",", ".") 
    acompanhamentos_novos = "-" if df_data_on_date["emAcompanhamentoNovos"].isna().values[0]  else f'{int(df_data_on_date["emAcompanhamentoNovos"].values[0]):,}'.replace(",", ".") 
    casos_acumulados = "-" if df_data_on_date["casosAcumulado"].isna().values[0]  else f'{int(df_data_on_date["casosAcumulado"].values[0]):,}'.replace(",", ".") 
    casos_novos = "-" if df_data_on_date["casosNovos"].isna().values[0]  else f'{int(df_data_on_date["casosNovos"].values[0]):,}'.replace(",", ".") 
    obitos_acumulado = "-" if df_data_on_date["obitosAcumulado"].isna().values[0]  else f'{int(df_data_on_date["obitosAcumulado"].values[0]):,}'.replace(",", ".") 
    obitos_novos = "-" if df_data_on_date["obitosNovos"].isna().values[0]  else f'{int(df_data_on_date["obitosNovos"].values[0]):,}'.replace(",", ".") 
    return (
            recuperados_novos, 
            acompanhamentos_novos, 
            casos_acumulados, 
            casos_novos, 
            obitos_acumulado, 
            obitos_novos,
            )


@app.callback(
        Output("grafico-linha", "figure"),
        [Input("localizacao-dropdown", "value"), Input("botao-localizacao", "children")]
)
def plot_line_graph(plot_type, location):
    if location == "BRASIL":
        df_data_on_location = df_brasil.copy()
    else:
        df_data_on_location = df_estados[(df_estados["estado"] == location)]
    fig2 = go.Figure(layout={"template":"plotly_white"})
    bar_plots = ["casosNovos", "obitosNovos"]

    if plot_type in bar_plots:
        fig2.add_trace(go.Bar(x=df_data_on_location["data"], y=df_data_on_location[plot_type]))
    else:
        fig2.add_trace(go.Scatter(x=df_data_on_location["data"], y=df_data_on_location[plot_type]))
    
    fig2.update_layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        autosize=True,
        margin=dict(l=10, r=10, b=10, t=10),
        )
    return fig2


@app.callback(
    Output("choropleth-map", "figure"), 
    [Input("date-picker", "date")]
)
def update_map(date):
    df_data_on_states = df_estados[df_estados["data"] == date]

    fig = px.choropleth_mapbox(df_data_on_states, locations="estado", geojson=mapa, 
        center={"lat": -14.95, "lon": -52.98},
        zoom=3.5, color="casosAcumulado", color_continuous_scale="brbg", opacity=0.55,
        hover_data={"casosAcumulado": True, "casosNovos": True, "obitosNovos": True, "estado": False}
        )

    fig.update_layout(paper_bgcolor="#D4DADC", mapbox_style="carto-positron", autosize=True,
                    margin=go.layout.Margin(l=0, r=0, t=0, b=0), showlegend=False)
    return fig


@app.callback(
    Output("botao-localizacao", "children"),
    [Input("choropleth-map", "clickData"), Input("botao-localizacao", "n_clicks")]
)
def update_location(click_data, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if click_data is not None and changed_id != "botao-localizacao.n_clicks":
        state = click_data["points"][0]["location"]
        return "{}".format(state)
    
    else:
        return "BRASIL"

if __name__ == "__main__":
    app.run_server(debug=True)

#-=====================================================================================================-