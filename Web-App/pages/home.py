import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')

first_card = dbc.Card(
    dbc.CardBody(
        [
            html.H4(children='Situation'),
            html.P(children =  'A vast amount of sales data comprising of Customer description, Product description, order details and delivery details has  been provided.' ),
            html.P(children =  'We need to clean, query and transform to demonstrate the process of using our dashboard for gaining business insights.' ),  
        ], 
        style = {'text-align':'center'}))


second_card = dbc.Card(
    dbc.CardBody(
        [
            html.H4(children='Complication'),
            html.P(children = 'The data has been stored in multiple sources, hence must be streamed together into an individual pipeline.' ),
            html.P(children = 'Daily data dump with automated dashboard analysis updates.' )
        ], 
        style = {'text-align':'center'}))


third_card = dbc.Card(
    dbc.CardBody(
        [
            html.H4(children='Question'),
            html.P(children = 'The question we will address is "How can we increase company sales."'), 
        ], 
        style = {'text-align':'center'}))


fourth_card = dbc.Card(
    dbc.CardBody(
        [
            html.H4(children='Solution'),
            html.P(children = 'Implement a set of queries to gain insight on target audience, regional statistics and storage to customer turnover.'),
            html.P(children = 'Presenting all findings on a dashboard with interactive visualisations.' ),
            html.P(children = 'This solution will demonstrate that our dashboard meets client requirements.')
        ],
        style = {'text-align':'center'}))


overview_card = dbc.Card(
    dbc.CardBody(
        [
            html.H3(children='Overview'),
            html.P(children='Our client is a large nation-wide Toothbrush manufacturing and sales company.'),
            html.P(children='They have approached us with the task of creating a visualisation method for gaining business insights into sales data gathered over the last year and a half.'),
            html.P(children='They have requested a live dashboard to visualise key information, we have tackled this task using the following four point planning strategy; ')
        ], 
        style = {'text-align':'center'}))


cards = dbc.CardGroup(
    [
        first_card,
        second_card,
        third_card,
        fourth_card,
    ])


layout = html.Div(children=
[   
    overview_card,
    cards
])