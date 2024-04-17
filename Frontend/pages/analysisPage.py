# import pandas as pd
# import dash
# from dash import dcc, html, callback
# import plotly.express as px
# from dash.dependencies import Input, Output
# import requests

# dash.register_page(__name__, path='/analysis', name="Analysis 📊")

# ####################### LOAD DATASET #############################
# df = pd.read_csv("output.csv")

# ####################### HISTOGRAM ###############################
# def create_distribution(col_name="Revolut"):
#     return px.histogram(data_frame=df, x="Sentiment", height=600)

# ####################### WIDGETS ################################
# columns = ["Revolut"]
# dd = dcc.Dropdown(id="dist_column", options=columns, value="Revolut", clearable=False)

# ####################### PAGE LAYOUT #############################
# layout = html.Div(children=[
#     html.Br(),
#     html.P("Select Column:"),
#     dd,
#     dcc.Graph(id="histogram"),
#     html.Button('Analyze Reviews and generate recommendations',
#                 id='analyze-btn', n_clicks=0),
#     dcc.Loading(id="loading", children=[html.Div(id="analysis-output")], type="default"),
#     html.Br(),
#     html.Button('Generate statistics of the reviews',
#                 id='second-btn', n_clicks=0),  # The second button
#     dcc.Loading(id="loading2", children=[html.Div(id="second-output")], type="default"),  # Output for the second button
# # ])
# # ####################### CALLBACKS ################################
# # @callback(Output("histogram", "figure"), [Input("dist_column", "value"), ])
# # def update_histogram(dist_column):
# #     return create_distribution(dist_column)

# # @dash.callback(
# #     Output("analysis-output", "children"),
# #     [Input("analyze-btn", "n_clicks")],
# #     prevent_initial_call = True
# # )

# def on_button_click(n_clicks):
#     if n_clicks > 0:
#         # This is where you'll call your backend API
#         response = requests.get('http://localhost:5001/analyze_reviews')
#         if response.status_code == 200:
#             analysis_result = response.json().get('analysis', 'No analysis found.')
#             # Split the result by new line and create a list of components for Dash to render
#             analysis_components = []
#             for line in analysis_result.split('\n'):
#                 analysis_components.append(html.P(line))
#                 analysis_components.append(html.Br())  # add a line break after each line
#             return html.Div([
#                 html.H5("Analysis Results:"),
#                 html.Div(analysis_components)  # use the list of components
#             ])
#         else:
#             print(response.text)
#             return "Failed to get analysis results."
#     return "Click the button to analyze reviews."
# @dash.callback(
#     Output("second-output", "children"),
#     [Input("second-btn", "n_clicks")],
#     prevent_initial_call=True
# )
# def on_second_button_click(n_clicks):
#     if n_clicks > 0:
#         # Call the `/index statistics` endpoint
#         response = requests.get('http://localhost:5001/index_statistics')
#         if response.status_code == 200:
#             analysis_result = response.json().get('analysis', 'No analysis found.')
#             analysis_components = [html.P(line) for line in analysis_result.split('\n')]
#             return html.Div([
#                 html.H5("Index Statistics:"),
#                 html.Div(analysis_components)
#             ])
#         else:
#             print(response.text)
#             return "Failed to get analysis results."
#     return "Click the button to get index statistics."


from dash import html, dcc, register_page, dash_table, Input, Output, callback
import pandas as pd
import dash
import requests

# Assume df is a pandas DataFrame with the data from your CSV
df = pd.read_csv("https://raw.githubusercontent.com/HaoEarm/DSA3101_Project/main/Data/predictions.csv")
banks = df['Bank'].unique().tolist()  # Get unique list of banks for the dropdown

register_page(__name__, name='Analysis', top_nav=True, path='/analysisPage')

def layout():
    return html.Div([
        html.H1("Comments Analysis", style={'backgroundColor': '#333', 'color': 'white'}),
        dcc.Dropdown(
            id='bank-filter',
            options=[{'label': bank, 'value': bank} for bank in banks],
            value=banks[0],  # Default value
            clearable=False
        ),
        dash_table.DataTable(
            id='table',
            columns=[
                {'name': 'Customer ID', 'id': 'UserName'},
                {'name': 'Comments', 'id': 'Review'},
                {'name': 'Score', 'id': 'Score'},
                {'name': 'Date', 'id': 'Date'},
                {'name': 'Bank', 'id': 'Bank'}
            ],
            data=df.to_dict('records'),
            style_cell={'textAlign': 'left', 'padding': '5px'},
            style_cell_conditional=[
                {'if': {'column_id': 'Review'}, 'width': '800px'},
                {'if': {'column_id': 'UserName'}, 'width': '200px'},
                {'if': {'column_id': 'Score'}, 'width': '100px'},
                {'if': {'column_id': 'Date'}, 'width': '150px'},
                {'if': {'column_id': 'Bank'}, 'width': '150px'}
            ],
            style_data={'whiteSpace': 'normal', 'height': 'auto'},
            page_size=10,  # Specify the number of rows per page
            style_table={'height': '600px', 'overflowY': 'auto'},
            style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white'}
        ),
        html.Button('Analyze Reviews and generate recommendations',
                    id='analyze-btn', n_clicks=0),
        dcc.Loading(id="loading", children=[html.Div(id="analysis-output")], type="default"),
        html.Br(),
        html.Button('Generate statistics of the reviews',
                    id='second-btn', n_clicks=0),
        dcc.Loading(id="loading2", children=[html.Div(id="second-output")], type="default"),
    ], style={'padding': '20px'})

# Callback for the Analyze Reviews button
@callback(
    Output("analysis-output", "children"),
    [Input("analyze-btn", "n_clicks")],
    prevent_initial_call=True
)
def on_analyze_button_click(n_clicks):
    if n_clicks > 0:
        response = requests.get('http://localhost:5001/analyze_reviews')
        if response.status_code == 200:
            analysis_result = response.json().get('analysis', 'No analysis found.')
            return html.Div([html.P(part) for part in analysis_result.split('\n')])
        else:
            return f"Failed to get analysis results. Status code: {response.status_code}"

# Callback for the Generate statistics button
@callback(
    Output("second-output", "children"),
    [Input("second-btn", "n_clicks")],
    prevent_initial_call=True
)
def on_statistics_button_click(n_clicks):
    if n_clicks > 0:
        response = requests.get('http://localhost:5001/index_statistics')
        if response.status_code == 200:
            statistics_result = response.json().get('analysis', 'No statistics found.')
            return html.Div([html.P(part) for part in statistics_result.split('\n')])
        else:
            return f"Failed to get statistics results. Status code: {response.status_code}"

# Callback to update table based on bank selection
@callback(
    Output('table', 'data'),
    [Input('bank-filter', 'value')]
)
def update_table(selected_bank):
    filtered_df = df[df['Bank'] == selected_bank]
    return filtered_df.to_dict('records')