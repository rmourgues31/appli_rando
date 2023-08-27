from dash import Dash
import dash_bootstrap_components as dbc
import os

app = Dash(prevent_initial_callbacks=True, 
           external_stylesheets=[dbc.themes.LUMEN],
           title="Itirando",
           update_title='Chargement...',
           assets_folder=os.getenv("ASSETS"))
