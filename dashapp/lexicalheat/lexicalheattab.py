import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from tools.factories import jumbotron_2_columns
from dashapp.lexicalheat.lexicalheatcards import lex_topics_formgroup, lex_heatmap
from dashapp import LEXCATS_MARKDOWN

TAB_ID = 'lexicalheat-tab'

# Jumbotron
title = 'Lexique'
tab_context = 'Analyse du lexique, prototype.'
tab_context_2 = ''

lexicalheat_jumbotron = jumbotron_2_columns(title, tab_context, tab_context_2)


# tab container, which is imported by tabindex
# divided in rows with dbc.Row() and then cols with dbc.Col()
# each col typically holds one card
lexicalheat_tab = dbc.Container([
    dbc.Row([
        dbc.Col([
            lexicalheat_jumbotron,
        ])
    ]),
    dbc.Row([
        # imported cards go here
        dbc.Col(dbc.Form(lex_topics_formgroup), width=2),
        dbc.Col([
            lex_heatmap,
            html.H4('Champs lexicaux:', className='pt-4 pb-2'),
            LEXCATS_MARKDOWN,
        ], width=10),
    ]),
    dbc.Row([]),
], fluid=True, id=TAB_ID)


# callback go below

