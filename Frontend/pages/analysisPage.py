import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output
import requests

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
    dcc.Graph(id="histogram"),
    html.Button('Analyze Reviews and generate recommendations',
                id='analyze-btn', n_clicks=0),
    dcc.Loading(id="loading", children=[html.Div(id="analysis-output")], type="default"),
    html.Br(),
    html.Button('Generate statistics of the reviews',
                id='second-btn', n_clicks=0),  # The second button
    dcc.Loading(id="loading2", children=[html.Div(id="second-output")], type="default"),  # Output for the second button
])
####################### CALLBACKS ################################
@callback(Output("histogram", "figure"), [Input("dist_column", "value"), ])
def update_histogram(dist_column):
    return create_distribution(dist_column)

@dash.callback(
    Output("analysis-output", "children"),
    [Input("analyze-btn", "n_clicks")],
    prevent_initial_call = True
)

def on_button_click(n_clicks):
    if n_clicks > 0:
        # This is where you'll call your backend API
        response = requests.get('http://localhost:5001/analyze_reviews')
        if response.status_code == 200:
            analysis_result = response.json().get('analysis', 'No analysis found.')
            # Split the result by new line and create a list of components for Dash to render
            analysis_components = []
            for line in analysis_result.split('\n'):
                analysis_components.append(html.P(line))
                analysis_components.append(html.Br())  # add a line break after each line
            return html.Div([
                html.H5("Analysis Results:"),
                html.Div(analysis_components)  # use the list of components
            ])
        else:
            print(response.text)
            return "Failed to get analysis results."
    return "Click the button to analyze reviews."
@dash.callback(
    Output("second-output", "children"),
    [Input("second-btn", "n_clicks")],
    prevent_initial_call=True
)
def on_second_button_click(n_clicks):
    if n_clicks > 0:
        # Call the `/index statistics` endpoint
        response = requests.get('http://localhost:5001/index_statistics')
        if response.status_code == 200:
            analysis_result = response.json().get('analysis', 'No analysis found.')
            analysis_components = [html.P(line) for line in analysis_result.split('\n')]
            return html.Div([
                html.H5("Index Statistics:"),
                html.Div(analysis_components)
            ])
        else:
            print(response.text)
            return "Failed to get analysis results."
    return "Click the button to get index statistics."