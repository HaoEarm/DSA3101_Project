# import dash
# from dash import html

# dash.register_page(__name__, path='/test', name="Testing :)")


# layout = html.Div(children=[
#     html.Div(children=[
#         html.H2("Hi"),
#         "testing",
#         html.Br(),html.Br(),
#         "testing2",
#         html.Br(), html.Br(),
#         "testing3"])
#     ])





from dash import html, register_page  #, callback # If you need callbacks, import it here.

register_page(
    __name__,
    name='Page 3',
    top_nav=True,
    path='/page3'
)


def layout():
    layout = html.Div([
        html.H1(
            [
                "Page 3"
            ]
        )
    ])
    return layout