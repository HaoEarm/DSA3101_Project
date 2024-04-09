import dash
from dash import html

dash.register_page(__name__, path='/test', name="Testing :)")


layout = html.Div(children=[
    html.Div(children=[
        html.H2("Hi"),
        "testing",
        html.Br(),html.Br(),
        "testing2",
        html.Br(), html.Br(),
        "testing3"])
    ])