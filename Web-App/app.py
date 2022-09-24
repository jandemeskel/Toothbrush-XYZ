import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.MINTY])

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}


CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


sidebar = html.Div(
    [
        html.H2("Dashboard Navigator"),
        html.Hr(),
        dbc.Nav(
            [
                dcc.Link(f"{page['name']}", href=page["relative_path"])
                for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True)
    ],
    style=SIDEBAR_STYLE)


logo = dbc.Card(
    dbc.CardBody(
        [
            html.Img(src='https://user-images.githubusercontent.com/5181870/186762844-8c0f0464-60b3-4dbf-b895-ed525d28f26e.png')
        ]))


app.layout = html.Div([
    sidebar,
    html.Div(
        id="page-content", 
        children=[logo, dash.page_container], 
        style=CONTENT_STYLE
        )])


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True, port=8080)


