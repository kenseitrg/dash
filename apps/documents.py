import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import os

icons = {"pdf": f"/static/img/pdf_icon.png",
         "xlsx": f"/static/img/xlsx_icon.png", 
         "rar": f"/static/img/rar_icon.png"}

def create_cards():
    def make_card(f):
        card = dbc.Card([
            html.H4(f.split(".")[0], className="card-title"),
            dbc.CardImg(src=icons[f.split(".")[1]]),
            dbc.CardLink(f, href=f"file:///data/example/{f}")
        ], style={"width": "22rem"})
        return card  
    cards = [make_card(f) for f in os.listdir(f"data/example")]
    return dbc.CardColumns(cards)

layout = dbc.Container([
    dbc.Row(dbc.Col([create_cards()], width=12), justify="center"),
], style={'max-width': '80%'})
