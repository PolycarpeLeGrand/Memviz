import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

from dashapp import app, METADATA_DF


# Card with wordcount graph and control panel. Total width = 8
word_counts_card = dbc.Card([
    dbc.CardHeader('Répartition des documents selon la taille des textes ou des abstracts', className='lead'),
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.H4('', className="card-title pb-5"),
                html.P('Le graphique à la droite montre la répartition des documents du corpus en fonction du nombre de mots. '
                        'Le menu permet de choisir entre les textes et les abstracts. ', className='card-text pt-5'),
                dbc.Select(id='bags-select', value='texts',
                           options=[{'label': 'Textes (tranches de 500)', 'value': 'texts'},
                                    {'label': 'Abstracts (tranches de 50)', 'value': 'abstracts'}]),
                dbc.FormGroup([
                    dbc.Checklist(
                        options=[{'label': 'Séparer les types de documents', 'value': 1}],
                        value=[],
                        switch=True,
                        id='bags-select-2'
                    ),
                    dbc.FormText('Sous-divise chaque intervale selon les catégories doctypes.')
                    # dbc.Checkbox(id='bags-select-2'),
                    # dbc.Label(' Séparer les categories doctypes', html_for='bags-select-2')
                ], className='pt-2', inline=True),
            ], width=3),

            dbc.Col([
                dcc.Graph(
                    id='token_counts_fig', style={'width': '180%'}
                )
            ], width=5)
        ])
    ])
])


# Callbacks

@app.callback(
    Output('token_counts_fig', 'figure'),
    [Input('bags-select', 'value'), Input('bags-select-2', 'value')])
def update_bags_fig(selected_part, split_doctypes):
    params = {'texts':
                  {'df_col': 'text_tokens',
                   'bag_size': 500,
                   'title': 'Taille des textes'},
              'abstracts':
                  {'df_col': 'abs_tokens',
                   'bag_size': 50,
                   'title': 'Taille des abstracts'}
              }
    col = params[selected_part]['df_col']
    size = params[selected_part]['bag_size']
    split_doctypes = 1 in split_doctypes

    tdf = METADATA_DF.loc[:, (col, 'doctype_cat')]
    tdf[col] = tdf[col].map(lambda x: x if x < 11*size else 11*size-2)
    tdf['bins'] = pd.cut(tdf[col], [i*size - 1 for i in range(12)], labels=[f'{i*size}-{i*size+499}' if i*size < 10*size else f'{i*size}+' for i in range(11)])
    groups = ['bins', 'doctype_cat'] if split_doctypes else ['bins']
    tdf = tdf.groupby(groups).size().reset_index(name='counts')
    return px.bar(tdf, x='bins', y='counts', text='counts', color='doctype_cat' if split_doctypes else None,
                  title=params[selected_part]['title'],
                  labels={
                      'bins': 'Nombre de mots (tokens)',
                      'counts': 'Nombre de documents',
                  },
                  )

