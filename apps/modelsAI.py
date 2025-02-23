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
from plotly.graph_objects import Layout
from plotly.validator_cache import ValidatorCache
import pytz
import os
import modules as md
from app import app

df1=pd.read_csv('complete_data.csv')
styleDrpdown={'border-radius': '18px','border-color':'#46AFC4','color':'#46AFC4'}
outlineClass=''
cardClass="shadow mt-2 mt-2"
styleHead={'color':'blue','font-size': '28px','color':'#0275D8'}
tickers=['FFC','NESTLE','LUCK','HBL','ARPL','EFERT','SEPL','BAHL','UBL','COLG','MARI',
         'APL','DAWH','POL','BATA','INIL','MCB','ISL','MTL','AGIL','ENGRO','EFUG','ZIL','AGP','GADT']
companiesTicker=[]
companies=pd.read_csv('companies.csv')
for ticker in tickers:
    for i in range(len(companies)):
        if ticker ==companies['Symbol'][i]:
            companiesTicker.append({'label':companies['Name'][i],'value':ticker})
layout=dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Dropdown(
                        id='aiModelDropDown',
                        options=companiesTicker,
                        value='FFC',
                        style=styleDrpdown
                    ),
                ])
            ],className=cardClass),
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H3(id='companyName',style={'font-weight': 'bold','color':'green','font-size': '20px'}),
                            html.H3(id='companySym',style={'font-weight': 'bold','font-size': '14px'}),
                            html.H2(id='sectorName',style={'font-weight': 'bold','font-size': '24px'})
                        ],width=4),
                        
                        dbc.Col([
                            dbc.Row([
                                dbc.Col([
                                    html.H3('CLOSE',style={'font-weight': 'bold','color':'green','font-size': '16px'}),
                                    html.H3(id='currentPrice',style={'font-weight': 'bold','font-size': '22px'})
                                ]),
                                dbc.Col([
                                    html.H3('VOLUME',style={'font-weight': 'bold','color':'green','font-size': '16px'}),
                                    html.H3(id='currentVolm',style={'font-weight': 'bold','font-size': '22px'})
                                ]),
                                dbc.Col([
                                    dcc.Graph(id='delta-graph', config={'displayModeBar':False})
                                ]),
                        
                            ])
                        ],width=4,className='d-flex align-items-center'),
                        dbc.Col([
                            dcc.Graph(id='lineGraph', config={'displayModeBar':False})
                        ],width=4),
                    ])
                    
                ])
            ],className=cardClass)
        ],className='mt-2 mb-2')
    ]),
    dbc.Row([
        dbc.Col([
            html.H3('Previous 7 Days',style=styleHead)
        ],className='mb-2 mt-2')
    ]),
    dbc.Row(
        id='previousfigure'
    ),
    dbc.Row([
        dbc.Col([
            html.H3('Next 7 Days Predictions',style=styleHead)
        ],className='mb-2 mt-2')
    ]),
    dbc.Row(
        id='nextfigure'
    )

])

@app.callback(
    Output(component_id='companyName',component_property='children'),
    Output(component_id='companySym',component_property='children'),
    Output(component_id='sectorName',component_property='children'),
    Output(component_id='currentPrice',component_property='children'),
    Output(component_id='currentVolm',component_property='children'),
    Output(component_id='delta-graph',component_property='figure'),
    Output(component_id='lineGraph',component_property='figure'),
    Input(component_id='aiModelDropDown',component_property='value')
)
def infoReturn(val):
    df=md.DataClean(df1,val)
    df=df[['SYMBOL','LDCP','OPEN','HIGH','LOW','CLOSE','VOLUME']]
    #print(md.predictionFun(df,val))
    for i in range(len(companies)):
        if companies['Symbol'][i]==val:
            sect=companies['Sector'][i]
            name=companies['Name'][i]
    indexes=df.index.tolist()
    maxDate=df.index.max()
    for i in range(len(indexes)):
        if indexes[i]==maxDate:
            start_date=indexes[i-10]
    dff=df[start_date:] 
    fig1 = go.Figure(go.Indicator(
        mode="delta",
        value=df[df.index==maxDate]['CLOSE'][0],
        delta={'reference': df.iloc[df.index.get_loc(maxDate)-1]['CLOSE'],'relative': True, 'valueformat':'.2%'}))
    fig1.update_traces(delta_font={'size':21})
    fig1.update_layout(height=50, width=120)

    fig = px.line(df, x=df.index, y='CLOSE',
               range_y=[df['CLOSE'].min(), df['CLOSE'].max()],
               height=140).update_layout(margin=dict(t=0, r=0, l=0, b=20),
                                         paper_bgcolor='rgba(0,0,0,0)',
                                         plot_bgcolor='rgba(0,0,0,0)',
                                         yaxis=dict(
                                         title=None,
                                         showgrid=False,
                                         showticklabels=False
                                         ),
                                         xaxis=dict(
                                         title=None,
                                         showgrid=False,
                                         showticklabels=False
                                         ))

    day_start = df[df.index == df.index.max()]['LDCP'].values[0]
    day_end = df[df.index == df.index.max()]['CLOSE'].values[0]
    if day_end > day_start:
        fig.update_traces(fill='tozeroy',line={'color':'green'})
    elif day_end < day_start:
        fig.update_traces(fill='tozeroy',line={'color': 'red'})
    else:
        fig.update_traces(fill='tozeroy',line={'color': 'blue'})

    volmR="{:,}".format(float(df[df.index==maxDate]['VOLUME'][0]))
    return name,val,sect,df[df.index==maxDate]['CLOSE'][0],volmR,fig1,fig


