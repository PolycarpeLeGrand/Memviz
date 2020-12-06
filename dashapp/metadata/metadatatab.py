"""This contains the layout for the Metadata tab. Cards are imported"""

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from tools.factories import jumbotron_2_columns
from dashapp.metadata.wordcountscard import word_counts_card
from dashapp.metadata.metatablecard import meta_table_card


TAB_ID = 'metadata-tab'

# Jumbotron
title = 'Métadonnées'
tab_context = 'Cette page présente un aperçu du corpus à partir des différentes métadonnées disponibles. ' \
              'Les éléments sont interactifs et les options peuvent être ajustées.'

metadata_jumbotron = jumbotron_2_columns(title, tab_context)



# tab container, which is imported by tabindex
# divided in rows with dbc.Row() and then cols with dbc.Col()
# each col typically holds one card
metadata_tab = dbc.Container([
    dbc.Row([
        dbc.Col([
            metadata_jumbotron,
        ])
    ]),
    dbc.Row([
        # imported cards go here
        dbc.Col([word_counts_card], width=8),
        dbc.Col([meta_table_card], width=4),
    ]),
], fluid=True, id=TAB_ID)


# callback go below
