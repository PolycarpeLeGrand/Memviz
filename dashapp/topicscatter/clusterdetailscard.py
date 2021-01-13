import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dashapp import app, TOPIC_REDUCTIONS_DF, DOC_TOPICS_DF

# cluster_details_carddeck = dbc.CardColumns(children=[], id='cluster-details-carddeck')
cluster_details_carddeck = dbc.Row(children=[], id='cluster-details-carddeck')

# Card with this tab's content
cluster_details_card = dbc.Card([
    dbc.CardBody(
        dbc.Row([
            dbc.Col([cluster_details_carddeck])
        ])
    )
])



# callbacks!

# Uses sdas from topicsscattercards as input!
@app.callback(
    [Output('cluster-details-carddeck', 'children')],
    [Input('clusters-select', 'value')]
)
def update_cluster_details(cluster_col):
    """Updates cluster details with a row of cluster cards"""

    def make_cluster_details_card(cluster_col, cluster_name):
        tdf = DOC_TOPICS_DF.loc[TOPIC_REDUCTIONS_DF[(TOPIC_REDUCTIONS_DF[cluster_col] == cluster_name)].index]
        top_topics = tdf.mean().nlargest(10)
        return dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    dcc.Markdown(
                        f'{cluster_name}  \nNombre de docs: {TOPIC_REDUCTIONS_DF[cluster_col].value_counts()[cluster_name]}'
                    ), className='lead'),
                dbc.CardBody(
                    dcc.Markdown(
                        f'  \n'.join(f'{topic} - {avg:.4f}' for topic, avg in top_topics.items())
                    )
                )
            ])
        ], width=3, className='pb-3')
    return [[make_cluster_details_card(cluster_col, f'Cluster {num_cluster}') for num_cluster in range(int(cluster_col.split('_')[1]))]]

