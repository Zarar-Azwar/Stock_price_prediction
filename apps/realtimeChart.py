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

companies=pd.read_csv('companies.csv')
df=pd.read_csv('complete_data.csv')
styleDrpdown={'border-radius': '18px','border-color':'#46AFC4','color':'#46AFC4'}
outlineClass=''
cardClass="shadow border border-primary mt-4 mt-2"
companies=companies.rename(columns={'Symbol':'SYMBOL'})
companiesDF=companies[['SYMBOL','Name']]
newDF=pd.merge(df,companiesDF,on='SYMBOL')
newDF.sort_values(by='Date',inplace=True,ascending=False)
df=newDF

cardClass="shadow border mt-2 mt-2"
styleHead={'color':'blue','font-size': '28px','color':'#0275D8'}#'backgroundColor': '#0275D8'
classHead='mt-2'
labels=[]
for i in range(len(companies)):
    labels.append({'value':companies['SYMBOL'][i],'label':companies['Name'][i]})
#df=df[:300][:]
menu=dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='demo-dropdown',
                options=labels,
                value='786',
                style=styleDrpdown
            ),
        ],width=5,className=outlineClass),
        dbc.Col([
            dbc.Checkbox(
                id='emaEnable',
                value=False,
                style=styleDrpdown
            )
        ],className='d-flex justify-content-center justify-content-sm-end mt-1'),
        dbc.Col([
            dcc.Dropdown(
                id='emaDropdown',
                options=[{'label':i,'value':i} for i in range(10,201)],
                multi=True,
                disabled=True,
                value=[20],
                placeholder="Select EMA",
                style=styleDrpdown
            )
        ],width=2,className=outlineClass),
        dbc.Col([
            dcc.Dropdown(
                id='indicators',
                options=[
                    {'label':'CHANNEL IDENTIFICATION','value':'channel'},
                    {'label':'ICHIMOKU CLOUD','value':'ichimoku'},
                    {'label':'BOLLINGER BAND','value':'bollinger'},
                    {'label':'RSI','value':'rsi'},
                    {'label':'MACD','value':'macd'},
                ],
                multi=True,
                placeholder="Select Indicators",
                value=[],
                style=styleDrpdown
                
            )
        ],width=4,className=outlineClass),

    ]),
    
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='chartType',
                options=[
                    {'label':'Candlestick','value':'candlestic'},
                    {'label':'HikenAshi','value':'heikenashi'},
                    {'label':'Line','value':'line'}
                ],
                multi=False,
                value='candlestic',
                style=styleDrpdown

            )
        ],width=3,className=outlineClass),
        dbc.Col([
            dcc.Dropdown(
                id='daysDropdown',
                options=[{'label':i,'value':i} for i in range(10,201)],
                multi=False,
                value=200,
                style=styleDrpdown
            )
        ],width=3,className=outlineClass),
        dbc.Col([
            dbc.Label('RSI Range',style={"justify":"center", "align":"center",
            'color':'#46AFC4'}, className="h-50")
        ],width=2,className='d-flex justify-content-center justify-content-sm-end mt-1'),
        dbc.Col([
            dcc.Dropdown(
                id='lowerDropdown',
                options=[{'label':i,'value':i} for i in range(10,50,10)],
                multi=False,
                value=10,
                style=styleDrpdown
            )
        ],width=2,className=outlineClass),
        dbc.Col([
            dcc.Dropdown(
                id='upperDropdown',
                options=[{'label':i,'value':i} for i in range(60,100,10)],
                multi=False,
                value=90,
                style=styleDrpdown
            )
        ],width=2,className=outlineClass)

    ],className='mt-2 mb-2'),  
    
])
layout=dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    menu
                ])
            ],className="mt-2 shadow")
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H5('OPEN',
                    style={'font-family': 'Arial','font-size': '18px','color':'#46AFC4','text-align': 'center'})
                ),
                dbc.CardBody([
                    html.H1(id='oID',
                          style={'font-family': 'Arial','font-size': '18px','text-align': 'center','fontWeight':'bold'})
                ])
            ],className=cardClass)
        ],width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H5('LOW',
                    style={'font-family': 'Arial','font-size': '18px','color':'#46AFC4','text-align': 'center'})
                
                ),
                dbc.CardBody([
                    html.H1(id='lID',
                          style={'font-family': 'Arial','font-size': '18px','text-align': 'center','fontWeight':'bold'})
                ])
            ],className=cardClass)
        ],width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H5('HIGH',
                    style={'font-family': 'Arial','font-size': '18px','color':'#46AFC4','text-align': 'center'})
                
                ),
                dbc.CardBody([
                    html.H1(id='hID',
                          style={'font-family': 'Arial','font-size': '18px','text-align': 'center','fontWeight':'bold'})
                ])
            ],className=cardClass)
        ],width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H5('CLOSE',
                    style={'font-family': 'Arial','font-size': '18px','color':'#46AFC4','text-align': 'center'})
                
                ),
                dbc.CardBody([
                    html.H1(id='cID',
                          style={'font-family': 'Arial','font-size': '18px','text-align': 'center','fontWeight':'bold'})
                ])
            ],className=cardClass)
        ],width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H5('VOLUME',
                    style={'font-family': 'Arial','font-size': '18px','color':'#46AFC4','text-align': 'center'})
                
                ),
                dbc.CardBody([
                    html.H2(id='vID',
                          style={'font-family': 'Arial','font-size': '18px','text-align': 'center','fontWeight':'bold'})
                ])
            ],className=cardClass)
        ],width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H5('LDCP',
                    style={'font-family': 'Arial','font-size': '18px','color':'#46AFC4','text-align': 'center'})
                
                ),
                dbc.CardBody([
                    html.H2(id='ldID',
                          style={'font-family': 'Arial','font-size': '18px','text-align': 'center','fontWeight':'bold'})
                ])
            ],className=cardClass)
        ],width=2)
    
    
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='candlesticks',
                figure={}
            )
        ],width=12)
    ]),

    html.Hr(),
    dbc.Row([
            html.H2('STRATEGIES')
    ]),
    dbc.Row([
        dbc.Col([
           dbc.Card([
               dbc.CardHeader(
                   html.H4('20 50 EMA',
                           style={'font-family': 'Arial','font-size': '14px','text-align': 'center'})
               ),
               dbc.CardBody([
                   html.H1(id='2050EMA',
                          style={'font-family': 'Arial','font-size': '18px','text-align': 'center','fontWeight':'bold'})
               ])
           ],className=cardClass)
        ]),
        dbc.Col([
            dbc.Card([
               dbc.CardHeader(
                   html.H4('20 200 EMA',
                           style={'font-family': 'Arial','font-size': '14px','text-align': 'center'})
               ),
               dbc.CardBody([
                   html.H1(id='20200EMA',
                          style={'font-family': 'Arial','font-size': '18px','text-align': 'center','fontWeight':'bold'})
               ])
           ],className=cardClass)
           
        ]),
        dbc.Col([
            dbc.Card([
               dbc.CardHeader(
                   html.H4('ICHIMOKU CLOUD',
                           style={'font-family': 'Arial','font-size': '14px','text-align': 'center'})
               ),
               dbc.CardBody([
                   html.H1(id='ichC',
                          style={'font-family': 'Arial','font-size': '18px','text-align': 'center','fontWeight':'bold'})
               ])
           ],className=cardClass)
           
        ]),
        dbc.Col([
            dbc.Card([
               dbc.CardHeader(
                   html.H4('MACD',
                           style={'font-family': 'Arial','font-size': '14px','text-align': 'center'})
                   
               ),
               dbc.CardBody([
                   html.H1(id='macdSB',
                          style={'font-family': 'Arial','font-size': '18px','text-align': 'center','fontWeight':'bold'})
               ])
           ],className=cardClass)
           
        ]),
        dbc.Col([
            dbc.Card([
               dbc.CardHeader(
                   html.H4('RSI',
                           style={'font-family': 'Arial','font-size': '14px','text-align': 'center'})
                   
               ),
               dbc.CardBody([
                   html.H1(id='rsiSB',
                           style={'font-family': 'Arial','font-size': '18px','text-align': 'center','fontWeight':'bold'})
               ])
           ],className=cardClass)
           
        ]),
        dbc.Col([
            dbc.Card([
               dbc.CardHeader(
                   html.H4('BOLLINGER BAND',
                           style={'font-family': 'Arial','font-size': '14px','text-align': 'center'})
                   
               ),
               dbc.CardBody([
                   html.H4(id='bollingerBand',
                           style={'font-family': 'Arial','font-size': '18px','text-align': 'center','fontWeight':'bold'})
               ])
            
           ],className=cardClass)
           
        ])
        
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Dropdown(
                        id='strategies-dropdown',
                        options=[
                            {'label':'20&50 Strategy','value':'strategy2050'},
                            {'label':'20&200 Strategy','value':'strategy20200'},
                            {'label':'Ichimoku Cloud Strategy','value':'ichimoku'},
                            {'label':'MACD Strategy','value':'macd'},
                            {'label':'RSI Strategy','value':'rsi'},
                            {'label':'Bollinger Band Strategy','value':'bollinger'},
                        ],
                        value='strategy2050',
                        multi=False,
                        style=styleDrpdown,
                    ),
    
                ])
            ],className="mt-2 shadow")
        ])
    ]),
   
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='strategyGraph',
                figure={}
            )
        ],width=12)
    ]),

    
],fluid=True)

