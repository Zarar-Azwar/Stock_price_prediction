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
timeandDate=dbc.Container([
    dbc.Row([
            dbc.Col([
                #daq.LEDDisplay(value=datetime.datetime.now().strftime('%H:%M:%S'),size=12)
                html.H6(id='timeCurr',
                        style={'font-size': '20px','color':'#0275D8',
                        'font-family': 'Calibri, sans-serif','text-align': 'left'})
            ]),
            dbc.Col([
                html.H6(id='dateCurr',
                       style={'font-size': '20px','color':'#0275D8','font-family': 'Calibri, sans-serif','text-align': 'right'})
                #daq.LEDDisplay(value=datetime.datetime.now().strftime('%Y-%m-%d'),size=12)

            ])
        ],className="mt-3"),
        
])

index=dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H3('Indices',style=styleHead)
        ],className=classHead)
    ]),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H2(id='companyNameIndex',style={'font-weight': 'bold','color':'green',
                                    'font-size': '27px'})
                        ]),
                        dbc.Col([
                            html.H2(id='priceIDIndex',style={'font-size': '25px'})
                        ]),
                        dbc.Col([
                            dcc.Graph(id='index-graphIndex', figure={},config={'displayModeBar':False})
                        ]),
                        dbc.Col([
                            dbc.Row([
                                dbc.Col([
                                    html.H6('HIGH',style={'font-size': '15px'})
                                ]),
                                dbc.Col([
                                    html.H3(id='highValIndex',style={'font-size': '20px'})
                                ])
                            ])
                        ]),
                        dbc.Col([
                            dbc.Row([
                                dbc.Col([
                                    html.H6('LOW',style={'font-size': '15px'})
                                ]),
                                dbc.Col([
                                    html.H3(id='lowValIndex',style={'font-size': '20px'})
                                ])
                            ])
                        ]),
                        dbc.Col([
                            dbc.Row([
                                dbc.Col([
                                    html.H6('LDCP',style={'font-size': '15px'})
                                ]),
                                dbc.Col([
                                    html.H3(id='ldcpValIndex',style={'font-size': '20px'})
                                ])
                            ])
                        ]),
                        dbc.Col([
                            dbc.Row([
                                dbc.Col([
                                    html.H6('VOLUME',style={'font-size': '15px'})
                                ]),
                                dbc.Col([
                                    html.H3(id='volValIndex',style={'font-size': '20px'})
                                ])
                            ])
                        ]),
                        
                        
                    
                    ])
                ])
            ],className=cardClass)
        )
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dash_table.DataTable(
                    id='indicesTable',
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
                        
                    ])
                )
        
            ],className=cardClass)
        ])
    ],className='mt-2 mb-2'),
    
])

summry=dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H3('Exchange',id='exchange',style=styleHead)
        ],className=classHead)
    ]),
    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H3('State',style={'font-weight': 'bold','color':'green',
                                            'font-size': '17px'}),
                    html.H3(id='StateVal',style={'color':'black','font-size': '17px'}),
                ],width=3,className=''),
                dbc.Col([
                    html.H3('Volume',style={'font-weight': 'bold','color':'green',
                                            'font-size': '17px'}),
                    html.H3(id='VolmVal',style={'color':'black','font-size': '17px'}),
                ],width=3,className=''),
                dbc.Col([
                    html.H3('Value',style={'font-weight': 'bold','color':'green',
                                            'font-size': '17px'}),
                    html.H3(id='ValVal',style={'color':'black','font-size': '17px'}),
                ],width=3,className=''),
                dbc.Col([
                    html.H3('Trades',style={'font-weight': 'bold','color':'green',
                                            'font-size': '17px'}),
                    html.H3(id='tradesVal',style={'color':'black','font-size': '17px'}),
                ],width=3,className=''),
            ]),
    

        ])
    ],className=cardClass),
    dbc.Row([
        dbc.Col([
            html.H3('Symbol',id='symbol',style=styleHead)
        ],className=classHead)
    ]),
    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H3('Advanced',style={'font-weight': 'bold','color':'green',
                                            'font-size': '17px'}),
                            html.H3(id='advancedVal',style={'color':'green','font-size': '17px'}),
                ],width=3,className=''),
                dbc.Col([
                    html.H3('Declined',style={'font-weight': 'bold','color':'red',
                                            'font-size': '17px'}),
                    html.H3(id='declinedVal',style={'color':'red','font-size': '17px'}),
                ],width=3,className=''),
                dbc.Col([
                    html.H3('Unchanged',style={'font-weight': 'bold','color':'blue',
                                            'font-size': '17px'}),
                    html.H3(id='unchangedVal',style={'color':'blue','font-size': '17px'}),
                ],width=3,className=''),
                dbc.Col([
                    html.H3('Total',style={'font-weight': 'bold','color':'black',
                                            'font-size': '17px'}),
                    html.H3(id='totalVal',style={'color':'black','font-size': '17px'}),
                ],width=3,className=''),
            ]),
            
        ])
    ],className=cardClass),
],className='mt-2 mb-2')   

