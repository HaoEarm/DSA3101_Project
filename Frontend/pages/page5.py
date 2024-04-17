from dash import html, register_page  #, callback # If you need callbacks, import it here.
import base64

register_page(
    __name__,
    name='Page 5',
    top_nav=True,
    path='/page5'
)


with open('Frontend\other_bank_promoter_cloud.png', 'rb') as f:
    encoded_image1 = base64.b64encode(f.read()).decode('utf-8')

with open('Frontend\other_bank_detractor_cloud.png', 'rb') as f2:
    encoded_image2 = base64.b64encode(f2.read()).decode('utf-8')


def layout():
    layout = html.Div([
        html.Br(),
        html.H1("Commonly used words in positive reviews - Other Banks", style={'textAlign': 'center'}),
        html.Img(src='data:image/png;base64,{}'.format(encoded_image1), 
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
        html.Img(src='data:image/png;base64,{}'.format(encoded_image2), 
                 style={
                'height': '50%',
                'width': '50%',
                'textAlign': 'center'
                })
    ]
    )
    return layout, layout2