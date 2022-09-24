import dash
from dash import Input, Output, callback, dcc, html
from db import delivery_status_df
import plotly.express as px
import dash_bootstrap_components as dbc

dash.register_page(__name__)


insight = dbc.Card(
    dbc.CardBody(
        [
            html.H4(children='Key insights'),
            html.P(children='Will be filled in soon!' ),
        ]))


slider = dcc.RangeSlider(
    min = 0,
    max = 23,
    step=1,
    count = 1,
    value=[0,23],
    allowCross = False,
    id = 'slider2')


layout = html.Div(
    children = 
    [
        dcc.Graph(id='graph-output2'),
        slider,
        html.H4("Hour Range", style = {'text-align':'center'}),
        insight
    ])


@callback(
    Output('graph-output2','figure'),
    [Input('slider2', 'value')]
)


def update_delivery_graph(input_value):

    lower = min(input_value)
    upper = max(input_value)
    monthly_del_status = delivery_status_df.query('@lower <= delivery_date <= @upper')
    delivery_status  = px.pie(monthly_del_status, values='pct_delivery', names='delivery_status')
    delivery_status.update_layout( title = 'Percentage of delivered orders', legend_title_text='Delivery Status')
    return  delivery_status


