from dash import dcc
from dash import  html
from dash.dependencies import Input, Output
from apps import Home,companies
# Connect to main app.py file
from app import app
from app import server
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
import dash_daq as daq
from dash import dcc
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dash_table
import pandas as pd
import datetime

layout=dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Interval(id='inter',interval=60000,n_intervals=0),
            html.H2(id='time'),
            html.H1('helloworld')
        ])
    ])
])
@app.callback(
    Output(component_id='inter',component_property='n_intervals'),
    Input(component_id='time',component_property='children')
)
def timeInteval(inter):
    print(inter)
    return inter