@app.callback(
    [
        Output(component_id='2050EMA',component_property='children'),
        Output(component_id='20200EMA',component_property='children'),
        Output(component_id='ichC',component_property='children'),
        Output(component_id='macdSB',component_property='children'),
        Output(component_id='rsiSB',component_property='children'),
        Output(component_id='bollingerBand',component_property='children'),
    ],
    Input(component_id='demo-dropdown',component_property='value')
)
def updateBuySell(val):
    dff=df[df['SYMBOL']==val]
    dff=md.stockChange(dff)
    buySell=md.buySellReturn(dff)
    strategy=buySell[buySell.index==buySell.index.min()].values.tolist()[0]
    for i in range(len(strategy)):
        if strategy[i]=='':
            strategy[i]='NEUTRAL'
            
    return strategy[0],strategy[1],strategy[2],strategy[3],strategy[4],strategy[5]


@app.callback(
    [
        Output(component_id='oID',component_property='children'),
        Output(component_id='lID',component_property='children'),
        Output(component_id='hID',component_property='children'),
        Output(component_id='cID',component_property='children'),
        Output(component_id='vID',component_property='children'),
        Output(component_id='ldID',component_property='children'),
    ],
    Input(component_id='demo-dropdown',component_property='value')
)
def cardsupdate(compName):
    dff=df[df['SYMBOL']==compName]
    dff=md.stockChange(dff)
    dff=dff[dff.index==dff.index.max()]
    op="{:,}".format(dff['OPEN'][0])
    hi="{:,}".format(dff['HIGH'][0])
    lo="{:,}".format(dff['LOW'][0])
    cl="{:,}".format(dff['CLOSE'][0])
    vo="{:,}".format(dff['VOLUME'][0])
    ld="{:,}".format(dff['LDCP'][0])
    return op,hi,lo,cl,vo,ld
