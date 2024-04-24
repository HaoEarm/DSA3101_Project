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
import numpy as np
from numpy import radians, cos, sin
import base64
import requests

register_page(
    __name__,
    name='Home',
    top_nav=True,
    path='/'
)


preds = pd.read_csv("https://raw.githubusercontent.com/HaoEarm/DSA3101_Project/main/Data/predictions.csv")
preds['Date'] = pd.to_datetime(preds['Date'])
# Sort by date
preds.sort_values(by=['Date'], inplace=True)
# Monthly rolling sum of sentiments
preds['cum_pos'] = preds.rolling(window="30D", on='Date')['Positive'].sum()
preds['cum_neg'] = preds.rolling(window="30D", on='Date')['Negative'].sum()
# Separate into GXS vs Other Banks:
preds_GXS = preds.loc[preds['Bank'].eq('GXS Bank')]
preds_rest = preds[(preds.Bank != 'GXS Bank')]
#GXS
preds_GXS = preds.loc[preds['Bank'].eq('GXS Bank')]
#Other banks
preds_rest = preds[(preds.Bank != 'GXS Bank')]
#Adding a label column
preds['Sentiment'] = preds['Positive'].apply(lambda x: 'Negative' if x < 0.33 else 'Neutral' if (x >= 0.33 and x < 0.63) else 'Positive')




# Getting Image Icon
# Download and save the images
def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
    else:
        print(f'Failed to download image from {url}')

# URLs for the images
url = 'https://raw.githubusercontent.com/HaoEarm/DSA3101_Project/main/Frontend/comment_icon.png'



# Download images
download_image(url, 'comment_icon.png')



def layout():

    # Encode image to base64
    def encode_image(image_file):
        with open(image_file, 'rb') as file:
            encoded = base64.b64encode(file.read()).decode('ascii')
        return f"data:image/png;base64,{encoded}"

    layout = html.Div([
        html.Br(),
        html.H1(
            [
                "Sentiment Analysis Dashboard"
            ],
            style={'backgroundColor': '#333', 'color': 'white'}
        ),
        dbc.Row(
            [dbc.Col(
                dbc.Row(
                    [html.Div(["Select Bank:"]), 
                    dcc.Dropdown(id = 'Banks',
                                options = ['Overall','GXS Bank', 'Maribank', 'Revolut', 'Trust', 'Wise'],
                                value = 'Overall',
                                clearable = False
                                ),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Div([
                    html.Img(src=encode_image('comment_icon.png'), style={'height': '100%', 'width': '30%','display': 'inline-block'}, className = 'center'),
                    html.Div(id="stat", style={'textAlign': 'center', 'fontSize': 40, 'display': 'inline-block'})          
                    ], style={"textAlign":"center"})
                    ]),
                   
            ),
            dbc.Col(
                [dcc.Graph(id='indicator-output')]
            ),
            dbc.Col(
                [dcc.Graph(id='pie-output')]
            )]
        ),
        html.Br(),
        html.Div(["Cumulative Sentiment Score Overtime"], style={'fontSize':30}),
        dbc.Row(
            [dcc.Dropdown(id="multi", multi=True, options=['Overall (Average Across All Banks)','GXS Bank', 'Maribank', 'Revolut', 'Trust', 'Wise'],
                          value=["Overall (Average Across All Banks)"]),
                dcc.Graph(id='multi-graph')]
        )
    ])
    return layout


