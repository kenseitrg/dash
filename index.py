import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from waitress import serve

from app import app
from apps import summary, seisboard, documents

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Информация", href="/", 
                    style={"fontSize": 16}, external_link=True)),
        dbc.NavItem(dbc.NavLink("Сейсмические работы", href="/apps/seisboard", 
                    style={"fontSize": 16}, external_link=True)),
        dbc.NavItem(dbc.NavLink("Документация", href="/apps/documents",
                    style={"fontSize": 16}, external_link=True))
    ],
    brand="Digital Supervisor 4.0",
    brand_href="/",
    color="primary",
    dark=True,
)

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    navbar,
    html.Div(id="page-content")
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname in ['/', '/apps/summary']:
        return summary.layout
    elif pathname == "/apps/seisboard":
        return seisboard.layout
    elif pathname == "/apps/documents":
        return documents.layout
    else:
        return '404'

if __name__ == "__main__":
    #app.run_server(debug=True, dev_tools_hot_reload=False)
    serve(app.server, host="127.0.0.1", port=8050)
