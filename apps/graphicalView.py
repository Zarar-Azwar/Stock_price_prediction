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
from app import app
import datetime
import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import calendar
from datetime import datetime,date,time
import pytz
import modules as md

FA="https://use.fontawesome.com/releases/v5.12.1/css/all.css"
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
cardClass="shadow border border-primary text-primary mt-4 mb-2"
styleHead={'color':'blue','font-size': '28px','color':'#0275D8'}
headerstyle={'color':'#46AFC4','text-align': 'center','font-size': '18px'}
graphs=dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H3('Graphical View',id='graphView',style=styleHead)
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.H3('Top 10 Sectors',style=headerstyle)
                        ]),
                        dbc.CardBody([
                            dcc.Graph(id='top10Turnover',figure={})
                        ])
                    ],className=cardClass)
                    
                ]),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.H3('Top 10 Current Prices',style=headerstyle)
                        ]),
                        dbc.CardBody([
                            dcc.Graph(id='top10Current',figure={})
                        ])
                    ],className=cardClass)
                    
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.H3('Top 10 Advances',style=headerstyle)
                        ]),
                        dbc.CardBody([
                            dcc.Graph(id='top10advances',figure={})
                        ])
                    ],className=cardClass)
                    
                ]),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.H3('Top 10 Declines',style=headerstyle)
                        ]),
                        dbc.CardBody([
                            dcc.Graph(id='top10Decliner',figure={})
                        ])
                    ],className=cardClass)
                    
                ])
            ])
        ])
    ])
])
interval=html.Div([
    dcc.Interval(id='oneMInterval',interval=60000,n_intervals=0)
])
layout=dbc.Container([interval,graphs],fluid=True)

@app.callback(
    [
        Output(component_id='top10Turnover',component_property='figure'),
        Output(component_id='top10Current',component_property='figure'),
        Output(component_id='top10advances',component_property='figure'),
        Output(component_id='top10Decliner',component_property='figure')
    ],
    Input(component_id='oneMInterval',component_property='n_intervals')
)
def tableGraph(interval):
    datadf=md.sectorDataScrap()
    datadf=md.sectorDataCleaning(datadf)
    top10turnover=datadf.sort_values(by='Turnover',ascending=False)
    top10turnover=top10turnover[:10]
    top10Current=datadf.sort_values(by='Current',ascending=False)
    top10Current=top10Current[:10]
    top10Advances=datadf.sort_values(by='Advance',ascending=False)
    top10Advances=top10Advances[:10]
    top10Declines=datadf.sort_values(by='Decline',ascending=False)
    top10Declines=top10Declines[:10]
    
    figTO=px.pie(top10turnover, values='Turnover', names='Sector Name',
            color_discrete_sequence=px.colors.sequential.haline,height=400)
    figTO.update(layout_showlegend=False)
    #figTO.update_traces(textposition='inside', textinfo='percent+Sector Name')
    figC=px.pie(top10Current, values='Current', names='Sector Name',
            color_discrete_sequence=px.colors.sequential.haline,height=400)
    figC.update(layout_showlegend=False)
    figAd=px.pie(top10Advances, values='Advance', names='Sector Name',
            color_discrete_sequence=px.colors.sequential.haline,height=400)
    figAd.update(layout_showlegend=False)
    figDec=px.pie(top10Declines, values='Decline', names='Sector Name',
            color_discrete_sequence=px.colors.sequential.haline,height=400)
    figDec.update(layout_showlegend=False)
    #print(data)
    
# Customize aspect

    return figTO,figC,figAd,figDec
if __name__ == "__main__":
    app.run_server()