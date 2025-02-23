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
import calendar
from datetime import datetime,date,time
import pytz
import os
import modules as md
from app import app
FA="https://use.fontawesome.com/releases/v5.12.1/css/all.css"
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
valueZero=0
# make a reuseable dropdown for the different examples
import pandas as pd

cardClass="shadow border mt-2 mt-2"
styleHead={'color':'blue','font-size': '28px','color':'#0275D8'}#'backgroundColor': '#0275D8'
classHead='mt-2'


companies=pd.read_csv('companies.csv')
df=pd.read_csv('complete_data.csv')
styleDrpdown={'border-radius': '18px','border-color':'#46AFC4','color':'#46AFC4'}
outlineClass=''
cardClass="shadow border border-primary mt-4 mb-2"
companies=companies.rename(columns={'Symbol':'SYMBOL'})
companiesDF=companies[['SYMBOL','Name']]
newDF=pd.merge(df,companiesDF,on='SYMBOL')
newDF.sort_values(by='Date',inplace=True,ascending=False)
df=newDF
dff=pd.read_csv('complete_data.csv')
dff=md.dataCleaningPortfolio(dff)
symbols=dff['SYMBOL'].unique()
conDf=md.byCompanies(dff,symbols)
labels=[]
for i in range(len(companies)):
    labels.append({'value':companies['SYMBOL'][i],'label':companies['Name'][i]})
layout=dbc.Container([
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader([
                    html.H5('Recommendation',id='recom')
                ],className='bg-primary text-white'),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col(
                            id='recommendation'
                        )
                    ])
                ])
            ],className=cardClass)
            
        ),
        
    ])
])

@app.callback(
    Output(component_id='recommendation',component_property='children'),
    Input(component_id='recom',component_property='children')
)
def recommendation(val):
    recomender,deltagraphs=md.recommendationReturn(conDf)
    symbs=recomender.index
    compNames=[]
    sectorNames=[]
    companies=pd.read_csv('all_Companies.csv')
    for s in symbs:
        for i in range(len(companies)):
            if companies['Symbol'][i]==s:
                compNames.append(companies['Name'][i])
                sectorNames.append(companies['Sector'][i])
    cards=[
        dbc.Container([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H1(children=compNames[i],style={'font-size':'25px','font-weight': 'bold','text-align': 'left',
                                'margin-top':'15px'}),
                            html.H5(children=sectorNames[i],
                                style={'font-size':'12px','text-align': 'left','color':'#A0A0A0'})
                        ],className='mt-2',width=4),
                        dbc.Col([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Row([
                                        dbc.Col([
                                            html.H6('1D',style={'font-size': '18px','color':'#46AFC4','text-align': 'center'}),
                                            dcc.Graph(figure=deltagraphs[i][0],config={'displayModeBar':False})
                                        ],className='mt-2',width=2),
                                        dbc.Col([
                                            html.H6('1W',style={'font-size': '18px','color':'#46AFC4','text-align': 'center'}),
                                            dcc.Graph(figure=deltagraphs[i][1],config={'displayModeBar':False})
                                        ],className='mt-2',width=2),
                                        dbc.Col([
                                            html.H6('1M',style={'font-size': '18px','color':'#46AFC4','text-align': 'center'}),
                                            dcc.Graph(figure=deltagraphs[i][2],config={'displayModeBar':False})
                                        ],className='mt-2',width=2),
                                        dbc.Col([
                                            html.H6('3M',style={'font-size': '18px','color':'#46AFC4','text-align': 'center'}),
                                            dcc.Graph(figure=deltagraphs[i][3],config={'displayModeBar':False})
                                        ],className='mt-2',width=2),
                                        dbc.Col([
                                            html.H6('6M',style={'font-size': '18px','color':'#46AFC4','text-align': 'center'}),
                                            dcc.Graph(figure=deltagraphs[i][4],config={'displayModeBar':False})
                                        ],className='mt-2',width=2),
                        
                                    ])
                                ])
                            ]),
                        ],width=8)
                    ])
                
                ]),
            ],className=cardClass)
        ])for i in range(len(recomender))

    ]
    return cards