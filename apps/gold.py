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
df=pd.read_csv('wholeData.csv')
df1=md.oneDay(df,'2021-12-27')
cardClass="shadow border mt-2 mt-2"
styleHead={'color':'blue','font-size': '28px','color':'#0275D8'}#'backgroundColor': '#0275D8'
classHead='mt-2'


layout=dbc.Container([
    html.Div([
        dcc.Interval(id='oMInterval',interval=60000,n_intervals=0)
    ]),
    html.Div([
        dcc.Interval(id='oDInterval',interval=86400000,n_intervals=0)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.Row([
                    dbc.Col([
                        html.Img(src=app.get_asset_url('gold.jpg'),
                        style={'width': '130px','radius':'8px','margin-left':'15px',
                        'margin-right':'5px','margin-top':'15px','margin-bottom':'15px'})
                    ],className='mr-auto',width=2),
                    dbc.Col([
                        html.H1('Barrick Gold Corporation (GOLD)',
                            style={'font-size':'25px','font-weight': 'bold','text-align': 'left',
                            'margin-top':'15px'}),
                        html.H5('NYSE - Nasdaq Real Time Price. Currency in USD',
                            style={'font-size':'12px','text-align': 'left','color':'#A0A0A0'})
                    ],className='mr-auto',width=5),
                    dbc.Col([
                        dbc.Row([
                            dbc.Col([
                                html.H3(id='goldCurr',
                                    style={'font-size':'30px','font-weight': 'bold','text-align': 'center',
                                    'margin-left':'25px',
                                'margin-top':'25px','margin-bottom':'25px'})
                            ],width=5),
                            dbc.Col([
                                html.H5(id='goldChange')
                            ],width=3),
                            dbc.Col([
                                html.H5(id='goldChangePer'),
                            ],width=4),
                        
                        ])
                    ],width=4),
                    
                ])

            ],className=cardClass)
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
           dbc.Card([
               dbc.CardHeader(
                   html.H4('OPEN',
                           style={'font-family': 'Arial','font-size': '14px','text-align': 'center'})
               ),
               dbc.CardBody([
                   html.H1(id='opGld',
                          style={'font-family': 'Arial','font-size': '18px','text-align': 'center','fontWeight':'bold'})
               ])
           ],className=cardClass)
        ]),
        #open,bid,high,low,volume,ask
        dbc.Col([
            dbc.Card([
               dbc.CardHeader(
                   html.H4('BID',
                           style={'font-family': 'Arial','font-size': '14px','text-align': 'center'})
               ),
               dbc.CardBody([
                   html.H1(id='bidGld',
                          style={'font-family': 'Arial','font-size': '18px','text-align': 'center','fontWeight':'bold'})
               ])
           ],className=cardClass)
           
        ]),
        dbc.Col([
            dbc.Card([
               dbc.CardHeader(
                   html.H4('HIGH',
                           style={'font-family': 'Arial','font-size': '14px','text-align': 'center'})
               ),
               dbc.CardBody([
                   html.H1(id='hiGld',
                          style={'font-family': 'Arial','font-size': '18px','text-align': 'center','fontWeight':'bold'})
               ])
           ],className=cardClass)
           
        ]),
        dbc.Col([
            dbc.Card([
               dbc.CardHeader(
                   html.H4('LOW',
                           style={'font-family': 'Arial','font-size': '14px','text-align': 'center'})
                   
               ),
               dbc.CardBody([
                   html.H1(id='lowGld',
                          style={'font-family': 'Arial','font-size': '18px','text-align': 'center','fontWeight':'bold'})
               ])
           ],className=cardClass)
           
        ]),
        dbc.Col([
            dbc.Card([
               dbc.CardHeader(
                   html.H4('VOLUME',
                           style={'font-family': 'Arial','font-size': '14px','text-align': 'center'})
                   
               ),
               dbc.CardBody([
                   html.H1(id='volGld',
                           style={'font-family': 'Arial','font-size': '18px','text-align': 'center','fontWeight':'bold'})
               ])
           ],className=cardClass)
           
        ]),
        dbc.Col([
            dbc.Card([
               dbc.CardHeader(
                   html.H4('ASK',
                           style={'font-family': 'Arial','font-size': '14px','text-align': 'center'})
                   
               ),
               dbc.CardBody([
                   html.H4(id='askGld',
                           style={'font-family': 'Arial','font-size': '18px','text-align': 'center','fontWeight':'bold'})
               ])
            
           ],className=cardClass)
           
        ])
        
    
    ],className='mb-2 mt-2 d-flex align-items-center justify-content-center'),


    dbc.Row([
        dbc.Col([
            html.H3('Previous 7 Days',id='goldID',style=styleHead)
        ],className='mb-2 mt-2')
    ]),
    dbc.Row(
        id='previousGoldfigure'
    ),
    dbc.Row([
        dbc.Col([
            html.H3('Next 7 Days Predictions',id='goldNext',style=styleHead)
        ],className='mb-2 mt-2')
    ]),
    dbc.Row(
        id='nextGoldfigure'
    ),
    dbc.Row([
        dbc.Col([
            html.H3('Market Watch',style=styleHead)
        ],className=classHead),
        dbc.Col([
                dbc.Button(html.Span([html.I(className='fas fa-arrow-circle-down')]),id='downloadGldBut',
                className='rounded-circle btn-primary mt-2'),
                dcc.Download(id='downloadGoldOp')
        ],className='d-flex justify-content-end')
    ],className='mb-2 mt-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dash_table.DataTable(
                    id='oneMinuteGoldTable',
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
                    filter_action="native",
                    sort_action="native",
                    page_current= 0,
                    page_size= 15,
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
                        
                    ])
                )
            
            ],className=cardClass),
        ],className='mb-5')
    ])





]) 

