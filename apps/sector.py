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
valueZero=0
styleDrpdown={'border-radius': '18px','border-color':'#46AFC4','color':'#46AFC4'}
outlineClass=''
styleHead={'color':'blue','font-size': '28px','color':'#0275D8'}
cardClass="shadow border border-primary text-primary mt-4 mt-2"
# make a reuseable dropdown for the different examples
sector=dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H3('Sector Summary',id='sector',style=styleHead)
        ])
    ]),
    dbc.Row([
        dbc.Col([
           dbc.Card([
               dbc.CardHeader(
                   html.H4('MAX Turnover',
                           style={'font-family': 'Arial','font-size': '14px','text-align': 'center'})
               ),
               dbc.CardBody([
                   html.H1(id='mTurnOver',
                          style={'font-family': 'Arial','font-size': '18px','text-align': 'center','fontWeight':'bold'})
               ])
           ],className=cardClass)
        ]),
        dbc.Col([
            dbc.Card([
               dbc.CardHeader(
                   html.H4('MAX Price',
                           style={'font-family': 'Arial','font-size': '14px','text-align': 'center'})
               ),
               dbc.CardBody([
                   html.H1(id='mPrice',
                          style={'font-family': 'Arial','font-size': '18px','text-align': 'center','fontWeight':'bold'})
               ])
           ],className=cardClass)
           
        ]),
        dbc.Col([
            dbc.Card([
               dbc.CardHeader(
                   html.H4('MAX + Change',
                           style={'font-family': 'Arial','font-size': '14px','text-align': 'center'})
               ),
               dbc.CardBody([
                   html.H1(id='mPChange',
                          style={'font-family': 'Arial','font-size': '18px','text-align': 'center','fontWeight':'bold'})
               ])
           ],className=cardClass)
           
        ]),
        dbc.Col([
            dbc.Card([
               dbc.CardHeader(
                   html.H4('MAX - Change',
                           style={'font-family': 'Arial','font-size': '14px','text-align': 'center'})
                   
               ),
               dbc.CardBody([
                   html.H1(id='mNChange',
                          style={'font-family': 'Arial','font-size': '18px','text-align': 'center','fontWeight':'bold'})
               ])
           ],className=cardClass)
           
        ]),
        dbc.Col([
            dbc.Card([
               dbc.CardHeader(
                   html.H4('MAX Advance',
                           style={'font-family': 'Arial','font-size': '14px','text-align': 'center'})
                   
               ),
               dbc.CardBody([
                   html.H1(id='mAd',
                           style={'font-family': 'Arial','font-size': '18px','text-align': 'center','fontWeight':'bold'})
               ])
           ],className=cardClass)
           
        ]),
        dbc.Col([
            dbc.Card([
               dbc.CardHeader(
                   html.H4('MAX Decline',
                           style={'font-family': 'Arial','font-size': '14px','text-align': 'center'})
                   
               ),
               dbc.CardBody([
                   html.H4(id='mDec',
                           style={'font-family': 'Arial','font-size': '18px','text-align': 'center','fontWeight':'bold'})
               ])
            
           ],className=cardClass)
           
        ])
        
    
    ],className='mb-2 mt-2 d-flex align-items-center justify-content-center'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='sector_bargraph',figure={})
                ])
            ],className=cardClass)
        ])
    ],className='mb-2 mt-2'),
    dbc.Row([
        dbc.Col([
                dbc.Button(html.Span([html.I(className='fas fa-arrow-circle-down')]),id='downloadButton',
                className='rounded-circle btn-primary'),
                dcc.Download(id='downloadOption')
        ],className='d-flex justify-content-end')
    ],className='mb-2 mt-4'),
    dbc.Row([
        dbc.Col([
            dash_table.DataTable(
                id='sectortable',
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
                style_data_conditional=([
                    {
                        'if':{
                            'filter_query':'{Change} < 0'
                        },
                        'color': 'red'
                    },
                    {
                        'if':{
                            'filter_query':'{Change} > 0'
                        },
                        'color': 'green'
                    },
                    {
                        'if':{
                            'filter_query':'{Change} = 0'
                        },
                        'color': 'blue'
                    },
                    {
                        'if':{
                            'column_id':'Sector Name'
                        },
                        'textAlign': 'left',
                        'font-size': '15px'
                        
                    }
                ])
            )
        ],className='mb-5')
    ]),
])
interval=html.Div([
    dcc.Interval(id='MinuteInterval',interval=60000,n_intervals=0)
])
layout=dbc.Container([interval,sector],fluid=True)
@app.callback(
    Output(component_id='downloadOption',component_property='data'),
    Input(component_id='downloadButton',component_property='n_clicks'),
    prevent_initial_call=True,
)
def download(click):
    if click > 0:
        data=md.sectorDataScrap()
        data=md.sectorDataCleaning(data)
        return dcc.send_data_frame(data.to_csv,"data.csv")

@app.callback(
    [
        Output(component_id='sector_bargraph',component_property='figure'),
        Output(component_id='sectortable',component_property='data'),
        Output(component_id='sectortable',component_property='columns'),
        Output(component_id='mTurnOver',component_property='children'),
        Output(component_id='mPrice',component_property='children'),
        Output(component_id='mPChange',component_property='children'),
        Output(component_id='mNChange',component_property='children'),
        Output(component_id='mAd',component_property='children'),
        Output(component_id='mDec',component_property='children'),
    ],
    Input(component_id='MinuteInterval',component_property='n_intervals')
)
def tableGraph(interval):
    data=md.sectorDataScrap()
    data=md.sectorDataCleaning(data)
    print(data)
    fig=px.bar(data,'Sector Code','Turnover',hover_data=['Sector Name', 'Turnover'],height=400)
    cols=data.columns
    cols=cols.tolist()
    data=data[cols]
    mTO="{:,}".format(data['Turnover'].max())
    mP="{:,}".format(data['Current'].max())
    mPC="{:,}".format(data['Change'].max())
    mNC="{:,}".format(data['Change'].min())
    mAd=data['Advance'].max()
    mDec=data['Decline'].max()
    cols=[{'name':i,'id':i} for i in cols]
    dataD=data.to_dict('records')
    return fig,dataD,cols,mTO,mP,mPC,mNC,mAd,mDec
if __name__ == "__main__":
    app.run_server()