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
from datetime import datetime, timedelta

register_page(
    __name__,
    name='Page 2',
    top_nav=True,
    path='/page2'
)

# Getting the dataset
df2 = pd.read_csv("https://raw.githubusercontent.com/HaoEarm/DSA3101_Project/main/Data/predictions.csv")
df2['Date'] = pd.to_datetime(df2['Date'])
# Sort by date
df2.sort_values(by=['Date'], inplace=True)
# Monthly rolling sum of sentiments
df2['cum_pos'] = df2.rolling(window="30D", on='Date')['Positive'].sum()
df2['cum_neg'] = df2.rolling(window="30D", on='Date')['Negative'].sum()
#Adding a label column
df2['Sentiment'] = df2['Positive'].apply(lambda x: 'Negative' if x < 0.33 else 'Neutral' if (x >= 0.33 and x < 0.63) else 'Positive')



####################### HISTOGRAM & BARCHART ###############################
def create_histogram2(bank):
    if bank == "Overall":
        subset_df2 = df2
    else:
        subset_df2 = df2[df2['Bank'] == bank]
    hist = px.histogram(data_frame=subset_df2, x="Positive",
                       height = 800)
    hist.update_layout(font = dict(size=16), xaxis_title="Sentiment Score", yaxis_title="Count")
    return hist

def create_line2(bank):
    if bank == "Overall":
        subset_df2 = df2
    else:
        subset_df2 = df2[df2['Bank'] == bank]

    subset_df2 = subset_df2.assign(Ones=1)
    wide_df = subset_df2.pivot_table(index='Date', columns='Sentiment', values="Ones", aggfunc="sum")
    wide_df = wide_df.reset_index()

    grouped_data = wide_df.groupby(pd.Grouper(key='Date', freq='Y'))

    # Perform an operation on the grouped data
    result1 = grouped_data['Negative'].sum()
    result2 = grouped_data['Neutral'].sum()
    result3 = grouped_data['Positive'].sum()
    result1 = result1.reset_index()
    result2 = result2.reset_index().Neutral
    result3 = result3.reset_index().Positive

    result = pd.concat([result1, result2, result3], axis=1)
    # line = go.FigureWidget()
    # line.add_scatter(name="Positive", x=result.Date, y=result.Positive, fill="tonexty")
    # line.add_scatter(name="Neutral", x=result.Date, y=result.Neutral, fill="tonexty")
    # line.add_scatter(name="Negative", x=result.Date, y=result.Negative, fill="tonexty")
    # line.update_layout(xaxis_title="Year", yaxis_title="Number of Sentiments")
    
    dates = result.Date
    # Decrease the x axi years by one year to get correct display
    dates_minus_one_year = [date - timedelta(days=365) for date in dates]
    x_labels = [date.strftime('%Y-%m-%d') for date in dates_minus_one_year]
    line = go.Figure(go.Bar(x=x_labels, y=result.Positive, name='Positive'))
    line.add_trace(go.Bar(x=x_labels, y=result.Neutral, name='Neutral'))
    line.add_trace(go.Bar(x=x_labels, y=result.Negative, name='Negative'))

    line.update_layout(barmode='stack', xaxis={'categoryorder':'category ascending'},
                       xaxis_title="Year", yaxis_title="Number of Sentiments", width=1900,
                       height = 900, font = dict(size=16))


    return line




def layout():
    layout = html.Div([
        html.Br(),
        html.H1(
            [
                "Further Breakdown of Sentiments"
            ],
            style={'backgroundColor': '#333', 'color': 'white'}
        ),
        dcc.Dropdown(id = 'bank',
                              options = ['Overall','GXS Bank', 'Maribank', 'Revolut', 'Trust', 'Wise'],
                              value = 'Overall',
                              clearable = False
                              ),
        html.Br(),
        html.Br(),
        dbc.Row(
            [dbc.Col(
                    [html.Div(["Number of Sentiments Overtime"], style={"fontSize":30}),
                     html.Div([dcc.Graph(id = 'line2')], style={'height': '800%', 'width': '100%'})]
                ),
                dbc.Col(
                    [html.Div(["Distribution of Sentiment Scores"], style={"fontSize":30}), 
                    dcc.Graph(id = 'histogram2')  
                    ]
                )
            ]
        )
    ])
    return layout









####################### CALLBACKS ################################
@callback(Output("histogram2", "figure"), [Input("bank", "value"), ])
def update_histogram2(bank):
    return create_histogram2(bank)

@callback(Output("line2", "figure"), [Input("bank", "value"), ])
def update_line2(bank):
    return create_line2(bank)







