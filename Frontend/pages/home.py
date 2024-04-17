# import dash
# from dash import html

# dash.register_page(__name__, path='/', name="Introduction 😃")

# ####################### PAGE LAYOUT #############################
# layout = html.Div(children=[
#     html.Div(children=[
#         html.H2("Sentiment Analysis"),
#         "Customer reviews are an important resource for improving service quality. We collate reviews from 5 different digital banks, and conduct sentiment analysis on them.",
#         html.Br(),html.Br(),
#         "In this dashboard, we will categorise the sentiments, analyse their trends, and provide recommendations for improvement.",
#     ]),
# ], className="bg-light p-4 m-2")


#---------------------------------------------------------



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
    name='Home',
    top_nav=True,
    path='/'
)


df = pd.read_csv("https://raw.githubusercontent.com/HaoEarm/DSA3101_Project/main/Data/predictions.csv")
df['Sentiment'] = df['Positive'].apply(lambda x: 1 if x >= 0.5 else 0)

# def layout():
#     layout1 = html.Div([
#         html.H1(
#             [
#                 "Home Page"
#             ]
#         )
#     ])
#     layout2 = html.Div([
#         html.H3(
#             [
#                 "No"
#             ]
#         )
#     ])

#     layout3 = html.Div([
#         html.Div([
#             html.H6(children='Global Cases',
#                     style={
#                         'textAlign': 'center',
#                         'color': 'black'}
#                     ),

#             html.P(1000,
#                    style={
#                        'textAlign': 'center',
#                        'color': 'orange',
#                        'fontSize': 40}
#                    ),

#             html.P("lol",
#                    style={
#                        'textAlign': 'center',
#                        'color': 'orange',
#                        'fontSize': 15,
#                        'margin-top': '-18px'}
#                    )], className="card_container three columns",
#                 )
#     ])
#     return layout1, layout2, layout3


####################### HISTOGRAM ###############################
def create_distribution(bank):
    subset_df = df[df['Bank'] == bank]
    return px.histogram(data_frame=subset_df, x="Positive", height=600)



####################### WIDGETS ################################
banks = ['GXS Bank', 'Maribank', 'Revolut', 'Trust', 'Wise']
dd = dcc.Dropdown(id="bank", options=banks, value="GXS Bank", clearable=False)


####################### LAYOUT ################################
def layout():
    title = html.Div([
        html.H1(
            [
                "Sentiment Analysis Dashboard"
            ]
        ),
        html.Br(),
        html.H3("Distribution of probability of whether a comment is positive, by banks")
    ])
    layout = html.Div(children=[
        html.Br(),
        html.P("Select Column:"),
        dd,
        dcc.Graph(id="histogram")
    ])
    return title, layout



####################### CALLBACKS ################################
@callback(Output("histogram", "figure"), [Input("bank", "value"), ])
def update_histogram(bank):
    return create_distribution(bank)



# @callback(Output("histogram", "figure"), [Input("column", "value"), ])
# def update_histogram2(column):
#     return create_distribution2(column)


# # Graph 2
# ####################### HISTOGRAM ###############################
# def create_distribution2(col_name="GXS Bank"):
#     return px.histogram(data_frame=df, x="Positive", height=600)

# ####################### WIDGETS ################################
# columns2 = ['GXS Bank', 'Maribank', 'Revolut', 'Trust', 'Wise']
# dd2 = dcc.Dropdown(id="column", options=columns2, value="GXS Bank", clearable=False)

# ####################### PAGE LAYOUT #############################
# layout2 = html.Div(children=[
#     html.Br(),
#     html.P("Select Column:"),
#     dd,
#     dcc.Graph(id="histogram")
# ])

# ####################### CALLBACKS ################################
# @callback(Output("histogram", "figure"), [Input("column", "value"), ])
# def update_histogram2(column):
#     return create_distribution2(column)








