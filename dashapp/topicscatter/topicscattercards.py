import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
from sklearn.cluster import MiniBatchKMeans
import pickle

from dashapp import app, DOC_TOPICS_DF, TOPIC_REDUCTIONS_DF, TOPIC_WORDS_DF
from config import VIZ_DICTS_PATH


# Formgroups for the graph options
# Each value has its formgroup, which are then placed in a dbc.Form
title_formgroup = dbc.FormGroup([
    dbc.Label('Ajustements', className='h4')
], className='pb-3 pt-5')

sample_formgroup = dbc.FormGroup([
    dbc.Label('Taille de l\'échantillon', className='h6'),
    dbc.Label(children='X des X documents affichés (X%) ', id='sample-size-label', className='h6'),
    dcc.Slider(min=0.1, max=1.0, step=0.1, value=0.6, id='topics-sample-slider', marks={0.1: '10%', 1: '100%'}),
    dbc.FormText(['Permet d\'afficher un echantillon aléatoire du corpus pour améliorer la performance et la lisibilité']),
    #dbc.Label(id='sample-size-label')
], className='pb-2')

reduc_algo_formgroup = dbc.FormGroup([
    dcc.Markdown('Algorithme de réduction &#x1F6C8', id='reduc-algo-label', className='h6'),
    dbc.Tooltip('Technique de réduction de dimensionnalité appliquée sur les vecteurs doc-topics.', target='reduc-algo-label'),
    dbc.RadioItems(
        options=[
            {'label': 'T-SNE', 'value': 'tsne'},
            {'label': 'UMAP', 'value': 'umap'},
        ],
        value='tsne',
        id='topic-scatter-algo-radio'
    )
], className='pb-2')

n_dims_formgroup = dbc.FormGroup([
    dbc.Label('Nombre de dimensions', className='h6'),
    dbc.RadioItems(
        options=[
            {'label': '2 D', 'value': 2},
            {'label': '3 D', 'value': 3},
        ],
        value=2,
        id='topic-scatter-dims-radio'
    )
], className='pb-2')

# old custom n clusters
'''
clusters_formgroup = dbc.FormGroup([
    dbc.Label('Nombre de clusters (1-300)', className='h6'),
    dbc.Row([
        dbc.Col([dbc.Input(type='number', value=32, min=1, max=300, step=1, id='cluster-number-input')]),
        dbc.Col([dbc.Button('Update', color='success', id='cluster-update-button')]),
    ]),
    dbc.FormText('Entrer le nombre et cliquer sur le bouton pour mettre à jour (peut prendre quelques secondes).'),
], className='pb-2')
'''

clusters_formgroup = dbc.FormGroup([
    dbc.Label('Nombre de clusters (1-300)', className='h6'),
    dbc.Select(id='clusters-select', value='clustering_7',
               options=[{'label': f'{n} Clusters', 'value': f'clustering_{n}'} for n in [5, 7, 10, 15, 20, 25, 40]]),
], className='pb-2')

# Form with the abobove formgroups
scatter_form = dbc.Form([
    title_formgroup,
    reduc_algo_formgroup,
    n_dims_formgroup,
    clusters_formgroup,
    sample_formgroup
])


# Listgroup with the doc details. Updates when a point is clicked on the plot (see callbacks)
doc_details_listgroup = dbc.ListGroup([
    dbc.ListGroupItem([
        dbc.ListGroupItemHeading('Détails du document sélectionné', className='h4'),
        dbc.ListGroupItemText(children='Titre: ', id='doc-details-title', className='h6'),
        dbc.ListGroupItemText(children='Revue: ', id='doc-details-source', className='h6'),
        dbc.ListGroupItemText(children='Id: ', id='doc-details-id', className='h6'),
        dbc.ListGroupItemText(children='Cluster: ', id='doc-details-cluster', className='h6'),
        dbc.Button('Voir l\'abstract', id='doc-details-abstract-button', color='success', className='pt-2 pb-2'),
        dbc.Modal([
            dbc.ModalHeader('', id='abstract-modal-header'),
            dbc.ModalBody('', id='abstract-modal-body'),
            dbc.ModalFooter(dbc.Button('Fermer', id='abstract-modal-close-button', color='success'))
        ], id='abstract-modal', size='lg'),
        dbc.ListGroupItemText(children='Topics principaux', className='h4 pt-2'),
        dcc.Markdown(children='', id='doc-details-topics', className='h6')
    ])
], flush=True)


