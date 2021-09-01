import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import geopandas as gpd
import plotly.express as px
import holoviews as hv
from holoviews.plotting.plotly.dash import to_dash

from app import summary_df, preplot_raster_graph

layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Западная Мессояха"), width={"size": 6, "offset": 3})
    ], justify="center"),
    dbc.Row([
        dbc.Col(html.H4("Заказчик: АО «МЕССОЯХАНЕФТЕГАЗ»"), width=4),
        dbc.Col(html.H4("Исполнитель: ООО ТНГ-Групп «Югра-сервис»"), width=4),
        dbc.Col(html.H4("Супервайзинг: АО «ЦГЭ»"), width=4)
    ], justify="center"),
    dbc.Row([
        dbc.Col(dbc.Card(
            dbc.CardBody(html.Div(preplot_raster_graph))
        ), width=7, style={"height": "80vh"}, align="top"),
        dbc.Col([
            dbc.Card(
                dbc.CardBody(dbc.Table.from_dataframe(summary_df, striped=True, bordered=True,
                             hover=True, responsive=True, style={"fontSize": 10}))
            )
        ], width=5, style={"height": "80vh"}, align="top")
    ])
], style={'max-width': '100%'})

