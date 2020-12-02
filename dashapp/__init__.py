import dash
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SIMPLEX], suppress_callback_exceptions=True)

DATA = [2312, 34234, 3453]  # with temp as open(): DATA = pickle.load(PATH)

