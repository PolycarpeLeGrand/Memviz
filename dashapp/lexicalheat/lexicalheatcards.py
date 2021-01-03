import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import MiniBatchKMeans
import urllib
import pandas as pd

from tools.factories import text_with_info_tooltip
from dashapp import app, TOPIC_REDUCTIONS_DF, LEXCATS_TEXTS_DF, LEXCATS_ABS_DF, LEXCATS_PARAS_DF
from config import VIZ_DICTS_PATH


lex_topics_formgroup = dbc.FormGroup([
    dbc.Label('Selection des données', className='lead'),
    dbc.Select(
        options=[
            {'label': 'Textes complets', 'value': 'full_texts'},
            {'label': 'Paragraphes', 'value': 'paragraphs'},
            {'label': 'Abstracts', 'value': 'abstracts'},
        ],
        value='full_texts',
        id='lex-topics-data-select',
    ),
    dbc.Label('Selectionn de la visualisation', className='lead pt-4'),
    dbc.RadioItems(
        options=[
            {'label': 'Corrélations entre champs lexicaux', 'value': 'corrs'},
            {'label': 'Occurences moyennes', 'value': 'means'},
            {'label': 'Déviations aux occurences moyennes', 'value': 'norm_means'},
        ],
        value='corrs',
        id='lex-topics-calc-select'
    ),
    dbc.Button(html.A('Télécharger CSV', href='#', id='lexical-csv-download', download='data.csv'), className='mb-2 mt-2'),
    html.Br(),
    dbc.Label('Selectionner les topics', className='lead pt-4'),
    html.Br(),
    dbc.Button('Tout sélectionner', id='lex-topics-show-button', color='success', className='mr-2 mb-2 mt-2'),
    dbc.Button('Tout masquer', id='lex-topics-hide-button', color='primary', className='m-2'),
    dbc.Checklist(
        options=[
            {'label': topic_name, 'value': topic_name} for topic_name in TOPIC_REDUCTIONS_DF['main_topic'].unique()
        ],
        value=TOPIC_REDUCTIONS_DF['main_topic'].unique(),
        id='lex-topics-checklist',
        className='pt-2'
    ),
    html.Div(id='lex-topics-click-log', children='show:0 hide:0 last:0', style={'display': 'none'})
])

lex_heatmap = dcc.Graph(id='lex-heatmap', style={'height': '100vh', 'width': '10vw'}) # 'height': '95vh'



@app.callback(
    [Output('lex-topics-click-log', 'children')],
    [Input('lex-topics-show-button', 'n_clicks'),
     Input('lex-topics-hide-button', 'n_clicks')],
    [State('lex-topics-click-log', 'children'),
     State('lex-topics-checklist', 'value')], prevent_initial_call=True
)
def update_lex_topics(s, h, log, v):
    if not s:
        s = 0
    if not h:
        h = 0
    values = dict([i.split(':') for i in log.split(' ')])
    last = 1 if s > int(values['show']) else 0

    return [f'show:{s} hide:{h} last:{last}']


@app.callback(
    [Output('lex-topics-checklist', 'value')],
    [Input('lex-topics-click-log', 'children')], prevent_initial_call=True
)
def update_lex_topics_2(log):
    values = dict([i.split(':') for i in log.split(' ')])
    r = [TOPIC_REDUCTIONS_DF['main_topic'].unique()] if values['last'] == '1' else [['']]
    return r


@app.callback(
    [Output(component_id='lex-heatmap', component_property='figure'),
     Output(component_id='lex-heatmap', component_property='style'),
     Output(component_id='lexical-csv-download', component_property='href')],
    [Input(component_id='lex-topics-checklist', component_property='value'),
     Input('lex-topics-data-select', 'value'),
     Input('lex-topics-calc-select', 'value')]
)
def update_lexical_heatmap(topics, data, calc):

    # Select data and filter lexcats to only keep docs in topic modeling results
    if data == 'full_texts':
        sub_lexcats = LEXCATS_TEXTS_DF[LEXCATS_TEXTS_DF.index.isin(TOPIC_REDUCTIONS_DF.index)].copy()
    elif data == 'paragraphs':
        # update PARAS to new values when done
        # tdf = LEXCATS_PARAS_DF.set_index(map(lambda x: x.split('_')[0], LEXCATS_PARAS_DF.index))
        # sub_lexcats = tdf[tdf.index.isin(TOPIC_REDUCTIONS_DF.index)].copy()
        sub_lexcats = LEXCATS_PARAS_DF[LEXCATS_PARAS_DF.index.isin(TOPIC_REDUCTIONS_DF.index)].copy()
    else:
        sub_lexcats = LEXCATS_ABS_DF[LEXCATS_ABS_DF.index.isin(TOPIC_REDUCTIONS_DF.index)].copy()

    # Means heatmap
    if calc in ['means', 'norm_means']:
        avg = sub_lexcats.mean()
        rf = pd.DataFrame(avg, columns=['Corpus complet'])
        for topic in topics:
            if topic == '':
                continue
            rf[topic] = sub_lexcats[sub_lexcats.index.isin(TOPIC_REDUCTIONS_DF[(TOPIC_REDUCTIONS_DF['main_topic'] == topic)].index)].mean()
        if calc == 'norm_means':
            rf = rf.divide(avg, axis=0)
        return px.imshow(rf), {'height': '95vh', 'width': f'{int((len(topics)/80)*70+10)}vw'}, \
               "data:text/csv;charset=utf-8," + urllib.parse.quote(rf.to_csv(encoding='utf-8', index=True))

    # Corrs heatmap
    ids = TOPIC_REDUCTIONS_DF[TOPIC_REDUCTIONS_DF['main_topic'].isin(topics)].index
    rf = sub_lexcats.loc[ids].corr().applymap(lambda x: 0 if x == 1 else x)
    return px.imshow(rf), {'height': '95vh', 'width': f'{int((len(sub_lexcats.columns)/80)*90+10)}vw'}, \
           "data:text/csv;charset=utf-8," + urllib.parse.quote(rf.to_csv(encoding='utf-8', index=True))


