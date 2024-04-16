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




from dash import html, register_page  #, callback # If you need callbacks, import it here.

register_page(
    __name__,
    name='Home',
    top_nav=True,
    path='/'
)


def layout():
    layout = html.Div([
        html.H1(
            [
                "Home Page"
            ]
        )
    ])
    return layout