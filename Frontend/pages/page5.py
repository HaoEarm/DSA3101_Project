from dash import html, register_page  #, callback # If you need callbacks, import it here.
import base64
import requests

register_page(
    __name__,
    name='Page 5',
    top_nav=True,
    path='/page5'
)

def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
    else:
        print(f'Failed to download image from {url}')

# URLs for the images
url1 = 'https://raw.githubusercontent.com/HaoEarm/DSA3101_Project/main/Frontend/other_bank_promoter_cloud.png'
url2 = 'https://raw.githubusercontent.com/HaoEarm/DSA3101_Project/main/Frontend/other_bank_detractor_cloud.png'

# Download images
download_image(url1, 'other_bank_promoter_cloud.png')
download_image(url2, 'other_bank_detractor_cloud.png')


def layout():
    def encode_image(image_file):
        with open(image_file, 'rb') as file:
            encoded = base64.b64encode(file.read()).decode('ascii')
        return f"data:image/png;base64,{encoded}"

    layout = html.Div([
        html.Br(),
        html.H1("Commonly used words in positive reviews - Other Banks", style={'textAlign': 'center'}),
        html.Img(src= encode_image("other_bank_promoter_cloud.png"),
                 style={
                'height': '50%',
                'width': '50%',
                'textAlign': 'center'
                })
    ]
    )

    layout2 = html.Div([
        html.Br(),
        html.Br(),
        html.H1("Commonly used words in negative reviews - Other Banks", style={'textAlign': 'center'}),
        html.Img(src=encode_image("other_bank_detractor_cloud.png"),
                 style={
                'height': '50%',
                'width': '50%',
                'textAlign': 'center'
                })
    ]
    )
    return layout, layout2