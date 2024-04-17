from dash import html, register_page  #, callback # If you need callbacks, import it here.
import base64

register_page(
    __name__,
    name='Page 6',
    top_nav=True,
    path='/page6'
)


with open('Frontend\o_nps.png', 'rb') as f:
    encoded_image1 = base64.b64encode(f.read()).decode('utf-8')


def layout():
    layout = html.Div([
        html.Br(),
        html.H1("Net Promoter Score", style={'textAlign': 'center'}),
        html.Img(src='data:image/png;base64,{}'.format(encoded_image1), 
                 style={
                'height': '50%',
                'width': '50%',
                'textAlign': 'center'
                })
    ]
    )

    return layout