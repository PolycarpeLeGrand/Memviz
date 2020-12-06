import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from tools.factories import jumbotron_2_columns
from dashapp.topicscatter.topicscattercards import topics_scatter_card


TAB_ID = 'topicscatter-tab'

# Jumbotron
title = 'Topics et clusters'
tab_context = 'Cette page présente, sous forme de nuage de points, la distribution des documents en fonction des topics qui les composent. ' \
              'Les données proviennent d\'un topic modeling de 80 topics réalisé sur les abstracts des documents.  \n' \
              'Les documents peuvent être groupés en clusters à partir de la similarité des topics qui les composent. ' \
              'Chaque cluster est représenté par une couleur (attention, les couleurs peuvent se répéter!)  \n' \
              'Cliquer sur un point pour afficher les détails du document, du topic principal et du cluster sous le graphique.'

tab_context_2 = 'Commandes pour l\'interface:  \n' \
                'Cliquer sur la légende à droite pour masque ou afficher des clusters. Double cliquer pour choisir tous.  \n' \
                '2d: Faire un boite pour zoomer. Double cliquer pour réinitialiser la vue.  \n' \
                '3d: Clic gauche pour pivoter, clic droit pour naviguer, scroll pour zoomer.'

topicscatter_jumbotron = jumbotron_2_columns(title, tab_context, tab_context_2)


# tab container, which is imported by tabindex
# divided in rows with dbc.Row() and then cols with dbc.Col()
# each col typically holds one card
topicscatter_tab = dbc.Container([
    dbc.Row([
        dbc.Col([
            topicscatter_jumbotron,
        ])
    ]),
    dbc.Row([
        # imported cards go here
        dbc.Col(topics_scatter_card),
    ]),
    dbc.Row([]),
], fluid=True, id=TAB_ID)


# callback go below