performer=dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('Market Performers',style=styleHead)
        ],className=classHead)
    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.Row([
                   dbc.Col([
                       html.H3('TOP ACTIVE STOCKS',id='topActive',
                               style={'font-size':'17px','font-weight': 'bold','text-align': 'center'})
                   ]) 
                ]),
                dbc.Row([
                    dbc.Col([
                        dash_table.DataTable(
                            id='topActiveStocks',
                            
                            style_as_list_view=True,
                            style_cell={'padding': '2px','font-family': 'Arial','font-size': '14px','text-align': 'center'},
                            style_header={
                                'backgroundColor': 'white',
                                'fontWeight': 'bold',
                                'text-align': 'center'
                            },
                            style_data_conditional=([
                                {
                                    'if':{
                                        'filter_query':'{CHANGE} < 0'
                                    },
                                    'color': 'red'
                                },
                                {
                                    'if':{
                                        'filter_query':'{CHANGE} > 0'
                                    },
                                    'color': 'green'
                                },
                                {
                                    'if':{
                                        'filter_query':'{CHANGE} = 0'
                                    },
                                    'color': 'blue'
                                },
                            ])
                        )
                    ])
                ]),
            ],className=cardClass)
        ]),
        dbc.Col([
            dbc.Card([
                dbc.Row([
                   dbc.Col([
                       html.H3('TOP DECLINER',id='topAdvancers',
                               style={'font-size':'17px','font-weight': 'bold','text-align': 'center'})
                   ]) 
                ]),
                dbc.Row([
                    dbc.Col([
                        dash_table.DataTable(
                            id='topAdvancersStocks',
                            style_as_list_view=True,
                            style_cell={'padding': '2px','font-family': 'Arial','font-size':'14px','text-align': 'center'},
                            style_header={
                                'backgroundColor': 'white',
                                'fontWeight': 'bold',
                                'text-align': 'center'
                            },
                            style_data_conditional=([
                                {
                                    'if':{
                                        'filter_query':'{CHANGE} < 0'
                                    },
                                    'color': 'red'
                                },
                                {
                                    'if':{
                                        'filter_query':'{CHANGE} > 0'
                                    },
                                    'color': 'green'
                                },
                                {
                                    'if':{
                                        'filter_query':'{CHANGE} = 0'
                                    },
                                    'color': 'blue'
                                },
                            ])
                        )
                    ])
                ]),
            ],className=cardClass)
        ]),
        dbc.Col([
            dbc.Card([
                dbc.Row([
                   dbc.Col([
                       html.H3('TOP ADVANCER',id='topDecliner',
                               style={'font-size':'17px','font-weight': 'bold','text-align': 'center'})
                   ]) 
                ]),
                dbc.Row([
                    dbc.Col([
                        dash_table.DataTable(
                            id='topDeclinersStocks',
                            style_as_list_view=True,
                            style_cell={'padding': '2px','font-family': 'Arial','font-size': '14px','text-align': 'center'},
                            style_header={
                                'backgroundColor': 'white',
                                'fontWeight': 'bold',
                                'text-align': 'center'
                            },
                            style_data_conditional=([
                                {
                                    'if':{
                                        'filter_query':'{CHANGE} < 0'
                                    },
                                    'color': 'red'
                                },
                                {
                                    'if':{
                                        'filter_query':'{CHANGE} > 0'
                                    },
                                    'color': 'green'
                                },
                                {
                                    'if':{
                                        'filter_query':'{CHANGE} = 0'
                                    },
                                    'color': 'blue'
                                },
                            ])
                        )
                    ])
                ]),
            ],className=cardClass)
        ])
    ]),
    
],fluid=True)
table=dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H3('Market Watch',style=styleHead)
        ],className=classHead),
        dbc.Col([
                dbc.Button(html.Span([html.I(className='fas fa-arrow-circle-down')]),id='downloadBut',
                className='rounded-circle btn-primary mt-2'),
                dcc.Download(id='downloadOp')
        ],className='d-flex justify-content-end')
    ],className='mb-2 mt-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dash_table.DataTable(
                    id='oneMinuteTable',
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
                                'filter_query':'{CHANGE} < 0'
                            },
                            'color': 'red'
                        },
                        {
                            'if':{
                                'filter_query':'{CHANGE} > 0'
                            },
                            'color': 'green'
                        },
                        {
                            'if':{
                                'filter_query':'{CHANGE} = 0'
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
            
            ],className=cardClass),
        ],className='mb-5')
    ])
],fluid=True)
interval=html.Div([
    dcc.Interval(id='oneMinuteInterval',interval=60000,n_intervals=0)
])
interval1=html.Div([
    dcc.Interval(id='fiveSecInterval',interval=4000)
])

