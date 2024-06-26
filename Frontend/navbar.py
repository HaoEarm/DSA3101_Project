from dash import html
import dash_bootstrap_components as dbc


def create_navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(
                dbc.NavLink(
                    [
                        html.I(className="fa-brands fa-github"),  # Font Awesome Icon
                        " "  # Text beside icon
                    ],
                    href="https://github.com/HaoEarm/DSA3101_Project/tree/main",
                    target="_blank"
                )

            ),
            # dbc.NavItem(
            #     dbc.NavLink(
            #         [
            #             html.I(className="fa-brands fa-medium"),  # Font Awesome Icon
            #             " "  # Text beside icon
            #         ],
            #         href="[YOUR MEDIUM PROFILE URL]",
            #         target="_blank"
            #     )

            # ),
            # dbc.NavItem(
            #     dbc.NavLink(
            #         [
            #             html.I(className="fa-brands fa-linkedin"),  # Font Awesome Icon
            #             " "  # Text beside icon
            #         ],
            #         href="[YOUR LINKEDIN PROFILE URL]",
            #         target="_blank"
            #     )

            # ),
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="Menu",
                align_end=True,
                children=[  # Add as many menu items as you need
                    dbc.DropdownMenuItem("Home", href='/'),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Sentiment Breakdown", href='/page2'),
                    dbc.DropdownMenuItem("Wordclouds", href='/page3'),
                    dbc.DropdownMenuItem("NPS", href='/page4'),
                    dbc.DropdownMenuItem("Comments", href='/analysisPage'),
                ],
            ),
        ],
        brand='Home',
        brand_href="/",
        # sticky="top",  # Uncomment if you want the navbar to always appear at the top on scroll.
        color="dark",  # Change this to change color of the navbar e.g. "primary", "secondary" etc.
        dark=True,  # Change this to change color of text within the navbar (False for dark text)
    )

    return navbar