# Callback for indicator
@callback(Output("indicator-output", "figure"), [Input("Banks", "value"), ])
def update_indicator(bank):
    #Get filtered dataset
    if bank == "Overall":
        subset_df = preds
    else:
        subset_df = preds.loc[preds['Bank'].eq(bank)]
    # Indicator
    indicator = go.Figure(
        go.Indicator(
        mode = "gauge+number",
        number = {'suffix': " out of 1", 'font': {'size': 30}},
        #title = {'text': 'Average Sentiment Score', 'font': {'size': 15}},
        value = round(subset_df["Positive"].mean(),2),
        domain = {'x': [0,1], 'y': [0,1]},
        gauge = {
            'axis': {'range': [None, 1], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color':'rgba(0,0,0,0)'},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "white",
            'steps': [
                {'range': [0, 0.33], 'color': 'red'},
                {'range': [0.33, 0.63], 'color': 'yellow'},
                {'range': [0.63,1], 'color': 'green'}],
            },
        ),
    )

    indicator.update_layout(
        #font={'size':20},
        xaxis={'showgrid': False, 'showticklabels':False, 'range':[-0.7,0.7]},
        yaxis={'showgrid': False, 'showticklabels':False, 'range':[0,1]},
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
        )

    indicator.add_annotation(x=-0.7, y=0.3, text="<b>Negative</b>", showarrow=False, font=dict(size=16))
    indicator.add_annotation(x=0, y=0.75, text="<b>Neutral</b>", showarrow=False, font=dict(size=16))
    indicator.add_annotation(x=0.7, y=0.3, text="<b>Positive</b>", showarrow=False, font=dict(size=16))
    indicator.add_annotation(x=0, y=1, text='Average Sentiment Score', showarrow=False, font=dict(size=20))
    
    ## by setting the range of the layout, we are effectively adding a grid in the background
    ## and the radius of the gauge diagram is roughly 0.9 when the grid has a range of [-1,1]x[0,1]

    theta = (1-subset_df["Positive"].mean())*180 + 5
    r = 0.75
    x_head = r * cos(radians(theta))
    y_head = r * sin(radians(theta))

    indicator.add_annotation(
        ax=0,
        ay=0.2,
        axref='x',
        ayref='y',
        x=x_head,
        y=y_head,
        xref='x',
        yref='y',
        showarrow=True,
        arrowhead=3,
        arrowsize=1,
        arrowwidth=4
        )
    return indicator
    


# Callback for piechart
@callback(Output("pie-output", "figure"), [Input("Banks", "value"), ])
def update_pie(bank):
    #Get filtered dataset
    if bank == "Overall":
        subset_df = preds
    else:
        subset_df = preds.loc[preds['Bank'].eq(bank)]
    # Create Pie Chart
    pie = go.Figure(
        px.pie(subset_df, 
               names='Sentiment', 
               title='Proportion of sentiments',
               color='Sentiment',
               color_discrete_map={'Positive':'Green',
                                 'Neutral':'Yellow',
                                 'Negative':'Red',
                                 })
    )
    pie.update_layout(title_x=0.5, font=dict(size=16), paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)')
    return pie



#Callback for statistic
@callback(Output("stat", "children"), [Input("Banks", "value"), ])
def update_graph(bank):
    #Get filtered dataset
    if bank == "Overall":
        subset_df = preds
    else:
        subset_df = preds.loc[preds['Bank'].eq(bank)]
    # Create graph
    return [f"{len(subset_df)} Reviews"]



# Callback for graph
@callback(Output("multi-graph", "figure"), [Input("multi", "value"), ])
def update_graph(bank):
    #print(bank)
    if ("Overall (Average Across All Banks)" in bank) and (len(bank)==1):
        # Create only overall graph
        graph = px.line(preds, x="Date", y="cum_pos",
                labels={"cum_pos": "Cumulative Sentiment Score"})
        graph.update_layout(height = 600)
        return graph
    elif ("Overall (Average Across All Banks)" in bank) and (len(bank) > 1):
        # Create both overall and other graphs
        bank.remove("Overall (Average Across All Banks)")
        subset_df = preds[preds["Bank"].isin(bank)]
        graph = px.line(subset_df, x="Date", y="cum_pos", color="Bank",
                labels={"cum_pos": "Cumulative Sentiment Score"})
        graph.add_scatter(name="Overall", x=preds.Date, y=preds.cum_pos)
        graph.update_layout(height = 600)
        return graph
    else:
        subset_df = preds[preds["Bank"].isin(bank)]
        graph = px.line(subset_df, x="Date", y="cum_pos", color="Bank",
                    labels={"cum_pos": "Cumulative Sentiment Score"})
        graph.update_layout(height = 600)
        return graph
    # subset_df = preds[preds["Bank"].isin(bank)]
    # graph = px.line(subset_df, x="Date", y="cum_pos", color="Bank",
    #         labels={"cum_pos": "Cumulative Sentiment Score"})
    # graph.add_scatter(name="Overall", x=preds.Date, y=preds.cum_pos)
    # return graph

    
    