@app.callback(
    Output(component_id='emaDropdown',component_property='disabled'),
    Input(component_id='emaEnable',component_property='value')
)
def emaenable(val):
    if val==True:
        disabled=False
    else:
        disabled=True
    return disabled
@app.callback(
    
    Output(component_id='strategyGraph',component_property='figure'),
    [
        Input(component_id='demo-dropdown',component_property='value'),
        Input(component_id='strategies-dropdown',component_property='value'),
    ]
    
)
def strategyPlot(compName,value):
    dff=df[df['SYMBOL']==compName]
    dff=dff[:200][:]
    
    dff=md.stockChange(dff)
    dff=dff.loc[::-1]
    print(dff)
    #buySellCharts(df,emas,ichimoku,bollinger,macd,rsi)
    if value=='strategy2050':
        emas=[20,50]
        for ema in emas:
            dff=md.emaCalculator(dff,ema)
        dff=md.sellBuytwentyfifty(dff)
        fig=md.buySellCharts(dff,emas)
    elif value=='strategy20200':
        emas=[20,200]
        for ema in emas:
            dff=md.emaCalculator(dff,ema)
        dff=md.sellBuytwentyfifty(dff)
        fig=md.buySellCharts(dff,emas)
    elif value=='ichimoku':
        dff=md.ichimokuCloud(dff)
        dff=md.ichimokuCloudBuySell(dff)
        fig=md.buySellCharts(dff,ichimoku=True)
    elif value=='macd':
        dff=md.MACDcalculate(dff)
        dff=md.MACD_strategy(dff)
        fig=md.buySellCharts(dff,macd=True)
    elif value=='rsi':
        dff=md.RSIcalculator(dff)
        dff=md.RSI_strategy(dff)
        fig=md.buySellCharts(dff,rsi=True)
    elif value=='bollinger':
        dff=md.bollingerCalculate(dff)
        dff=md.bollingerStrategy(dff)
        fig=md.buySellCharts(dff,bollinger=True)
    

    return fig




