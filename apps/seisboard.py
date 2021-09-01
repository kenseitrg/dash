import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output
import holoviews as hv
from holoviews.operation.datashader import datashade
from holoviews.plotting.plotly.dash import to_dash

from app import app, stats_df, acq_df

date_picker = dcc.DatePickerRange(
    id="acq-date-range", min_date_allowed=stats_df.index.min(), max_date_allowed=stats_df.index.max(), 
    initial_visible_month=stats_df.index.min(), end_date=stats_df.index.max(), start_date=stats_df.index.min())

cards = dbc.CardDeck([
    dbc.Card(
        [html.Div(id="acq-plot")], body=True),
    dbc.Card([dbc.ListGroup([
        date_picker,
        dbc.ListGroupItem(id="total-shots-text"),
        dbc.ListGroupItem(id="planned-shots-text"),
        dbc.ListGroupItem(id="acquired-shots-text"),
        dbc.ListGroupItem(id="forecasted-shots-text"),
        dbc.ListGroupItem(html.Div([dcc.Graph(id="plan-indicators")])),
    ])], body=True),
    dbc.Card(
        [html.Div([dcc.Graph(id="stats-indicator")])], body=True),
])

layout = dbc.Container([
    dbc.Row(dbc.Col([cards], width=12), justify="center"),
    dbc.Row([dbc.Col(dbc.Card([html.Div([dcc.Graph(id="stats-graph")])], body=True))
    ], justify="center")
], style={'max-width': '100%'})

def update_acq_plot(df):
    hv_preplot = hv.Dataset(df)
    points = hv.Points(hv_preplot, ["X", "Y"]).opts(color="green")
    tiles = hv.element.tiles.EsriImagery()
    overlay = tiles * datashade(points)
    overlay.opts(margins=(1, 1, 1, 1))
    return to_dash(app, [overlay], responsive=True).graphs

def update_stats_indicator(date):
    stats_indicator = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=stats_df.loc[date, "Actual"],
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Статистика за день"},
        delta={'reference': stats_df.loc[date,"Forecast"]},
        gauge={
            'axis': {'range': [0, 1200], },
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'threshold': {
                'line': {'color': "red"},
                'value': stats_df.loc[date,"Forecast"]}
        }
    ))
    stats_indicator.update_layout(margin={"r": 1, "t": 1, "l": 1, "b": 1})
    return stats_indicator

def update_stats_grpaph(df):
    stats_plot = make_subplots(specs=[[{"secondary_y": True}]])
    stats_plot.add_trace(
        go.Bar(name="План", x=df.index, y=df.Planned), secondary_y=False)
    stats_plot.add_trace(
        go.Bar(name="Факт", x=df.index, y=df.Actual), secondary_y=False)
    stats_plot.add_trace(
        go.Bar(name="Прогноз", x=df.index, y=df.Forecast), secondary_y=False)
    stats_plot.add_trace(go.Scattergl(name="Суммарный план",
                                      x=df.index, y=df.Planned_sum), secondary_y=True)
    stats_plot.add_trace(go.Scattergl(name="Суммарный факт",
                                    x=df.index, y=df.Actual_sum), secondary_y=True)
    stats_plot.update_xaxes(title="Дата")
    stats_plot.update_layout(barmode="group", margin={
                            "r": 1, "t": 1, "l": 1, "b": 1})
    return stats_plot

def update_text_indicators(df):
    total_shots = int(stats_df.Planned.sum())
    planned_shots = int(df.Planned.sum())
    acq_shots = int(df.Actual.sum())
    forecast_shots = int(df.Forecast.sum())
    total_shots_txt = f"Всего ПВ: {total_shots}"
    planned_shots_txt = f"План ПВ за период: {planned_shots}"
    acq_shots_txt = f"Факт ПВ за период: {acq_shots}"
    forecast_shots_txt = f"Прогноз ПВ за период: {forecast_shots}"
    plan_indicator = go.Indicator(
        mode="delta",
        value=acq_shots,
        domain={'x': [0, 1], 'y': [0., 0.4]},
        title={'text': "Факт/План", "font.size": 24},
        delta={'reference': planned_shots, "relative": True, "font.size": 24},
    )
    forecast_indicator = go.Indicator(
        mode="delta",
        value=acq_shots,
        domain={'x': [0, 1], 'y': [0.5, 0.9]},
        title={'text': "Факт/Прогноз", "font.size": 24},
        delta={'reference': forecast_shots, "relative": True, "font.size": 24},
    )
    indicators = go.Figure()
    indicators.add_trace(plan_indicator)
    indicators.add_trace(forecast_indicator)
    indicators.update_layout(
        margin={"r": 1, "t": 1, "l": 1, "b": 1}, height=200)
    return (total_shots_txt, planned_shots_txt, acq_shots_txt, forecast_shots_txt, indicators)


@app.callback([Output("stats-indicator", "figure"), Output("stats-graph", "figure"), 
                Output("total-shots-text", "children"), Output("planned-shots-text", "children"), 
                Output("acquired-shots-text", "children"), Output("forecasted-shots-text", "children"),
               Output("acq-plot", "children"), Output("plan-indicators", "figure")],
            [Input("acq-date-range", "start_date"), Input("acq-date-range", "end_date")])
def update_display(start_date, end_date):
    indicator = update_stats_indicator(pd.to_datetime(end_date))
    stats_graph = update_stats_grpaph(stats_df.loc[pd.to_datetime(start_date):pd.to_datetime(end_date)])
    total_shots_txt, planned_shots_txt, acq_shots_txt, forecast_shots_txt, indicators = update_text_indicators(
        stats_df.loc[pd.to_datetime(start_date):pd.to_datetime(end_date)])
    acq_plot = update_acq_plot(
        acq_df[pd.to_datetime(start_date):pd.to_datetime(end_date)])
    return indicator, stats_graph, total_shots_txt, planned_shots_txt, acq_shots_txt, forecast_shots_txt, acq_plot, indicators
