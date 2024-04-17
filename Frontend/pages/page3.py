# import dash
# from dash import html

# dash.register_page(__name__, path='/test', name="Testing :)")


# layout = html.Div(children=[
#     html.Div(children=[
#         html.H2("Hi"),
#         "testing",
#         html.Br(),html.Br(),
#         "testing2",
#         html.Br(), html.Br(),
#         "testing3"])
#     ])


import dash
from dash import html, register_page, callback # If you need callbacks, import it here.
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output
import pandas as pd
import base64
import plotly.graph_objects as go
from flask import Flask
import os
import plotly.express as px
#import charts

register_page(
    __name__,
    name='Page 3',
    top_nav=True,
    path='/page3'
)


# def layout():
#     layout = html.Div([
#         html.H1(
#             [
#                 "Page 3"
#             ]
#         )
#     ])
#     return layout


df3 = pd.read_csv("https://raw.githubusercontent.com/HaoEarm/DSA3101_Project/main/Data/predictions.csv")
df3['Sentiment'] = df3['Positive'].apply(lambda x: 1 if x >= 0.5 else 0)


####################### HISTOGRAM ###############################
def create_distribution3(bank):
    subset_df3 = df3[df3['Bank'] == bank]
    return px.histogram(data_frame=subset_df3, x="Negative", height=600, color_discrete_sequence=['indianred'])



####################### WIDGETS ################################
banks3 = ['GXS Bank', 'Maribank', 'Revolut', 'Trust', 'Wise']
dd3 = dcc.Dropdown(id="bank3", options=banks3, value="GXS Bank", clearable=False)


####################### LAYOUT ################################
def layout():
    title = html.Div([
        html.H1(
            [
                "Negative Sentiments"
            ]
        ),
        html.Br(),
        html.H3("Distribution of probability of whether a comment is negative, by banks")
    ])
    layout = html.Div(children=[
        html.Br(),
        html.P("Select Column:"),
        dd3,
        dcc.Graph(id="histogram3")
    ])
    return title, layout



####################### CALLBACKS ################################
@callback(Output("histogram3", "figure"), [Input("bank3", "value"), ])
def update_histogram3(bank3):
    return create_distribution3(bank3)