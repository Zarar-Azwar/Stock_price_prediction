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
        dcc.Interval(id='oMGInterval',interval=60000,n_intervals=0)
    ]),
    html.Div([
        dcc.Interval(id='oDGInterval',interval=86400000,n_intervals=0)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.Row([
                    dbc.Col([
                        html.Img(src=app.get_asset_url('oilImg.png'),
                        style={'width': '130px','height':'130px','radius':'8px','margin-left':'15px',
                        'margin-right':'5px','margin-top':'15px','margin-bottom':'15px'})
                    ],className='mr-auto',width=2),
                    dbc.Col([
                        html.H1('Crude Oil Jun 22 (CL=F)',
                            style={'font-size':'25px','font-weight': 'bold','text-align': 'left',
                            'margin-top':'15px'}),
                        html.H5('NY Mercantile - NY Mercantile Delayed Price. Currency in USD',
                            style={'font-size':'12px','text-align': 'left','color':'#A0A0A0'})
                    ],className='mr-auto',width=5),
                    dbc.Col([
                        dbc.Row([
                            dbc.Col([
                                html.H3(id='oilCurr',
                                    style={'font-size':'30px','font-weight': 'bold','text-align': 'center',
                                    'margin-left':'25px',
                                'margin-top':'25px','margin-bottom':'25px'})
                            ],width=5),
                            dbc.Col([
                                html.H5(id='oilChange')
                            ],width=3),
                            dbc.Col([
                                html.H5(id='oilChangePer'),
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
                   html.H1(id='opOl',
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
                   html.H1(id='bidOl',
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
                   html.H1(id='hiOl',
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
                   html.H1(id='lowOl',
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
                   html.H1(id='volOl',
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
                   html.H4(id='askOl',
                           style={'font-family': 'Arial','font-size': '18px','text-align': 'center','fontWeight':'bold'})
               ])
            
           ],className=cardClass)
           
        ])
        
    
    ],className='mb-2 mt-2 d-flex align-items-center justify-content-center'),


    dbc.Row([
        dbc.Col([
            html.H3('Previous 7 Days',id='oilID',style=styleHead)
        ],className='mb-2 mt-2')
    ]),
    dbc.Row(
        id='previousoilfigure'
    ),
    dbc.Row([
        dbc.Col([
            html.H3('Next 7 Days Predictions',id='oilNext',style=styleHead)
        ],className='mb-2 mt-2')
    ]),
    dbc.Row(
        id='nextoilfigure'
    ),
    dbc.Row([
        dbc.Col([
            html.H3('Market Watch',style=styleHead)
        ],className=classHead),
        dbc.Col([
                dbc.Button(html.Span([html.I(className='fas fa-arrow-circle-down')]),id='downloadOlBut',
                className='rounded-circle btn-primary mt-2'),
                dcc.Download(id='downloadoilOp')
        ],className='d-flex justify-content-end')
    ],className='mb-2 mt-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dash_table.DataTable(
                    id='oneMinuteoilTable',
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
    Output(component_id='downloadoilOp',component_property='data'),
    Input(component_id='downloadOlBut',component_property='n_clicks'),
    prevent_initial_call=True,
)
def download(click):
    if click > 0:
        data=md.dataScrapMinute()
        return dcc.send_data_frame(data.to_csv,"data.csv")
@app.callback(
    Output(component_id='oneMinuteoilTable',component_property='columns'),
    Output(component_id='oneMinuteoilTable',component_property='data'),
    Input(component_id='oDGInterval',component_property='n_intervals')
)
def datashow(interval):
    df=pd.read_csv('OilData.csv')
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
    Output(component_id='previousoilfigure',component_property='children'),
    Input(component_id='oilID',component_property='children')
)
def previousDays(val):
    df=pd.read_csv('OilData.csv')
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
    Output(component_id='nextoilfigure',component_property='children'),
    Input(component_id='oilNext',component_property='children')
)
def nextDays(val):
    df=pd.read_csv('OilData.csv')
    predictions=md.marketOilPre(df)
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
    Output(component_id='opOl',component_property='children'),
    Output(component_id='bidOl',component_property='children'),
    Output(component_id='hiOl',component_property='children'),
    Output(component_id='lowOl',component_property='children'),
    Output(component_id='volOl',component_property='children'),
    Output(component_id='askOl',component_property='children'),
    Input(component_id='oMGInterval',component_property='n_intervals'),
)
def goldCleanShow(val):
    dataList=md.oilScrap()
    data=md.cleanDataGold(dataList)
    print(data)
    return data[0],data[1],data[2],data[3],data[4],data[5]

@app.callback(
    Output(component_id='oilCurr',component_property='children'),
    Output(component_id='oilChange',component_property='children'),
    Output(component_id='oilChangePer',component_property='children'),
    Output(component_id='oilChange',component_property='style'),
    Output(component_id='oilChangePer',component_property='style'),
    Input(
        component_id='oMGInterval',component_property='n_intervals',
    )
)
def valueOneM(val):
    values=md.oneMinuteOilPrices()
    styleR={'font-size':'18px','font-weight': 'bold','text-align': 'right',
    'margin-top':'35px'}
    if '-' in values[1]:
        styleR['color']='red'
    else:
        styleR['color']='green'
    return values[0]+'$',values[1],values[2],styleR,styleR
