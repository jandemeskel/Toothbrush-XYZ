import dash
from dash import dcc, html
from db import dispatched_time
import dash_bootstrap_components as dbc

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
        dcc.Graph(id='graph-output-3',figure=dispatched_time),
        insight
    ])

