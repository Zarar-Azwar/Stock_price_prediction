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
import modules as md
from app import app

df=pd.read_csv('complete_data.csv')
data=pd.read_csv('companies.csv')
companies=data.rename(columns={'Symbol':'SYMBOL'})
companiesDF=companies[['SYMBOL','Name','Sector']]
newDF=pd.merge(df,companiesDF,on='SYMBOL')
newDF.sort_values(by='Date',inplace=True,ascending=False)
DataUSE=newDF[['Date','Name','SYMBOL','Sector','LDCP','OPEN','HIGH','LOW','CLOSE','CHANGE','VOLUME']]

cleaning=['LDCP','OPEN','HIGH','LOW','CLOSE','CHANGE','VOLUME']
for c in cleaning:
    if(DataUSE[c].dtype=='object' or DataUSE[c].dtype=='str'):
        try:
            op=DataUSE[c].tolist()
            opn=[]
            for i in op:
                opn.append(float(i.replace(',','')))
            DataUSE[c]=opn
        except:
            print(i,c)

DataUSE.set_index(DataUSE.Date,inplace=True)
DataUSE.drop('Date',axis=1,inplace=True)

values=DataUSE.Sector.unique()
sectors=[]
for i in range(len(values)):
    sectors.append({'value':values[i],'label':values[i]})
styleDrpdown={'border-radius': '18px','border-color':'#46AFC4','color':'#46AFC4'}
outlineClass=''
cardClass="shadow mt-2 mt-2"
layout=dbc.Container([
    
    dbc.Row([
        dbc.Card([
            dcc.Dropdown(
                id='sector-dropdown',
                options=sectors,
                value='FOOD & PERSONAL CARE PRODUCTS',
                style=styleDrpdown,
                className='mt-2 mb-2'
            ),
        ],className=cardClass)
        
    ]),
    dbc.Row([
        dbc.Col(
            id='companiesList'
        )
    ])
],fluid=True)
@app.callback(
    Output(component_id='companiesList',component_property='children'),
    Input(component_id='sector-dropdown',component_property='value'),
)
def company(val):
    dUSE=DataUSE[DataUSE.index==DataUSE.index.max()]
    symb=dUSE[dUSE['Sector']==val]['SYMBOL']
    symbL=symb.values.tolist()
    dataFigures=[]
    figLlist=[]
    figClist=[]
    for symb in symbL:
        d=DataUSE[DataUSE['SYMBOL']==symb]
        dataFigures.append(d)
        figL=md.lineReturn(d)
        figLlist.append(figL)
        figC=md.deltaGraph(d)
        figClist.append(figC)
        
    cards=[
        dbc.Container([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Row([
                                dbc.Col([
                                    html.H1(dataFigures[i]['Name'][0],id='compName',style={'font-size':'23px','font-weight': 'bold','text-align': 'left'}),
                                ])    
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.H4(dataFigures[i]['SYMBOL'][0],id='compSymb',style={'font-size':'14px','font-weight': 'bold','text-align': 'left'})
                                ])
                            ])
                        ],width=3), #d-flex flex-wrap align-content-around
                        dbc.Col([
                            dbc.Row([
                                dbc.Col([
                                    html.H2(dataFigures[i]['CLOSE'][0],id='close1',style={'font-size': '28px','color':'black'})
                                ],className='d-flex align-items-center'),
                            ]),
                             dbc.Row([
                                dbc.Col([
                                    dcc.Graph(id='change-graph', figure=figClist[i],config={'displayModeBar':False})
                                ],className='d-flex align-items-center'),
                            ]),
                        ],width=2),
                        dbc.Col([
                            dbc.Row([
                                dbc.Col([
                                    html.H6('HIGH',style={'font-size':'15px','color':'green'})
                                ]),
                                dbc.Col([
                                    html.H6('LOW',style={'font-size': '15px','color':'green'})
                                ])    
                            ],className='mt-2'),
                            dbc.Row([
                                dbc.Col([
                                    html.H3(dataFigures[i]['HIGH'][0],id='high1',style={'font-size': '21px','color':'black'})
                                ]),
                                dbc.Col([
                                    html.H3(dataFigures[i]['LOW'][0],id='low1',style={'font-size': '21px','color':'black'})
                                ])    
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.H6('OPEN',style={'font-size': '15px','color':'green'})
                                ]),
                                dbc.Col([
                                    html.H6('VOLUME',style={'font-size': '15px','color':'green'})
                                ])    
                            ],className='mt-2'),
                            dbc.Row([
                                dbc.Col([
                                    html.H3(dataFigures[i]['OPEN'][0],id='open1',style={'font-size': '21px','color':'black'})
                                ]),
                                dbc.Col([
                                    html.H3(dataFigures[i]['VOLUME'][0],id='volume1',style={'font-size': '21px','color':'black'})
                                ])   
                            ])
                        ],width=3),
                        dbc.Col([
                            dcc.Graph(id='daily-line', figure=figLlist[i],config={'displayModeBar':False})
                        ],width=4),
                        
                    ])
                    
                ])
            ],className=cardClass)
        ])for i in range(len(symbL))
    ]
    
    return cards
