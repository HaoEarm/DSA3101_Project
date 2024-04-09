import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output

dash.register_page(__name__, path='/analysis', name="Analysis 📊")

####################### LOAD DATASET #############################
df = pd.read_csv("output.csv")

####################### HISTOGRAM ###############################
def create_distribution(col_name="Revolut"):
    return px.histogram(data_frame=df, x="Sentiment", height=600)

####################### WIDGETS ################################
columns = ["Revolut"]
dd = dcc.Dropdown(id="dist_column", options=columns, value="Revolut", clearable=False)

####################### PAGE LAYOUT #############################
layout = html.Div(children=[
    html.Br(),
    html.P("Select Column:"),
    dd,
    dcc.Graph(id="histogram")
])

####################### CALLBACKS ################################
@callback(Output("histogram", "figure"), [Input("dist_column", "value"), ])
def update_histogram(dist_column):
    return create_distribution(dist_column)

