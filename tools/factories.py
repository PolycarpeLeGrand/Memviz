import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


def jumbotron_from_title_paragraphs(title, paragraphs, className='pt-2 pb-2'):
    """Creates a jumbotron from a title and a list of strings, that will be split into lines in a paragraph"""

    return dbc.Jumbotron([
        html.H3(title),
        html.Br(),
        html.P(sum([[p, html.Br()]for p in paragraphs], [])[:-1], className='lead')
    ], className=className)

