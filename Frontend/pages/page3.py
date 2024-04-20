import dash
from dash import html, register_page
from dash import dcc
import dash_bootstrap_components as dbc
import base64
import requests


register_page(
    __name__,
    name='Page 3',
    top_nav=True,
    path='/page3'
)

# Download and save the images
def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
    else:
        print(f'Failed to download image from {url}')

# URLs for the images
url1 = 'https://raw.githubusercontent.com/HaoEarm/DSA3101_Project/main/Frontend/gxs_promoter_cloud.png'
url2 = 'https://raw.githubusercontent.com/HaoEarm/DSA3101_Project/main/Frontend/gxs_detractor_cloud.png'
url3 = 'https://raw.githubusercontent.com/HaoEarm/DSA3101_Project/main/Frontend/other_bank_promoter_cloud.png'
url4  = 'https://raw.githubusercontent.com/HaoEarm/DSA3101_Project/main/Frontend/other_bank_detractor_cloud.png'


# Download images
download_image(url1, 'gxs_promoter_cloud.png')
download_image(url2, 'gxs_detractor_cloud.png')
download_image(url3, 'other_bank_promoter_cloud.png')
download_image(url4, 'other_bank_detractor_cloud.png')

def layout():
    # Encode image to base64
    def encode_image(image_file):
        with open(image_file, 'rb') as file:
            encoded = base64.b64encode(file.read()).decode('ascii')
        return f"data:image/png;base64,{encoded}"

    # # Layouts
    # layout = html.Div([
    #     html.Br(),
    #     html.H1("GXS Bank", style={'textAlign': 'center'}),
    #     html.Img(src=encode_image('gxs_promoter_cloud.png'), style={'height': '50%', 'width': '50%', 'textAlign': 'center'})
    # ])

    # layout2 = html.Div([
    #     html.Br(),
    #     html.Br(),
    #     html.H1("Commonly used words in negative reviews - GXS Bank", style={'textAlign': 'center'}),
    #     html.Img(src=encode_image('gxs_detractor_cloud.png'), style={'height': '50%', 'width': '50%', 'textAlign': 'center'})
    # ])

    # layout3 = html.Div([
    #     html.Br(),
    #     html.Br(),
    #     html.H1("Commonly used words in negative reviews - GXS Bank", style={'textAlign': 'center'}),
    #     html.Img(src=encode_image('gxs_detractor_cloud.png'), style={'height': '50%', 'width': '50%', 'textAlign': 'center'})
    # ])


    layout = html.Div([
        html.Br(),
        html.H1(["Commonly Used Words in Reviews"], style={'backgroundColor': '#333', 'color': 'white'}),
        html.Br(),
        dbc.Row([
            html.H1(["GXS Bank"], style={'textAlign': 'center'}),
            dbc.Col([
                html.Img(src=encode_image('gxs_promoter_cloud.png'), style={'height': '100%', 'width': '90%'}, className = 'center')
            ]),
            dbc.Col([
                html.Img(src=encode_image('gxs_detractor_cloud.png'), style={'height': '100%', 'width': '90%'}, className = 'center')
            ])
        ]
        )
    ])
    layout2 = html.Div([
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.H1(["Other Banks"], style={'textAlign': 'center'}),
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.Img(src=encode_image('other_bank_promoter_cloud.png'), style={'height': '100%', 'width': '90%'}, className = 'center')
            ]),
            dbc.Col([
                html.Img(src=encode_image('other_bank_detractor_cloud.png'), style={'height': '100%', 'width': '90%'}, className = 'center')
            ])
        ]
        )
    ])

    return layout, layout2