layout=dbc.Container([timeandDate,summry,index,performer,interval,interval1,table],fluid=True)

@app.callback(
    Output(component_id='indicesTable',component_property='columns'),
    Output(component_id='indicesTable',component_property='data'),
    Input(component_id='oneMinuteInterval',component_property='n_intervals')
)
def indexTable(val):
    ind,heading=md.indicesFun()
    dataframe=md.indecesDf(ind,heading)
    cols=[{'name':i,'id':i} for i in dataframe.columns]
    data=dataframe.to_dict('records')
    #print(cols)
    return cols,data

@app.callback(
    Output(component_id='timeCurr',component_property='children'),
    Output(component_id='dateCurr',component_property='children'),
    Input(component_id='oneMinuteInterval',component_property='n_intervals')
)
def timeUpdates(val):
    t=datetime.now().strftime('%H:%M:%S')
    d=datetime.now().strftime('%Y-%m-%d')
    return t,d

@app.callback(
    Output(component_id='companyNameIndex',component_property='children'),
    Output(component_id='priceIDIndex',component_property='children'),
    Output(component_id='index-graphIndex',component_property='figure'),
    Output(component_id='highValIndex',component_property='children'),
    Output(component_id='lowValIndex',component_property='children'),
    Output(component_id='ldcpValIndex',component_property='children'),
    Output(component_id='volValIndex',component_property='children'),
    Input(component_id='fiveSecInterval',component_property='n_intervals')
)
def indexFun(val):
    val=int(0 if val is None else val)
    indexNames=['KSE100','ALLSHR','KSE30','KMI30','BKTi','OGTi',
         'KMIALLSHR','UPP9','NITPGI','NBPPGI','MZNPI','JSMFI','ACI']
    rem=val%13
    ind,heading=md.indicesFun()
    kse100val=heading[rem][0]
    ksehigh=ind[rem][0]
    kselow=ind[rem][1]
    ksevol=ind[rem][2]
    kseldcp=ind[rem][5]
    
    kseInd=float(kse100val.replace(',',''))
    ldcpInd=float(kseldcp.replace(',',''))
    
    fig = go.Figure(go.Indicator(
        mode="delta",
        value=kseInd,
        delta={'reference': ldcpInd,'relative': True, 'valueformat':'.2%'}))
    fig.update_traces(delta_font={'size':16})
    fig.update_layout(height=30, width=90)

    if kseInd >= ldcpInd:
        fig.update_traces(delta_increasing_color='green')
    elif kseInd < ldcpInd:
        fig.update_traces(delta_decreasing_color='red')
    print(indexNames[rem],kseInd)
    return indexNames[rem],kse100val,fig,ksehigh,kselow,ldcpInd,ksevol

