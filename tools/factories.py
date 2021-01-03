import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import csv


def jumbotron_from_title_paragraphs(title, paragraphs, className='pt-2 pb-2'):
    """Creates a jumbotron from a title and a list of strings, that will be split into lines in a paragraph"""

    return dbc.Jumbotron([
        html.H3(title),
        html.Br(),
        html.P(sum([[p, html.Br()]for p in paragraphs], [])[:-1], className='lead')
    ], className=className)


def jumbotron_2_columns(title, col_0_text='', col_1_text=''):
    return dbc.Jumbotron([
        dbc.Row([
            dbc.Col([html.H3(title), html.Br()])
        ]),
        dbc.Row([
            dbc.Col([dcc.Markdown(col_0_text)], width=5, className='lead text-justify'),
            dbc.Col([], width=1),
            dbc.Col([dcc.Markdown(col_1_text)], width=5, className='lead text-justify'),

        ])
    ], className='pt-4 pb-2')


def text_with_info_tooltip(text, tooltip, text_id, placement='top'):
    """Text with info icon and tooltip on hover"""

    return html.Div([
        dcc.Markdown(text + ' &#x1F6C8', text_id,  className='h6'),
        dbc.Tooltip(tooltip, target=text_id, placement=placement)
    ], className='h6')


def csv_to_markdown(csv_file_path):
    csvfile = open(csv_file_path, newline='')
    text_dict = {n[0]: [n[i + 1] for i in range(len(n) - 1) if n[i + 1] != ''] for n in csv.reader(csvfile)}
    text_str = '  \n'.join(f'**{key}:** ' + ', '.join(f'{value}' for value in values) for key, values in text_dict.items())
    return dcc.Markdown(text_str, className='h6')


if __name__ == '__main__':
    from pathlib import Path
    base_path = Path('C:/Users/Sanchez/Desktop/m3data')

    print(csv_to_markdown(base_path / 'csvs/lexcats_3.csv'))



