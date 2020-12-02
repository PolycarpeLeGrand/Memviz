import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from dashapp import app, DATA
from dashapp.header import header
from dashapp.exampletab import example_tab
from dashapp.abouttab import about_tab


# Declare tabs following this format, 1 dist per tab
# Can then filter to get info from input, see below
# Replace search_key, search_value and target_key accordingly
# next(filter(lambda x: x['search_key'] == 'search_value', TABS))['target_key']
TABS = [
    {'name': 'tab-0', 'url': '/extab', 'label': 'Example Tab', 'container': example_tab},
    {'name': 'tab-1', 'url': '/about', 'label': 'About', 'container': about_tab},
]


tabs = dbc.Tabs(
    [dbc.Tab(label=tab['label'], label_style={'cursor': 'pointer'}) for tab in TABS],
    id='tabs', active_tab='tab-0', style={'padding-left': '10px', }
)


layout = html.Div([
    dcc.Location(id='url', refresh=False),
    header,
    html.Div([
        tabs,
    ], className='pt-2 bg-dark text-light'),
    dbc.Container([], id='tab-container', fluid=True, className='bt-2 pt-3'),

])


@app.callback(Output(component_id='url', component_property='pathname'),
              [Input(component_id='tabs', component_property='active_tab')])
def update_pathname(selected_tab):
    """Changes the url when active_tab changes, triggering update_tab callback"""

    return next(filter(lambda x: x['name'] == selected_tab, TABS))['url']


@app.callback(
    [Output(component_id='tab-container', component_property='children'),
     Output(component_id='tabs', component_property='active_tab')],
    [Input(component_id='url', component_property='pathname')],
    State(component_id='tabs', component_property='active_tab')
)
def update_tab(curr_url, active_tab_state):
    """Updates selected tab and tab container on url update"""

    return next(filter(lambda x: x['url'] == curr_url, TABS))['container'],\
        next(filter(lambda x: x['url'] == curr_url, TABS))['name']


