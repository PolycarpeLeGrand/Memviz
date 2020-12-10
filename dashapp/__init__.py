import pickle
import dash
import dash_bootstrap_components as dbc

from config import METADATA_DF_PATH, TOPIC_REDUCTIONS_DF_PATH, DOC_TOPICS_DF_PATH, \
    TOPIC_WORDS_DF_PATH, TOPIC_MAPPING, PROJECT_TITLE, LEXCATS_TEXTS_DF_PATH, LEXCATS_ABS_DF_PATH, LEXCATS_PARAS_DF_PATH

G = 'https://fonts.googleapis.com/icon?family=Material+Icons'

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SIMPLEX, G], suppress_callback_exceptions=True, title=PROJECT_TITLE)


def load_df(path):
    with open(path, 'rb') as temp:
        return pickle.load(temp)


METADATA_DF = load_df(METADATA_DF_PATH)
DOC_TOPICS_DF = load_df(DOC_TOPICS_DF_PATH)
TOPIC_WORDS_DF = load_df(TOPIC_WORDS_DF_PATH)
TOPIC_REDUCTIONS_DF = load_df(TOPIC_REDUCTIONS_DF_PATH)

# LEXICON_DF = load_df(LEXICON_DF_PATH)
LEXCATS_TEXTS_DF = load_df(LEXCATS_TEXTS_DF_PATH)
LEXCATS_ABS_DF = load_df(LEXCATS_ABS_DF_PATH)
LEXCATS_PARAS_DF = load_df(LEXCATS_PARAS_DF_PATH)


# Mapping topic names
DOC_TOPICS_DF.columns = DOC_TOPICS_DF.columns.map(TOPIC_MAPPING)
TOPIC_REDUCTIONS_DF['main_topic'] = TOPIC_REDUCTIONS_DF['main_topic'].map(TOPIC_MAPPING)
TOPIC_WORDS_DF.index = TOPIC_WORDS_DF.index.map(TOPIC_MAPPING)

