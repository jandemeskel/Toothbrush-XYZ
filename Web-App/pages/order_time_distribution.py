import dash
from dash import Input, Output, callback, dcc, html
from db import order_time_distribution
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
        max = 24,
        step=1,
        count = 1,
        value=[0,24],
        allowCross = False,
        id = 'slider')


layout = html.Div(
    children = 
    [
        dcc.Graph(id='graph-output1'),
        slider,
        html.H4("Hour Range", style = {'text-align':'center'}),
        insight
    ])


@callback(
    Output('graph-output1','figure'),
    [Input('slider', 'value')])


def update_order_graph(input_value):

    lower = min(input_value)
    upper = max(input_value)
    order_time_df = order_time_distribution.query('@lower <= hour <= @upper')
    order_distribution = px.line( order_time_df,  x = 'hour', y = 'order_quantity', color = 'toothbrush_type')
    order_distribution.update_layout( title = 'Number of Orders per Toothbrush against time of day', yaxis_title = 'Product Order Count', xaxis_title = 'Hour of the day (Digital)',legend_title_text='Toothbrush Type')
    return  order_distribution

