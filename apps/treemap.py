from datetime import datetime
import dash
from dash import dcc
from dash import html
from dash.dcc.Graph import Graph
from dash.dependencies import Output, Input, State

import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dash_table
import pandas as pd
import calendar
from datetime import date
import modules as md
from app import app
companies=pd.read_csv('companies.csv')
df=pd.read_csv('complete_data.csv')
FA="https://use.fontawesome.com/releases/v5.12.1/css/all.css"

companies=companies.rename(columns={'Symbol':'SYMBOL'})
companiesDF=companies[['SYMBOL','Name','Sector']]
newDF=pd.merge(df,companiesDF,on='SYMBOL')
newDF.sort_values(by='Date',inplace=True,ascending=False)
styleHead={'color':'blue','font-size': '28px','color':'#0275D8'}
df=newDF
labels=[]
for i in range(len(companies)):
    labels.append({'value':companies['SYMBOL'][i],'label':companies['Name'][i]})
#df=df[:300][:]
cardClass="shadow border mt-4 mt-2"
headingsClass='mt-2 mb-2'

layout=dbc.Container([
    dbc.Row([
        html.H3('Treemap',id='treemap',style=styleHead),
        dcc.Graph(
            id='treemap',
            figure={},
        )
    ])
])




@app.callback(
    Output(component_id='treemap',component_property='figure'),
    Input(component_id='treemap',component_property='children')
)
def updateHeatmap(value):
    
    dff=md.cleanedHeatMap(df)
    figure=md.treeMapGenerator(dff)
    return figure