@app.callback(
    [
        Output(component_id='StateVal',component_property='children'),
        Output(component_id='VolmVal',component_property='children'),
        Output(component_id='ValVal',component_property='children'),
        Output(component_id='tradesVal',component_property='children'),
        Output(component_id='advancedVal',component_property='children'),
        Output(component_id='declinedVal',component_property='children'),
        Output(component_id='unchangedVal',component_property='children'),
        Output(component_id='totalVal',component_property='children')
    ],
    Input(component_id='oneMinuteInterval',component_property='n_intervals')
)
def exchange(inter):
    mSVal=md.marketSummary()
    vals=[]
    for i in range(len(mSVal)):
        vals.append(mSVal[i][1])
    return vals[0],vals[1],vals[2],vals[3],vals[4],vals[5],vals[6],vals[7]
@app.callback(
    Output(component_id='downloadOp',component_property='data'),
    Input(component_id='downloadBut',component_property='n_clicks'),
    prevent_initial_call=True,
)
def download(click):
    if click > 0:
        data=md.dataScrapMinute()
        return dcc.send_data_frame(data.to_csv,"data.csv")
@app.callback(
    Output(component_id='oneMinuteTable',component_property='columns'),
    Output(component_id='oneMinuteTable',component_property='data'),
    Input(component_id='oneMinuteInterval',component_property='n_intervals')
)
def datashow(interval):
    try:
        df=md.dataScrapMinute()
    except:
        print('a')
    dff=df[['SCRIP','LDCP','OPEN','HIGH','LOW','CURRENT','CHANGE','VOLUME']]
    cols=[{'name':i,'id':i} for i in dff.columns]
    dataD=dff.to_dict('records')
    return cols,dataD

        
@app.callback(
    [Output(component_id='topActiveStocks',component_property='data'),
    Output(component_id='topActiveStocks',component_property='columns'),
    Output(component_id='topAdvancersStocks',component_property='data'),
    Output(component_id='topAdvancersStocks',component_property='columns'),
    Output(component_id='topDeclinersStocks',component_property='data'),
    Output(component_id='topDeclinersStocks',component_property='columns')],
    Input(component_id='oneMinuteInterval',component_property='n_intervals')
)
def table(val):
    df=md.dataScrapMinute()
    df=md.stockChangeTop(df)
    volm,lChang,hChang=md.topPerformers(df)
    volmT=volm[['SCRIP','CLOSE','CHANGE','VOLUME']]
    cols=[{"name": i, "id": i} for i in volmT.columns]
    volmD=volmT.to_dict('records')
    lChangT=lChang[['SCRIP','CLOSE','CHANGE','VOLUME']]
    cols=[{"name": i, "id": i} for i in lChangT.columns]
    lChangD=lChangT.to_dict('records')
    hChangT=hChang[['SCRIP','CLOSE','CHANGE','VOLUME']]
    cols=[{"name": i, "id": i} for i in hChangT.columns]
    hChangD=hChangT.to_dict('records')
    return volmD,cols,lChangD,cols,hChangD,cols

#****************************************IndicesCallback**********************************************


if __name__ == "__main__":
    app.run_server()