@app.callback(
    Output(component_id='downloadGoldOp',component_property='data'),
    Input(component_id='downloadGldBut',component_property='n_clicks'),
    prevent_initial_call=True,
)
def download(click):
    if click > 0:
        data=md.dataScrapMinute()
        return dcc.send_data_frame(data.to_csv,"data.csv")
@app.callback(
    Output(component_id='oneMinuteGoldTable',component_property='columns'),
    Output(component_id='oneMinuteGoldTable',component_property='data'),
    Input(component_id='oDInterval',component_property='n_intervals')
)
def datashow(interval):
    df=pd.read_csv('GOLDData.csv')
    df['Change']=0.00
    for i in range(1,len(df)):
        df['Change'][i]=round(df['Close'][i]-df['Close'][i-1],2)
    
    cols=['Date','Open','High','Low','Close','Change','Adj Close','Volume']
    dff=df[cols]
    dff.sort_values(by='Date',ascending=False,inplace=True)
    cols=[{'name':i,'id':i} for i in dff.columns]
    dataD=dff.to_dict('records')
    
    return cols,dataD

 


@app.callback(
    Output(component_id='previousGoldfigure',component_property='children'),
    Input(component_id='goldID',component_property='children')
)
def previousDays(val):
    df=pd.read_csv('GOLDData.csv')
    predictions=md.marketGoldPre(df)
    predictions,showPre=md.predictClean(predictions)
    vals,showData=md.dataExt(df)
    figures=md.deltaGraphs(vals,predictions)
    prices=showData[1:]
    figures=figures[:7]
    styles=[]
    for i in range(len(showData)-1):
        if showData[i]>showData[i+1]:
            styles.append({'font-weight': 'bold','color':'red','text-align': 'center','font-size': '25px'})
        elif showData[i]<showData[i+1]:
            styles.append({'font-weight': 'bold','color':'green','text-align': 'center','font-size': '25px'})
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
        ],className='mt-2 mb-2')for i in range(len(prices))
    ]
    return cards
 


@app.callback(
    Output(component_id='nextGoldfigure',component_property='children'),
    Input(component_id='goldNext',component_property='children')
)
def nextDays(val):
    df=pd.read_csv('GOLDData.csv')
    predictions=md.marketGoldPre(df)
    predictions,showPre=md.predictClean(predictions)
    vals,showData=md.dataExt(df)
    figures=md.deltaGraphs(vals,predictions)
    prices=showPre
    figures=figures[:7]
    data=vals[7:]
    styles=[]
    for i in range(len(data)-1):
        if data[i]>data[i+1]:
            styles.append({'font-weight': 'bold','color':'red','text-align': 'center','font-size': '25px'})
        elif data[i]<data[i+1]:
            styles.append({'font-weight': 'bold','color':'green','text-align': 'center','font-size': '25px'})
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
        ],className='mt-2 mb-2')for i in range(len(prices))
    ]
    return cards
 


@app.callback(
    Output(component_id='opGld',component_property='children'),
    Output(component_id='bidGld',component_property='children'),
    Output(component_id='hiGld',component_property='children'),
    Output(component_id='lowGld',component_property='children'),
    Output(component_id='volGld',component_property='children'),
    Output(component_id='askGld',component_property='children'),
    Input(component_id='oMInterval',component_property='n_intervals'),
)
def goldCleanShow(val):
    dataList=md.goldScrap()
    data=md.cleanDataGold(dataList)
    print(data)
    return data[0],data[1],data[2],data[3],data[4],data[5]

@app.callback(
    Output(component_id='goldCurr',component_property='children'),
    Output(component_id='goldChange',component_property='children'),
    Output(component_id='goldChangePer',component_property='children'),
    Output(component_id='goldChange',component_property='style'),
    Output(component_id='goldChangePer',component_property='style'),
    Input(
        component_id='oMInterval',component_property='n_intervals',
    )
)
def valueOneM(val):
    values=md.oneMinuteGoldPrices()
    styleR={'font-size':'18px','font-weight': 'bold','text-align': 'right',
    'margin-top':'35px'}
    if '-' in values[1]:
        styleR['color']='red'
    else:
        styleR['color']='green'
    return values[0]+'$',values[1],values[2],styleR,styleR
