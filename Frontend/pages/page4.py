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
    name='Page 4',
    top_nav=True,
    path='/page4'
)


# Getting the dataset
df4 = pd.read_csv("https://raw.githubusercontent.com/HaoEarm/DSA3101_Project/main/Data/predictions.csv")
conditions = [
    (df4['Score'] <= 2),
    (df4['Score'] == 3 ),
    (df4['Score'] >= 4)
]
values = ['Detractor', 'Passive', 'Promoter']
df4['NPS category Rating'] = np.select(conditions, values)
nps_scores = df4.groupby('Bank')['NPS category Rating'].value_counts(normalize=True).unstack().fillna(0)
nps_scores['nps'] = nps_scores['Promoter'] - nps_scores['Detractor']
nps_scores = nps_scores.reset_index()
nps_scores = nps_scores.sort_values(by=['nps'], ascending=[True])


bar = px.bar(nps_scores, x='Bank', y='nps',width=1600, height=700,
             labels={"nps": "Net Promoter Score"})
# bar.update_layout(
#     margin=dict(l=20, r=20, t=20, b=20),
#     paper_bgcolor="White",
# )


def layout():
    layout = html.Div([html.Br(),html.H1(["NPS Scores"], style={'backgroundColor': '#333', 'color': 'white'}),
                       html.Br(),
                       html.Div(["NPS Scores Across Banks"], style={"fontSize":30}),
    dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=bar)),
            ], justify='center'
        )
    ])
    return layout
    







# def download_image(url, filename):
#     response = requests.get(url)
#     if response.status_code == 200:
#         with open(filename, 'wb') as f:
#             f.write(response.content)
#     else:
#         print(f'Failed to download image from {url}')

# # URLs for the images
# url1 = 'https://raw.githubusercontent.com/HaoEarm/DSA3101_Project/main/Frontend/o_nps.png'

# # Download images
# download_image(url1, 'o_nps')





# def layout():
#     def encode_image(image_file):
#         with open(image_file, 'rb') as file:
#             encoded = base64.b64encode(file.read()).decode('ascii')
#         return f"data:image/png;base64,{encoded}"

#     layout = html.Div([
#         html.Br(),
#         html.H1("Net Promoter Score", style={'textAlign': 'center'}),
#         html.Img(src= encode_image("o_nps"),
#                  style={
#                 'height': '50%',
#                 'width': '50%',
#                 'textAlign': 'center'
#                 })
#     ]
#     )

#     return layout