@app.callback(
    Output(component_id='upperDropdown',component_property='value'),
    Input(component_id='lowerDropdown',component_property='value')
)
def rsiRange(val):
    return 100-val

@app.callback(
    Output(component_id='lowerDropdown',component_property='value'),
    Input(component_id='upperDropdown',component_property='value')
)
def rsiRange(val):
    return 100-val

@app.callback(
    Output(component_id='candlesticks',component_property='figure'),
    [
     Input(component_id='demo-dropdown',component_property='value'),
     Input(component_id='emaEnable',component_property='value'),
     Input(component_id='emaDropdown',component_property='value'),
     Input(component_id='indicators',component_property='value'),
     Input(component_id='lowerDropdown',component_property='value'),
     Input(component_id='upperDropdown',component_property='value'),
     Input(component_id='daysDropdown',component_property='value'),
     Input(component_id='chartType',component_property='value')
    ]
    
)
def candlesticChart(compName,emaEn,emaDrop,indicator,lv,uv,daysSel,chartType='candlestic'):
    dff=df[df['SYMBOL']==compName]
    dff=md.stockChange(dff)
    dff=dff[:daysSel][:]
    print(dff.index.max(),dff[:1].index.max())
    dff=dff.loc[::-1]
    if chartType=='heikenashi':
        dff=md.hikenAshiCandles(dff)
    emas=[]
    if emaEn==True:
        emas=emaDrop
    for ema in emas:
        dff=md.emaCalculator(dff,ema)
    chanal=False
    ichimoku=False
    bollinger=False
    rsi=False
    macd=False
    if 'channel' in indicator:
        dff=md.channelsIdentification(dff)
        chanal=True
    if 'ichimoku' in indicator:
        dff=md.ichimokuCloud(dff)
        ichimoku=True
    if 'bollinger' in indicator:
        dff=md.bollingerCalculate(dff)
        bollinger=True
    if 'rsi' in indicator:
        dff=md.RSIcalculator(dff,lv,uv)
        rsi=True
    if 'macd' in indicator:
        dff=md.MACDcalculate(dff)
        macd=True
    if chartType=='line':
        fig=md.lineCharts(dff,emas,chanal,ichimoku,bollinger,macd,rsi)
    else:
        fig=md.candleStickCharts(dff,emas,chanal,ichimoku,bollinger,macd,rsi)
    return fig

