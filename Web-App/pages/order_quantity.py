import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from db import order_frequency

dash.register_page(__name__)


insight = dbc.Card(
    dbc.CardBody(
        [
            html.H4(children='Key insights'),
            html.P(children='Will be filled in soon!' ),
        ])) 


layout = html.Div(
    children = 
    [
        dcc.Graph(id='graph-output-4',figure=order_frequency),
        insight
    ])

