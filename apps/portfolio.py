from tkinter.messagebox import NO
from turtle import title
from xmlrpc.server import resolve_dotted_attribute
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
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Label('Enter Amount (Rs)',style={'font-size':'20px','font-weight': 'bold',
                                'color':'#46AFC4','text-align': 'center'},className='mx-auto'),
                    dbc.Input(id='amount',placeholder="Amount", type="number",style=styleDrpdown,
                                className='d-flex justify-content-center mt-2 mb-2'),
                    dcc.Dropdown(
                        id='portfolioOptionDropdown',
                        options=[{'label':'SHORT TERM','value':'ST'},
                                {'label':'MEDIUM TERM','value':'MT'},
                                {'label':'LONG TERM','value':'LT'}],
                        value='ST',
                        style=styleDrpdown,
                        className='mt-2 mb-2'
                    ),
                    dbc.Button('OK!',id='portfolioMaker',style={'border-radius': '18px'},
                        className='btn-primary mx-auto mt-2')
                
                ]),
                
                
            ],className=cardClass)
        ],className='col-md-6')
    ],className='d-flex justify-content-center mb-4 mt-4'),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                   html.H5('Portfolio Chart')
                ],className='bg-primary text-white'),
                dbc.CardBody([
                    dcc.Graph(id='pieChartPortfolio',figure={})
                ])
            ],className=cardClass)
        ],className='col-md-6'),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                   html.H5('Portfolio Table')
                ],className='bg-primary text-white'),
                dbc.CardBody([
                    dash_table.DataTable(
                        id='portfolio_Table',
                        style_as_list_view=True,
                        style_cell={'padding': '2px','font-family': 'Arial','font-size': '14px','text-align': 'center'},
                        style_header={
                            'backgroundColor': '#0275D8',
                            'fontWeight': 'bold',
                            'text-align': 'center',
                            'border': '1px solid gray',
                            'font-size': '15px',
                            'color': 'white',
                        },
                        style_data={ 'border': '1px solid gray' },
                    )
        
                ])
            ],className=cardClass)
        ],className='col-md-6')
    ]),

    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader([
                    html.H5('Portfolio')
                ],className='bg-primary text-white'),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col(
                            id='portfolioList'
                        )
                    ])
                ])
            ],className=cardClass)
            
        ),
        
    ])
    

])

@app.callback(
    Output(component_id='portfolioList',component_property='children'),
    Output(component_id='pieChartPortfolio',component_property='figure'),
    Output(component_id='portfolio_Table',component_property='columns'),
    Output(component_id='portfolio_Table',component_property='data'),
    Input(component_id='portfolioMaker',component_property='n_clicks'),
    Input(component_id='portfolioOptionDropdown',component_property='value'),
    Input(component_id='amount',component_property='value'),
    prevent_initial_call=True,
)
def portfolioReturn(click,val,amount):
    portfolioTable,leftover=md.portfolioMaker(conDf,amount,choice=val)
    symbs=portfolioTable['Ticker'].tolist()
    tempdf=conDf[symbs]
    linefigures=[]
    deltafigures=[]
    closes=[]
    compNames=[]
    sectorNames=[]
    noOfShares=[]
    shareAmount=[]
    companies=pd.read_csv('companies.csv')
    for col in tempdf.columns:
        closes.append("{0:,.2f}".format(tempdf[tempdf.index==tempdf.index.max()][col][0]))
        for i in range(len(companies)):
            if companies['Symbol'][i]==col:
                compNames.append(companies['Name'][i])
                sectorNames.append(companies['Sector'][i])
        
        for i in range(len(portfolioTable)):
            if(portfolioTable['Ticker'][i]==col):
                noOfShares.append("{0:,.2f}".format(portfolioTable['Shares'][i]))
                shareAmount.append("{0:,.2f}".format(portfolioTable['Amount'][i]))
        linefigures.append(md.lineReturnPortfolio(tempdf,col))
        deltafigures.append(md.deltaGraphPortfolio(tempdf,col))
    
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
                        ],width=3),
                        dbc.Col([
                            dbc.Row([
                                dbc.Col([
                                    html.H6('CLOSE',style={'font-size': '15px','color':'#46AFC4'})
                                ]),
                                dbc.Col([
                                    html.H6('SHARES',style={'font-size': '15px','color':'#46AFC4'})
                                ]),
                                dbc.Col([
                                    html.H6('AMOUNT',style={'font-size': '15px','color':'#46AFC4'})
                                ]) 
                            ],className='mt-2'),
                            dbc.Row([
                                dbc.Col([
                                    html.H3(closes[i],id='open1',style={'font-size': '21px','color':'black'})
                                ]),
                                dbc.Col([
                                    html.H3(noOfShares[i],id='volume1',style={'font-size': '21px','color':'black'})
                                ]),
                                dbc.Col([
                                    html.H3(shareAmount[i],id='volume1',style={'font-size': '21px','color':'black'})
                                ])
                            ])
                        ],width=4,className='mt-3'),
                        dbc.Col([
                            dcc.Graph(id='delgraphPortfolio', figure=deltafigures[i],config={'displayModeBar':False})
                        ],width=2,className='d-flex align-items-center'),
                        dbc.Col([
                            dcc.Graph(id='lineportfolio', figure=linefigures[i],config={'displayModeBar':False})
                        ],width=3)
                    ])
                
                ]),
            ],className=cardClass)
        ])for i in range(len(tempdf.columns.tolist()))

    ]

    figTO=px.pie(portfolioTable, values='Amount', names='Ticker',
            color_discrete_sequence=px.colors.sequential.haline,height=400)
    
    cols=[{'name':i,'id':i} for i in portfolioTable.columns]
    dataP=portfolioTable.to_dict('records')


    return cards,figTO,cols,dataP



