import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px

from dashapp import app, METADATA_DF

MAX_TABLE_ROWS = 15


meta_table_card = dbc.Card([
    dbc.CardHeader(f'Taille des documents et Metadonnnées ({MAX_TABLE_ROWS} plus fréquentes)', className='lead', id='meta-table-head'),
    dbc.Tooltip('Le tebleau montre les valeurs les plue fréquentes pour chaque métadonnée. Possibilité de filtrer les documents en fonction du nombre de mots.', target='meta-table-head'),
    dbc.CardBody([
        # html.Br(),
        dbc.Row([
           # dbc.Col([
            #    html.P('Choisir la metadonnee:', className='pt-3', style={'text-align': 'right'})
            #]),
            dbc.Col([
                dbc.InputGroup([
                    dbc.InputGroupAddon('Choisir la metadonnee', addon_type='prepend'),
                    dbc.Select(id='metadata-table-select', value='source',
                               options=[{'label': 'Revues', 'value': 'source'},
                                        {'label': 'Doctypes', 'value': 'doctype'},
                                        {'label': 'Categories Doctypes', 'value': 'doctype_cat'},
                                        {'label': 'Annees de Publication', 'value': 'year'}]
                    ),

                ]),
            ])
        ], justify='center', align='center'),
        html.Br(),
        dcc.RangeSlider(id='metadata-slider', min=0, max=5000, step=500, value=[0, 5000],
                        marks={i*500: {'label': str(i*500) if i < 10 else '5000+'} for i in range(11)}),
        html.P(id='metadata-slider-para', style={'text-align': 'center'}),
        html.Div(id='metadata-table'),
    ])
])


# Callbacks

@app.callback(
    [Output(component_id='metadata-table', component_property='children'),
     Output(component_id='metadata-slider-para', component_property='children')],
    [Input(component_id='metadata-table-select', component_property='value'),
     Input(component_id='metadata-slider', component_property='value')],
    [State(component_id='metadata-table-select', component_property='options')]
)
def update_metadata_table(value, slider_values, options):
    label = next(filter(lambda x: x['value'] == value, options))['label']
    min_tokens = slider_values[0]
    max_tokens = slider_values[1] if slider_values[1] < 5000 else 1000000
    tdf = METADATA_DF[(METADATA_DF['text_tokens'] >= min_tokens) & (METADATA_DF['text_tokens'] <= max_tokens)]
    n = len(tdf)
    tdf = tdf[value].value_counts().head(MAX_TABLE_ROWS)
    t = html.Table([
        html.Thead(
            html.Tr([html.Th(label), html.Th('Documents'), html.Th('Pct')])
        ),
        html.Tbody([
            html.Tr([
                html.Td(i), html.Td(v), html.Td(f'{v/n*100:.2f}%')
            ]) for i, v in tdf.items()
        ])
    ], style={'width': '100%'})
    text = ['Ajuster le slider pour filtrer par nombre de tokens.', html.Br(),
            f'Min tokens: {min_tokens} | Max tokens: {max_tokens if max_tokens < 10000 else "5000+"} | Total docs: {n}']
    return t, text