@app.callback(
    Output(component_id='previousfigure',component_property='children'),
    Input(component_id='aiModelDropDown',component_property='value')
)
def previousDays(val):
    df=md.DataClean(df1,val)
    df=df[['SYMBOL','LDCP','OPEN','HIGH','LOW','CLOSE','VOLUME']]

    indexes=df.index.tolist()
    maxDate=df.index.max()
    for i in range(len(indexes)):
        if indexes[i]==maxDate:
            start_date=indexes[i-6]  
    dff=df[start_date:]
    prices=[]
    figures=[]
    styles=[]
    for i in range(len(dff)):
        prices.append(dff['CLOSE'][i])
        figures.append(md.deltaGraph(dff[i:i+1][:]))
        if dff['CLOSE'][i]>dff['LDCP'][i]:
            styles.append({'font-weight': 'bold','color':'green','text-align': 'center','font-size': '25px'})
        elif dff['CLOSE'][i]<dff['LDCP'][i]:
            styles.append({'font-weight': 'bold','color':'red','text-align': 'center','font-size': '25px'})
        else:
            styles.append({'font-weight': 'bold','color':'blue','text-align': 'center','font-size': '25px'})
    cards=[
        dbc.Col([
            dbc.Card([
                dbc.Row([
                    dbc.Col([
                        html.H2(children=prices[i],style=styles[i]),
                        dcc.Graph(figure= figures[i],config={'displayModeBar':False},
                        style={'align-items': 'center','text-align': 'center'})
                    ],className='mt-2 mb-2')
                ])
                
            ],className=cardClass)
        ],className='mt-2 mb-2')for i in range(len(dff))
    ]
    return cards
    

@app.callback(
    Output(component_id='nextfigure',component_property='children'),
    Input(component_id='aiModelDropDown',component_property='value')
)
def previousDays(val):
    df=md.DataClean(df1,val)
    df=df[['SYMBOL','LDCP','OPEN','HIGH','LOW','CLOSE','VOLUME']]

    predictions=md.predictionFun(df,val)
    prices=[]
    figures=[]
    styles=[]
    for i in range(len(predictions)-1):
        prices.append("{:.3f}".format(round(predictions[i+1], 3)))
        figures.append(md.delta(predictions[i],predictions[i+1]))
        if predictions[i+1]>predictions[i]:
            styles.append({'font-weight': 'bold','color':'green','text-align': 'center','font-size': '25px'})
        elif predictions[i+1]<predictions[i]:
            styles.append({'font-weight': 'bold','color':'red','text-align': 'center','font-size': '25px'})
        else:
            styles.append({'font-weight': 'bold','color':'blue','text-align': 'center','font-size': '25px'})
    card=[
        dbc.Col([
            dbc.Card([
                dbc.Row([
                    dbc.Col([
                        html.H2(children=prices[i],style=styles[i]),
                        dcc.Graph(figure= figures[i],config={'displayModeBar':False})
                    ],className='mt-2 mb-2')
                ])
                
            ],className=cardClass)
        ],className='mt-2 mb-2')for i in range(len(figures))
    ]
    return card
        