# Listgroup with topic details for the main topics of the selected doc
topic_details_listgroup = dbc.ListGroup([
    dbc.ListGroupItem([
        dbc.ListGroupItemHeading('Détails du topic principal', className='h4'),
        dbc.ListGroupItemText(children='Nom: ', id='topic-details-name', className='h6'),
        dbc.ListGroupItemText(children='Mots principaux', className='h4'),
        dcc.Markdown(children='', id='topic-details-words', className='h6')
    ])
], flush=True)


# Listgroup with cluster details for selected cluster/doc
cluster_details_listgroup = dbc.ListGroup([
    dbc.ListGroupItem([
        dbc.ListGroupItemHeading('Détails du cluster', className='h4'),
        dbc.ListGroupItemText(children='Cluster: ', id='cluster-details-number', className='h6'),
        dbc.ListGroupItemText(children='Topics principaux', className='h4'),
        dcc.Markdown(children='', id='cluster-details-topics', className='h6')
    ])
], flush=True)


# Card with this tab's content
topics_scatter_card = dbc.Card([
    dbc.CardBody([
        dbc.Row([
            dbc.Col([scatter_form], width=2),
            dbc.Col([dcc.Graph(id='topics-scatter', style={'height': '80vh'}, className='bg-light')]) # , 'backgroundColor': 'ghostwhite'
        ]),
        dbc.Row([
            dbc.Col([doc_details_listgroup], width=3),
            dbc.Col([topic_details_listgroup], width=3),
            dbc.Col([cluster_details_listgroup]),
        ])
    ])
])


# Callbacks
@app.callback(
    [Output(component_id='topics-scatter', component_property='figure'),
     Output(component_id='sample-size-label', component_property='children')],
    [Input(component_id='topics-sample-slider', component_property='value'),
     Input(component_id='topic-scatter-algo-radio', component_property='value'),
     Input(component_id='topic-scatter-dims-radio', component_property='value'),
     Input(component_id='clusters-select', component_property='value')]
     #Input(component_id='cluster-update-button', component_property='n_clicks')],
    #[State(component_id='cluster-number-input', component_property='value')] # add saved data to state and check if == num clusters before update?
)
def update_topics_scatter(slider_value, reducer_algo, n_dims, cluster_col): #clusters_activated, n_clusters):
    """Builds the scatter from the inputs. Can be 2d or 3d, with umap or tsne reductions and N clusters"""

    # Make new df from base info. We use .loc instead of [[]] because it copies or something.
    tdf = TOPIC_REDUCTIONS_DF.loc[:, ('title', 'source', 'main_topic')]
    total_size = len(tdf.index)

    # Add coords according to reduction algo and n_dims
    reducer_prefix = 'tsne_' if reducer_algo == 'tsne' else 'umap_'
    if n_dims == 2:
        tdf[['x', 'y']] = TOPIC_REDUCTIONS_DF[[f'{reducer_prefix}2d_x', f'{reducer_prefix}2d_y']]
    else:
        tdf[['x', 'y', 'z']] = TOPIC_REDUCTIONS_DF[[f'{reducer_prefix}3d_x', f'{reducer_prefix}3d_y', f'{reducer_prefix}3d_z']]

    # Calc clusters and add col, old
    # tdf['cluster'] = MiniBatchKMeans(n_clusters=n_clusters, random_state=2112).fit_predict(DOC_TOPICS_DF)
    tdf['cluster'] = TOPIC_REDUCTIONS_DF[cluster_col]

    # Take a sample
    tdf = tdf.sample(int(slider_value*len(TOPIC_REDUCTIONS_DF)))

    sample_size = len(tdf.index)
    sample_size_label_value = f'{sample_size} des {total_size} documents affichés ({int(slider_value*100)}%).'

    # Make fig. Scatter or scatter_3d depending on n_dims
    if n_dims == 2:
        fig = px.scatter(tdf, x='x', y='y', title='Scatterplot documents-topics',
                         color='cluster', hover_name=tdf.index,
                         hover_data={'cluster': True,
                                     'main_topic': True,
                                     'Titre': tdf['title'].map(lambda x: x if len(x) < 60 else x[:60] + '...'),
                                     'Revue': tdf['source'],
                                     'x': False,
                                     'y': False},
                         color_discrete_sequence=px.colors.qualitative.Dark24, )

    else:
        fig = px.scatter_3d(tdf, x='x', y='y', z='z', title='Scatterplot documents-topics',
                            color='cluster', hover_name=tdf.index,
                            hover_data={'cluster': True,
                                        'main_topic': True,
                                        'Titre': tdf['title'],
                                        'Revue': tdf['source'],
                                        'x': False,
                                        'y': False,
                                        'z': False},
                            color_discrete_sequence=px.colors.qualitative.Dark24, )

    fig.update_traces(marker={'size': 3}) # hovertemplate=hover_template, woudl be cleaner with hovertemplate but it's a bit of work
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    return fig, sample_size_label_value


