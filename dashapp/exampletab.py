"""This is an example tab layout

the content goes in a dbc.container (or html.div) component and is imported by tabindex
"""

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from tools.factories import jumbotron_from_title_paragraphs


TAB_ID = 'example-tab'


# Jumbotron can be made from a markdown string (not used in this example)
md = '### Title  \nThis is the first line of text. And it goes on  \non another line.  \n  \nThen some more 2 lines down.'
ex_jumbotron_md = dbc.Jumbotron([
    dcc.Markdown(md, className='lead')
], className='pt-2 pb-2')

# Or from a factory
title = 'Title to show on the jumbotron'
paras = ['This is the first paragraph shown on the jumbotron.',
         'And this one is the second paragraph.',
         'We can even add a third one if we\'re feeling wild!']
ex_jumbotron = jumbotron_from_title_paragraphs(title, paras, className='pt-2 pb-2')


# Most content will be held in cars, that can be defined here or imported
card_md = '#### Big card text  \nFollowed by smaller card text, which is all in a markdown component.'
ex_card_1 = dbc.Card([
    dbc.CardHeader('First card header and stuff', className='lead'),
    dbc.CardBody([
        dcc.Markdown(card_md)
    ])
])

ex_card_2 = dbc.Card([
    dbc.CardHeader('Second card', className='lead'),
    dbc.CardBody([
        dbc.Row([
            dbc.Col(html.P('Text in top left')),
            dbc.Col(html.P('Text in top right'))
        ]),
        dbc.Row([
            dbc.Col(html.P('Text in bot left')),
            dbc.Col(html.P('Text in bot right'))
        ]),
    ])
])


card_no_head = dbc.Card([dbc.CardBody([html.P(['Card with no head', html.Br(), 'And a little text, small and centered'])])])

# tab container, which is imported by tabindex
# divided in rows with dbc.Row() and then cols with dbc.Col()
# each col typically holds one card
example_tab = dbc.Container([
    dbc.Row([
        dbc.Col([
            ex_jumbotron,
        ])
    ]),

    dbc.Row([
        dbc.Col([
            ex_card_1
        ], width=3),
        dbc.Col([
            ex_card_2
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            card_no_head
        ], width=3),
    ], justify='center'),
], fluid=True, id='example-tab')


# callback go below
