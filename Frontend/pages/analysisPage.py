from dash import html, dcc, register_page, dash_table, Input, Output, callback, State
import pandas as pd
import dash
import requests
import dash_bootstrap_components as dbc

# Assume df is a pandas DataFrame with the data from your CSV
df = pd.read_csv("https://raw.githubusercontent.com/HaoEarm/DSA3101_Project/main/Data/predictions.csv")
banks = df['Bank'].unique().tolist()  # Get unique list of banks for the dropdown

register_page(__name__, name='Analysis', top_nav=True, path='/analysisPage')

example_query_button1 = dbc.Button(
    "Example query: Give statistics about the data",
    id="example-prompt-btn1",
    n_clicks=0,
    className="mb-2",
    style={
        'backgroundColor': '#FFB6C1',  # Light pink
        'color': '#495057',  # Dark gray text
        'borderRadius': '15px',  # Rounded corners
        'border': 'none',  # Remove default border
        'width': '70%',  # Maintain the width specification if desired
        'boxShadow': '2px 2px 10px rgba(0,0,0,0.1)'  # Subtle shadow for depth
    }
)

example_query_button2 = dbc.Button(
    "Example query: Generate recommendations for the application",
    id="example-prompt-btn2",
    n_clicks=0,
    className="mb-2",
    style={
        'backgroundColor': '#FFDAB9',  # Peach color
        'color': '#495057',  # Dark gray text
        'borderRadius': '15px',  # Rounded corners
        'border': 'none',  # Remove default border
        'width': '70%',  # Maintain the width specification if desired
        'boxShadow': '2px 2px 10px rgba(0,0,0,0.1)'  # Subtle shadow for depth
    }
)


def layout():
    return html.Div([
        html.H1("Comments Analysis", style={'backgroundColor': '#333', 'color': 'white'}),
        dcc.Dropdown(
            id='bank-filter',
            options=[{'label': bank, 'value': bank} for bank in banks],
            value=banks[0],  # Default value
            clearable=False
        ),
        dbc.Row([
            dbc.Col([
                # This is the column for the DataTable
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
                    page_size=5,  # Specify the number of rows per page
                    style_table={'height': '75vh', 'overflowY': 'auto'},
                    style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white'}
                ),
            ], width=6),  # Using half the width of the row for the DataTable
            dbc.Col([
                # output colomn
                dcc.Loading(id="loading-query", children=[html.Div(
                    id="custom-query-output",
                    style={"overflowY": "scroll", "height": "60vh"}
                )], type="default",
                            style={"display": "none"}),
                html.Div([
                    example_query_button1,
                    example_query_button2,
                    html.Div([dcc.Input(
                        id='custom-query-input',
                        type='text',
                        placeholder='Enter your query about the reviews...',
                        style={'width': '95%'}
                    ), dbc.Button(
                        html.Span(className="fa fa-arrow-right"),
                        id='submit-query-btn',
                        n_clicks=0,
                        className="btn btn-primary",
                        style={'width': '5%', 'padding': '2px 6px'}
                    )]),
                ], style={'flex': '1', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'flex-end',
                          'marginTop': 'auto'}),
            ], width=6),  # Using the other half of the width
        ]),
    ], style={'padding': '20px'})


from dash import html, dcc, Output, Input, State, callback


# Existing imports and setup...

@callback(
    Output('custom-query-output', 'children'),
    Input('submit-query-btn', 'n_clicks'),
    State('custom-query-input', 'value'),
    State('custom-query-output', 'children'),  # Get the current output as state
    prevent_initial_call=True
)
def handle_custom_query(n_clicks, query, current_output):
    if n_clicks > 0 and query:
        response = requests.post('http://localhost:5001/custom_query', json={"query": query})

        # query_display = html.Div([
        #     dbc.Icon(icon="magnifying-glass", style={'marginRight': '5px'}),  # Use the appropriate icon name
        #     html.Strong("You: "),
        #     html.Span(query)
        # ], style={'color': '#000000', 'fontSize': '16px', 'padding': '5px', 'backgroundColor': '#f8f9fa',
        #           'borderRadius': '10px', 'display': 'inline-flex', 'alignItems': 'center'})

        # Display the query as part of the output
        query_display = html.Div([
            html.I(className="fa-solid fa-user"),
            html.Strong(" Query: "),
            html.Span(query)
        ], style={'color': '#007BFF'})  # Styling the query to differentiate it

        if response.status_code == 200:
            result = response.json().get('response', 'No response found.')
            result_display = html.Div([html.P(part) for part in result.split('\n')])

            # Group the query and its result together
            new_entry = html.Div([
                query_display,
                html.Hr(),  # Line to visually separate different entries
                result_display
            ])

            # Append new entry to the existing content
            if current_output:
                current_output.append(new_entry)
                return current_output
            else:
                return [new_entry]
        else:
            error_message = f"Failed to get response. Status code: {response.status_code}"
            error_display = html.Div([
                query_display,
                html.Hr(),
                html.P(error_message)
            ])

            # Handle error by appending error message
            if current_output:
                current_output.append(error_display)
                return current_output
            else:
                return [error_display]
    return "Please enter a query and press submit."


@callback(
    Output('table', 'data'),  # Updates the data of the 'table' component
    [Input('bank-filter', 'value')]  # Listens for changes in the 'bank-filter' dropdown
)
def update_table(selected_bank):
    filtered_df = df[df['Bank'] == selected_bank]
    return filtered_df.to_dict('records')


from dash import callback_context


@callback(
    Output('custom-query-input', 'value'),
    [Input('example-prompt-btn1', 'n_clicks'),
     Input('example-prompt-btn2', 'n_clicks')],
    prevent_initial_call=True
)
def update_input(btn1_clicks, btn2_clicks):
    triggered_id = callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_id == 'example-prompt-btn1':
        return "Give statistics about the data"
    elif triggered_id == 'example-prompt-btn2':
        return "Generate recommendations for the application"
    return dash.no_update