@app.callback(
    [Output(component_id='doc-details-title', component_property='children'),
     Output(component_id='doc-details-source', component_property='children'),
     Output(component_id='doc-details-cluster', component_property='children'),
     Output(component_id='doc-details-id', component_property='children'),
     Output(component_id='doc-details-topics', component_property='children')],
    [Input(component_id='topics-scatter', component_property='clickData')], prevent_initial_call=True
)
def update_doc_details_topics(data):
    """Updates various elements of doc_details_listgroup when a point is clicked on the graph"""

    # Number of topics to show in doc top topics list
    n_top_topics = 10
    cluster = data['points'][0]['customdata'][0]
    doc_id = data['points'][0]['hovertext']
    title, source = TOPIC_REDUCTIONS_DF.loc[doc_id][['title', 'source']]
    top_topics = DOC_TOPICS_DF.loc[doc_id].nlargest(n_top_topics)
    top_topics = f'  \n'.join(f'{top} - {weight:.4f}' for top, weight in top_topics.items())
    return f'Titre: {title}', f'Revue: {source}', f'Cluster: {cluster}', f'Id: {doc_id}', top_topics


@app.callback(
    [Output(component_id='topic-details-name', component_property='children'),
     Output(component_id='topic-details-words', component_property='children')],
    [Input(component_id='topics-scatter', component_property='clickData')], prevent_initial_call=True
)
def update_doc_details_topics(data):
    """Updates topic_details_listgroup to show top words of main topic of clicked doc"""

    # Number of word to show in top words list
    n_top_words = 15
    doc_id = data['points'][0]['hovertext']
    topic_name = TOPIC_REDUCTIONS_DF.loc[doc_id]['main_topic']
    top_words = TOPIC_WORDS_DF.loc[topic_name].nlargest(n_top_words)
    top_words = f'  \n'.join(f'{word} - {weight:.4f}' for word, weight in top_words.items())
    return f'Nom: {topic_name}', top_words


@app.callback(
    [Output(component_id='cluster-details-number', component_property='children'),
     Output(component_id='cluster-details-topics', component_property='children')],
    [Input(component_id='topics-scatter', component_property='clickData')],
    [State(component_id='clusters-select', component_property='value')], prevent_initial_call=True
)
def update_doc_details_cluster(data, cluster_col):
    """Updates cluster_details_listgroup to show top topics of selected cluster"""

    # Number of word to show in top words list
    n_top_topics = 15
    cluster = data['points'][0]['customdata'][0]

    #cluster_list = MiniBatchKMeans(n_clusters=32, random_state=2112).fit_predict(DOC_TOPICS_DF)
    #tdf = DOC_TOPICS_DF.copy()
    #tdf['cluster'] = cluster_list
    #tdf = tdf[(tdf['cluster'] == int(cluster))]
    #tdf = tdf.drop('cluster', axis=1)

    # tdf = DOC_TOPICS_DF.loc[[doc_id for doc_id, c in cluster_dict.items() if c == cluster]]
    tdf = DOC_TOPICS_DF.loc[TOPIC_REDUCTIONS_DF[(TOPIC_REDUCTIONS_DF[cluster_col] == cluster)].index]
    # print(TOPIC_REDUCTIONS_DF[(TOPIC_REDUCTIONS_DF[cluster_col] == cluster)])

    top_topics = tdf.mean().nlargest(n_top_topics)
    top_topics = f'  \n'.join(f'{topic} - {avg:.4f}' for topic, avg in top_topics.items())
    return f'Cluster: {cluster}', top_topics


@app.callback(
    [Output('abstract-modal-header', 'children'),
     Output('abstract-modal-body', 'children'),
     Output('abstract-modal', 'is_open')],
    [Input('doc-details-abstract-button', 'n_clicks'),
     Input('abstract-modal-close-button', 'n_clicks')],
    [State('abstract-modal', 'is_open'),
     State('abstract-modal-header', 'children'),
     State('abstract-modal-body', 'children'),
     State('doc-details-id', 'children')]
)
def show_abstract_modal(open_click_count, close_click_count, modal_is_opened, current_title, current_abstract, doc_id):
    if not open_click_count and not close_click_count:
        raise PreventUpdate

    doc_id = doc_id[4:]
    if modal_is_opened or doc_id == '':
        return current_title, current_abstract, False

    else:
        d = pickle.load(open(VIZ_DICTS_PATH / f'{doc_id}.p', 'rb'))
        return d['title'], dcc.Markdown('  \n'.join(para for para in d['abstract_paras'])), True


