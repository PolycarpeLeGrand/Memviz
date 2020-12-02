import dash_bootstrap_components as dbc

from config import HEADER_TITLE, HEADER_SUBTITLE


header = dbc.Navbar([
    dbc.Row([
        dbc.Col([
            dbc.NavbarBrand(HEADER_TITLE, className='ml-2', style={'font-size': '200%'}),
            # html.Hr(),
            dbc.NavbarBrand(HEADER_SUBTITLE, className='ml-2', style={'font-size': '100%'}),
        ]),
    ])
], color='primary', dark=True)

