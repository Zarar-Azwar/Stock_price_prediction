import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from collections import OrderedDict
import calendar
from datetime import datetime,date,time
import pytz
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime
import calendar
import os
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
#from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential,load_model
from tensorflow.keras.layers import Dense,LSTM,Dropout
from sklearn.preprocessing import MinMaxScaler
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import objective_functions
from pypfopt.discrete_allocation import DiscreteAllocation,get_latest_prices

pd.options.mode.chained_assignment = None

def stockChange(df):
    df.set_index(df.Date,inplace=True)
    df.sort_index(ascending=False,inplace=True)
    dfs=df[['LDCP','OPEN','HIGH','LOW','CLOSE','CHANGE','VOLUME']]
    d=dfs
    for column in dfs.columns:
        if column =='CHANGE':
            d[column]=pd.to_numeric(dfs[column])
        else:
          try:
            op=dfs[column].tolist()
            opn=[]
            for i in op:
                opn.append(float(i.replace(',','')))
            d[column]=opn
          except:
            print(i,column)
    
    return d

def indecesDf(a,b):
    indexes=['KSE100','ALLSHR','KSE30','KMI30',
    'BKTi','OGTi','KMIALLSHR','UPP9','NITPGI','NBPPGI','MZNPI','JSMFI','ACI']
    closes=[]
    changes=[]
    lows=[]
    highs=[]
    volums=[]
    ldcps=[]
    for i in range(len(b)):
        closes.append(b[i][0])
        changes.append(float(b[i][1]))
        lows.append(a[i][0])
        highs.append(a[i][1])
        volums.append(a[i][2])
        ldcps.append(a[i][5])
    data=[]
    d=[indexes,closes,lows,highs,volums,ldcps,changes]
    c=['Name','Close','Low','High','volume','LDCP','Change']
    dataframe=pd.DataFrame(d).T
    dataframe.columns=c
    return dataframe

def sectorDataScrap():
    url='https://dps.psx.com.pk/sector-summary/sectorwise'
    response=requests.get(url)
    if(response.status_code==200):
        soup=BeautifulSoup(response.text,'html.parser')
        tables=soup.find_all('table',{'class':'tbl'})
        dataList=[]
        for tab in tables:
            for data in tab.find_all('td'):
                dataList.append(data.text)
        dataTable=[dataList[i:i+9] for i in range(0,len(dataList),9)]
        dataTable=dataTable[:36]
        df=pd.DataFrame(dataTable,
                    columns=['Sector Code','Sector Name','Advance','Decline','Unchange','Open','Current','Change','Turnover'])
        return df

def sectorDataCleaning(df):
    df['Advance']=pd.to_numeric(df['Advance'])
    df['Decline']=pd.to_numeric(df['Decline'])
    df['Unchange']=pd.to_numeric(df['Unchange'])
    cols=['Open','Current','Change','Turnover']
    for col in cols:
        c=df[col].tolist()
        temp=[]
        for i in c:
            temp.append(float(i.replace(',','')))
        df[col]=temp
    return df

def indicesFun():
    url='https://dps.psx.com.pk/'
    response=requests.get(url)
    if response.status_code==200:
        soup=BeautifulSoup(response.text,'html.parser')
        indeces=soup.find_all('div',{'class','marketIndices__details'})
        currVal=[]
        statVal=[]
        for ind in indeces:
            for i in ind.find_all('h1'):
                currVal.append(i.text)
            for j in ind.find_all('div',{'class','stats_value'}):
                statVal.append(j.text)
        headingVal=[]
        for val in currVal:
            headingVal.append(val.split(' '))
        stats=[]
        for val in statVal:
            v=val.split('\n')
            stats.append(v[0]) 
        statValues=[stats[i:i+8] for i in range(0,len(stats),8)]
        lstat=[]
        for statval in statValues:
            lstat.append(statval[:6])
        return lstat,headingVal
    else:
        return 0

def oneDay(df,date):
    df.set_index(df.Date,inplace=True)
    df=df[df['Date']==date]
    cols=['SYMBOL','LDCP','OPEN','HIGH','LOW','CLOSE','CHANGE','VOLUME']
    dff=df[cols]
    d=dff
    for column in dff.columns:
        if column=='SYMBOL':
            continue
        elif column =='CHANGE':
            d[column]=pd.to_numeric(dff[column])
        else:
            try:
                op=dff[column].tolist()
                opn=[]
                for i in op:
                    opn.append(float(i.replace(',','')))
                d[column]=opn
            except:
                print(i,column)
    return d

def stockChangeTop(df):
    df.set_index(df.Date,inplace=True)
    df.sort_index(ascending=False,inplace=True)
    df.rename(columns={'CURRENT':'CLOSE'},inplace=True)
    dfs=df[['SCRIP','LDCP','OPEN','HIGH','LOW','CLOSE','CHANGE','VOLUME']]
    d=dfs
    for column in dfs.columns:
        if column =='CHANGE':
            d[column]=pd.to_numeric(dfs[column])
        else:
            try:
                op=dfs[column].tolist()
                opn=[]
                for i in op:
                    opn.append(float(i.replace(',','')))
                d[column]=opn
            except:
                print(i,column)
    
    return d
def topPerformers(df):
    dfVol=df[['SCRIP','CLOSE','CHANGE','LDCP','VOLUME']]
    VolSorted=dfVol.sort_values(['VOLUME','SCRIP','LDCP','CLOSE','CHANGE'],ascending=False)
    volm=VolSorted[:5]
    lowSorted=dfVol.sort_values(['CHANGE','SCRIP','LDCP','CLOSE','VOLUME'],ascending=True)
    lChang=lowSorted[:5]
    highSorted=dfVol.sort_values(['CHANGE','SCRIP','LDCP','CLOSE','VOLUME'],ascending=False)
    hChang=highSorted[:5]
    return volm,lChang,hChang

def lineReturn(d):
    fig = px.line(d, x=d.index, y='CLOSE',
                   range_y=[d['CLOSE'].min(), d['CLOSE'].max()],
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

    day_start = d[d.index == d.index.max()]['LDCP'].values[0]
    day_end = d[d.index == d.index.max()]['CLOSE'].values[0]

    if day_end > day_start:
        return fig.update_traces(fill='tozeroy',line={'color':'green'})
    elif day_end < day_start:
        return fig.update_traces(fill='tozeroy',line={'color': 'red'})
    else:
        return fig.update_traces(fill='tozeroy',line={'color': 'blue'})

def deltaGraph(d):
    day_start = float(d['LDCP'][0])
    day_end = float(d['CLOSE'][0])
    fig = go.Figure(go.Indicator(
        mode="delta",
        value=day_end,
        delta={'reference': day_start, 'relative': True, 'valueformat':'.2%'}))
    fig.update_traces(delta_font={'size':13})
    fig.update_layout(height=25, width=120)

    if day_end >= day_start:
        fig.update_traces(delta_increasing_color='green')
    elif day_end < day_start:
        fig.update_traces(delta_decreasing_color='red')
    return fig

def buySellReturn(df):
    sb2050=sellBuytwentyfifty(df)
    df=df[['LDCP','OPEN','HIGH','LOW','CLOSE','CHANGE','VOLUME']]
    sb20200=sellBuytwentytwoHundred(df)
    df=df[['LDCP','OPEN','HIGH','LOW','CLOSE','CHANGE','VOLUME']]
    dfich=ichimokuCloud(df)
    bsich=ichimokuCloudBuySell(dfich)
    df=df[['LDCP','OPEN','HIGH','LOW','CLOSE','CHANGE','VOLUME']]
    dfmacd=MACDcalculate(df)
    bsmacd=MACD_strategy(dfmacd)
    df=df[['LDCP','OPEN','HIGH','LOW','CLOSE','CHANGE','VOLUME']]
    dfrsi=RSIcalculator(df)
    bsrsi=RSI_strategy(dfrsi)
    df=df[['LDCP','OPEN','HIGH','LOW','CLOSE','CHANGE','VOLUME']]
    dfboll=bollingerCalculate(df)
    bsboll=bollingerStrategy(dfboll)
    df=df[['LDCP','OPEN','HIGH','LOW','CLOSE','CHANGE','VOLUME']]
    buySell=pd.DataFrame()
    buySell['Action2050']=sb2050['Action'].tolist()
    buySell['Action20200']=sb20200['Action'].tolist()
    buySell['ActionIch']=bsich['Action'].tolist()
    buySell['ActionMacd']=bsmacd['Action'].tolist()
    buySell['ActionRSI']=bsrsi['Action'].tolist()
    buySell['ActionBoll']=bsboll['Action'].tolist()
    buySell.index=df.index
    return buySell

def dataScrapMinute():
    url='https://www.psx.com.pk/market-summary/'
    #cafile = 'cacert.pem'
    page=requests.get(url)
    soup=BeautifulSoup(page.text)
    tables=soup.find_all('div',{'class':"table-responsive"})
    stockData=[]
    for table in tables[2:]:
        for i in table.find_all('td'):
            stockData.append(i.text)
    companies= [stockData[x:x+8] for x in range(0, len(stockData),8)]
    df=pd.DataFrame(companies)
    df.drop_duplicates(keep='first',inplace=True)
    df.reset_index(inplace=True)
    df.columns=df.iloc[0]
    df.drop(df.index[0],inplace=True)
    df['Date']=date.today()
    df['Time']=datetime.now(pytz.timezone('Asia/Karachi')).time().strftime('%H:%M:%S')
    return df

def deltaIndicator(daySum):
  day_start = daySum['LDCP'][0]
  day_end = daySum['CLOSE'][0]
  fig = go.Figure(go.Indicator(
      mode="delta",
      value=day_end,
      delta={'reference': day_start, 'relative': True, 'valueformat':'.2%'}))
  fig.update_traces(delta_font={'size':20})
  fig.update_layout(height=40, width=150)

  if day_end >= day_start:
      fig.update_traces(delta_increasing_color='green')
  elif day_end < day_start:
      fig.update_traces(delta_decreasing_color='red')

  return fig


def emaCalculator(df,days):
  df[str(days)]=df['CLOSE'].ewm(span=days).mean()
  return df

def candlestick(df):
    figure=make_subplots(rows=2, cols=1, shared_xaxes=True)
    figure.add_trace(
        go.Candlestick(
            x=df.index,
            open=df.OPEN,
            high=df.HIGH,
            close=df.CLOSE,
            low=df.LOW,
            increasing_line_color='GREEN',
            decreasing_line_color='RED'
        ),row=1,col=1
    )
    figure.add_trace(
        go.Bar(
            x=df.index,
            y=df.VOLUME
        ),row=2,col=1
    )

def candleStickCharts(df,emas,chanal,ichimoku,bollinger,macd,rsi):
    Rows=2
    row_height=[0.8,0.2]
    heightG=500
    rsiRow=3
    macdRow=3
    if macd ==True and rsi==True:
        Rows=4
        macdRow=4
        row_height=[0.4,0.2,0.2,0.2]
        heightG=1000
    elif macd==True or rsi==True:
        Rows=3
        row_height=[0.5,0.2,0.3]
        heightG=800
    figure=make_subplots(rows=Rows, cols=1, shared_xaxes=True,vertical_spacing=0.01,row_heights=row_height)

    figure.add_trace(
        go.Candlestick(
            x=df.index,
            open=df.OPEN,
            high=df.HIGH,
            close=df.CLOSE,
            low=df.LOW,
            #increasing_line_color='GREEN',
            #increasing_line_width=0.8
            #decreasing_line_color='RED'
        ),row=1,col=1
    )
    colors = ['green' if row['OPEN'] - row['CLOSE'] >= 0 
          else 'red' for index, row in df.iterrows()]
    figure.add_trace(
        go.Bar(
            x=df.index,
            y=df.VOLUME,
            marker_color=colors
        ),row=2,col=1
    )
    for ema in emas:
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df[str(ema)],
                
                #line=dict(color=emas),
                name=str(ema)+ 'days EMA'
            ),row=1,col=1
        )
    
    if chanal==True:
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['Lval'],
                line=dict(color='#F0E68C'),
                name='Support'
            ),row=1,col=1
        )
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['Uval'],
                line=dict(color='#F0E68C'),
                fill='tonexty',
                fillcolor='rgba(240,230,140,0.2)',
                name='Resistance'
            ),row=1,col=1
        )

    if ichimoku==True:
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['BaseLine'],
                line=dict(width=1,color='#FFA500'),
                name='Base Line'
            ),row=1,col=1
        )
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['LeadingSpanA'],
                
                line=dict(width=1,color='#006400'),
                name='Leading Span A'
            ),row=1,col=1
        )
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['LeadingSpanB'],
                line=dict(width=1,color='#FF0000'),
                name='Leading Span B',
                fill='tonexty',
                fillcolor='rgba(00,64,00,0.5)',
                opacity=0.1
            ),row=1,col=1
        )
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['LaggingSpan'],
                line=dict(width=1,color='#90ee90'),
                name='Lagging Span'
            ),row=1,col=1
        )
    if bollinger==True:
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['UPPER'],
                line=dict(width=1,color='#2196F3'),
                name='UPPER'
            ),row=1,col=1
        )
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['LOWER'],
                line=dict(width=1,color='#2196F3'),
                name='LOWER',
                fill='tonexty',
                fillcolor='rgba(33,150,243,0.3)',
                opacity=0.1
            ),row=1,col=1
        )
    
    if macd==True:
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['Signal'],
                line=dict(color='#0000ff', width=1),
                legendgroup='2',
                name='signal'
            ), row=macdRow, col=1
        )
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['MACD'],
                line=dict(color='#00ff00', width=1),
                legendgroup='2',
                name='MACD'
            ), row=macdRow, col=1
        )
        colors = np.where(df['MACD_Hist'] < 0, '#FF0000', '#00FF00')
        # Plot the histogram
        figure.add_trace(
            go.Bar(
                x=df.index,
                y=df['MACD_Hist'],
                marker_color=colors,
            ), row=macdRow, col=1
        )
    
    if rsi==True:
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['RSI'],
                line=dict(color='#00ff00', width=1),
                name='RSI',
                # showlegend=False,
                legendgroup='1',
            ), row=rsiRow, col=1
        )
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['y1'],
                line=dict(color='#ff0000', width=1),
                name='Lower 20',
                # showlegend=False,
                legendgroup='1',
            ), row=rsiRow, col=1
        )
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['y2'],
                line=dict(color='#ff0000', width=1),
                name='Higher 80',
                # showlegend=False,
                legendgroup='1',
            ), row=rsiRow, col=1
        )
    figure.update_traces(increasing_fillcolor='green',increasing_line_color='green', 
                     decreasing_line_color='red',
                     selector=dict(type='candlestick'),increasing_line_width=1,decreasing_line_width=0.8,
                 decreasing_fillcolor='red')
    figure.layout.xaxis.type='category'
    figure.update_layout( 
        xaxis_rangeslider_visible=False,
        height=heightG,
    )
    
    return figure
  

    
    
######################### BUY SELL #########################
def sellBuytwentyfifty(df):
    df['20_EMA'] = df['CLOSE'].ewm(span = 20, adjust = False).mean()
    df['50_EMA'] = df['CLOSE'].ewm(span = 50, adjust = False).mean()
    #dfT=df
    df['Action']=''
    for i in range(len(df)):
        if (df['CLOSE'][i]>=df['20_EMA'][i]) and (df['20_EMA'][i]>=df['50_EMA'][i]):
            df['Action'][i]='BUY'
        else:
            df['Action'][i]='SELL'
    df['Sell']=0.0
    df['Buy']=0.0
    
    for i in range(1,len(df)):
        if df['Action'][i]=='SELL':
            df['Sell'][i]=df['CLOSE'][i]
        elif df['Action'][i]=='BUY':
            df['Buy'][i]=df['CLOSE'][i]
    return df

def sellBuytwentytwoHundred(df):
    df['20_EMA'] = df['CLOSE'].ewm(span = 20, adjust = False).mean()
    df['200_EMA'] = df['CLOSE'].ewm(span = 200, adjust = False).mean()
    df['Action']=''
    for i in range(len(df)):
        if (df['CLOSE'][i]>=df['20_EMA'][i]) and (df['20_EMA'][i]>=df['200_EMA'][i]):
            df['Action'][i]='BUY'
        else:
            df['Action'][i]='SELL'
    df['Sell']=0.0
    df['Buy']=0.0
    
    for i in range(1,len(df)):
        if df['Action'][i]=='SELL':
            df['Sell'][i]=df['CLOSE'][i]
        elif df['Action'][i]=='BUY':
            df['Buy'][i]=df['CLOSE'][i]
    return df

def ichimokuCloudBuySell(df):
    df['LeadingSpan']=np.nan
    for i in range(len(df)):
        if(df['LeadingSpanA'][i]>=df['LeadingSpanB'][i]):
            df['LeadingSpan'][i]=df['LeadingSpanA'][i]
        else:
            df['LeadingSpan'][i]=df['LeadingSpanB'][i]
    df['Action']=''
    for i in range(len(df)):
        conditions=[]
        if df['ConvLine'][i]>df['BaseLine'][i]:
            conditions.append(True)
        else:
            conditions.append(False)
        if df['LaggingSpan'][i]>df['CLOSE'][i]:
            conditions.append(True)
        else:
            conditions.append(False)
        if df['LeadingSpan'][i]>df['CLOSE'][i]:
            conditions.append(True)
        else:
            conditions.append(False)
        if (conditions.count(True)>=2):
            df['Action'][i]='BUY'
        else:
            df['Action'][i]='SELL'
    df['Sell']=0.0
    df['Buy']=0.0
    
    for i in range(1,len(df)):
        if df['Action'][i]=='SELL':
            df['Sell'][i]=df['CLOSE'][i]
        elif df['Action'][i]=='BUY':
            df['Buy'][i]=df['CLOSE'][i]
    return df

def MACD_strategy(df):
    df['Action']=''
    for i in range(len(df)):
        if df['MACD'][i]>df['Signal'][i]:
            df['Action'][i]='BUY'
        elif df['MACD'][i]<=df['Signal'][i]:
            df['Action'][i]='SELL'
        else:
            continue
    df['Sell']=0.0
    df['Buy']=0.0
    
    for i in range(1,len(df)):
        if df['Action'][i]=='SELL':
            df['Sell'][i]=df['CLOSE'][i]
        elif df['Action'][i]=='BUY':
            df['Buy'][i]=df['CLOSE'][i]
    return df

def RSI_strategy(df):
    df['Action']=''
    for i in range(0,len(df)):
        if df['RSI'][i-1]<30 and df['RSI'][i]>=30:
            df['Action'][i]='BUY'
        elif df['RSI'][i-1]<70 and df['RSI'][i]>=70:
            df['Action'][i]='SELL'
        elif df['Action'][i-1]=='BUY':
            df['Action'][i]='BUY'
        elif df['Action'][i-1]=='SELL':
            df['Action'][i]='SELL'
        elif df['RSI'][i]>70:
            df['Action'][i]='SELL'
        elif df['RSI'][i]<30:
            df['Action'][i]='BUY'
        else:
            df['Action'][i]='SELL'
    df['Sell']=0.0
    df['Buy']=0.0
    
    for i in range(1,len(df)):
        if df['Action'][i]=='SELL':
            df['Sell'][i]=df['CLOSE'][i]
        elif df['Action'][i]=='BUY':
            df['Buy'][i]=df['CLOSE'][i]
    return df

def bollingerStrategy(df):
    df['Action']=''
    for i in range(0,len(df)):
        if df['CLOSE'][i]<=df['LOWER'][i] or df['CLOSE'][i]>=df['SMA'][i]:
            df['Action'][i]='BUY'
        elif df['CLOSE'][i]>=df['UPPER'][i] or df['CLOSE'][i]<=df['SMA'][i]:
            df['Action'][i]='SELL'
        elif df['Action'][i-1]=='SELL':
            df['Action'][i]='SELL'
        elif df['Action'][i-1]=='BUY':
            df['Action'][i]='BUY'
    df['Sell']=0.0
    df['Buy']=0.0
    
    for i in range(1,len(df)):
        if df['Action'][i]=='SELL':
            df['Sell'][i]=df['CLOSE'][i]
        elif df['Action'][i]=='BUY':
            df['Buy'][i]=df['CLOSE'][i]
    return df

def buySellCharts(df,emas=[],ichimoku=False,bollinger=False,macd=False,rsi=False):
    Rows=2
    row_height=[0.8,0.2]
    heightG=600
    rsiRow=3
    macdRow=3
    if macd ==True and rsi==True:
        Rows=4
        macdRow=4
        row_height=[0.4,0.2,0.2,0.2]
        heightG=1000
    elif macd==True or rsi==True:
        Rows=3
        row_height=[0.5,0.2,0.3]
        heightG=800
    figure=make_subplots(rows=Rows, cols=1, shared_xaxes=True,vertical_spacing=0.01,row_heights=row_height)

    figure.add_trace(
        go.Candlestick(
            x=df.index,
            open=df.OPEN,
            high=df.HIGH,
            close=df.CLOSE,
            low=df.LOW,
            #increasing_line_color='GREEN',
            #increasing_line_width=0.8
            #decreasing_line_color='RED'
        ),row=1,col=1
    )
    figure.add_trace(
        go.Scatter(
            x=df.index,
            y=df['Sell'],
            line=dict(width=0.5,color='#FF0000'),
            fill='tozeroy',
            fillcolor='rgba(255,0,0,0.4)',
            name='SELL'
        ),row=1,col=1
    )
    figure.add_trace(
        go.Scatter(
            x=df.index,
            y=df['Buy'],
            line=dict(width=0.5,color='#00FF00'),
            fill='tozeroy',
            fillcolor='rgba(0,255,0,0.3)',
            name='BUY'
        ),row=1,col=1
    )
    colors = ['green' if row['OPEN'] - row['CLOSE'] >= 0 
          else 'red' for index, row in df.iterrows()]
    figure.add_trace(
        go.Bar(
            x=df.index,
            y=df.VOLUME,
            marker_color=colors
        ),row=2,col=1
    )
    for ema in emas:
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df[str(ema)],
                
                #line=dict(color=emas),
                name=str(ema)+ 'days EMA'
            ),row=1,col=1
        )
    
    

    if ichimoku==True:
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['BaseLine'],
                line=dict(width=1,color='#FFA500'),
                name='Base Line'
            ),row=1,col=1
        )
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['LeadingSpanA'],
                
                line=dict(width=1,color='#006400'),
                name='Leading Span A'
            ),row=1,col=1
        )
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['LeadingSpanB'],
                line=dict(width=1,color='#FF0000'),
                name='Leading Span B',
                fill='tonexty',
                fillcolor='rgba(00,64,00,0.5)',
                opacity=0.1
            ),row=1,col=1
        )
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['LaggingSpan'],
                line=dict(width=1,color='#90ee90'),
                name='Lagging Span'
            ),row=1,col=1
        )
    if bollinger==True:
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['UPPER'],
                line=dict(width=1,color='#0000FF'),
                name='UPPER'
            ),row=1,col=1
        )
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['LOWER'],
                line=dict(width=1,color='#0000FF'),
                name='LOWER',
                fill='tonexty',
                fillcolor='rgba(26,150,65,0.5)',
                opacity=0.1
            ),row=1,col=1
        )
    
    if macd==True:
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['Signal'],
                line=dict(color='#0000ff', width=1),
                legendgroup='2',
                name='signal'
            ), row=macdRow, col=1
        )
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['MACD'],
                line=dict(color='#00ff00', width=1),
                legendgroup='2',
                name='MACD'
            ), row=macdRow, col=1
        )
        colors = np.where(df['MACD_Hist'] < 0, '#FF0000', '#00FF00')
        # Plot the histogram
        figure.add_trace(
            go.Bar(
                x=df.index,
                y=df['MACD_Hist'],
                marker_color=colors,
            ), row=macdRow, col=1
        )
    
    if rsi==True:
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['RSI'],
                line=dict(color='#00ff00', width=1),
                name='RSI',
                # showlegend=False,
                legendgroup='1',
            ), row=rsiRow, col=1
        )
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['y1'],
                line=dict(color='#ff0000', width=1),
                name='Lower 20',
                # showlegend=False,
                legendgroup='1',
            ), row=rsiRow, col=1
        )
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['y2'],
                line=dict(color='#ff0000', width=1),
                name='Higher 80',
                # showlegend=False,
                legendgroup='1',
            ), row=rsiRow, col=1
        )
    figure.update_traces(increasing_fillcolor='green',increasing_line_color='green', 
                     decreasing_line_color='red',
                     selector=dict(type='candlestick'),increasing_line_width=1,decreasing_line_width=0.8,
                 decreasing_fillcolor='red')
    figure.layout.xaxis.type='category'
    figure.update_layout( 
        xaxis_rangeslider_visible=False,
        height=heightG,
        yaxis_range=[df['CLOSE'].min()-5,df['CLOSE'].max()+5]
    )
    
    return figure

  
#df=pd.read_csv('wholeData.csv')
#dff=df[df['SYMBOL']=='ABL']
#dff=stockChange(dff)
#emas=['10','20','30']
#for ema in emas:
#  dff=emaCalculator(dff,ema)
#print(dff)
def predictionFun(df,comp):
  scaler=scalerFun()
  #X_train,Y_train,X_test,Y_test=dataPreparation(df,scaler)
  data=pd.DataFrame(df['CLOSE'][len(df)-60:])
  Odata=data['CLOSE'].tolist()
  model=load_model(os.path.join('E:\Models\models',comp+'model.h5'))
  predictions=[]
  predictions.append(data['CLOSE'][-1])
  for i in range(0,7):
    data=Odata[len(Odata)-60:]
    data=np.array(data)
    data=scaler.fit_transform(data.reshape(-1,1))
    data=data.reshape(1,60,1)
    #print(data,type(data),data.shape)
    p=model.predict(data)
    val=scaler.inverse_transform(p)
    predictions.append(val[0][0])
    Odata.append(val[0][0])
  return predictions

def delta(day1,day2):
    day_start = day1
    day_end = day2
    fig = go.Figure(go.Indicator(
        mode="delta",
        value=day_end,
        delta={'reference': day_start, 'relative': True, 'valueformat':'.2%'}))
    fig.update_traces(delta_font={'size':13})
    fig.update_layout(height=25, width=120)

    if day_end >= day_start:
        fig.update_traces(delta_increasing_color='green')
    elif day_end < day_start:
        fig.update_traces(delta_decreasing_color='red')
    return fig

def marketSummary():
    url='https://www.psx.com.pk/market-summary/'
    response=requests.get(url)
    soup=BeautifulSoup(response.text,'html.parser')
    tables=soup.find_all('div',class_='table-responsive')
    tables=soup.find_all('div',{'class':"table-responsive"})
    stockData=[]
    stockSummaryVal=[]
    for table in tables[:2]:
        for i in table.find_all('td'):
            for j in i.find_all('p'):
                stockData.append(j.text)
    for val in stockData:
        stockSummaryVal.append(val.split(':'))
    return stockSummaryVal

def DataClean(df,symb):
    pd.options.mode.chained_assignment = None
    df=df[df['SYMBOL']==symb]
    df.set_index(df.Date,inplace=True)
    #df1.drop('SYMBOL',axis=1,inplace=True)
    df.drop('CHANGE',axis=1,inplace=True)
    df.drop('CHANGE (%)',axis=1,inplace=True)
    df.drop('Unnamed: 0',axis=1,inplace=True)
    df.drop('Date',axis=1,inplace=True)
    ld=df.LDCP.tolist()
    ldc=[]
    for i in ld:
        ldc.append(float(i.replace(',','')))
    df['LDCP']=ldc

    vol=df.VOLUME.tolist()
    volm=[]
    for i in vol:
        volm.append(int(i.replace(',','')))
    df['VOLUME']=volm

    op=df.OPEN.tolist()
    opn=[]
    for i in op:
        opn.append(float(i.replace(',','')))
    df['OPEN']=opn

    hig=df.HIGH.tolist()
    high=[]
    for i in hig:
        high.append(float(i.replace(',','')))
    df['HIGH']=high

    lo=df.LOW.tolist()
    low=[]
    for i in lo:
        low.append(float(i.replace(',','')))
    df['LOW']=low

    clo=df.CLOSE.tolist()
    close=[]
    for i in clo:
        close.append(float(i.replace(',','')))
    df['CLOSE']=close
    return df

def scalerFun():
  scaler=MinMaxScaler(feature_range=(0,1))
  return scaler

def dataPreparation(df,scaler):
  training_data=pd.DataFrame(df['CLOSE'][0:int(len(df)*0.8)])
  testing_data=pd.DataFrame(df['CLOSE'][int(len(df)*0.8):len(df)])
  train_data_Arr=scaler.fit_transform(training_data)
  X_train=[]
  Y_train=[]
  #print(len(df),len(training_data),len(testing_data),sep='\t')
  for i in range(60,train_data_Arr.shape[0]):
    X_train.append(train_data_Arr[i-60:i])
    Y_train.append(train_data_Arr[i,0])
  X_train=np.array(X_train)
  Y_train=np.array(Y_train)
  testingData=training_data.tail(60)
  testingData=testingData.append(testing_data,ignore_index=True)
  testingD=scaler.fit_transform(testingData)
  X_test=[]
  Y_test=[]
  for i in range(60,testingD.shape[0]):
    X_test.append(testingD[i-60:i])
    Y_test.append(testingD[i,0])
  X_test=np.array(X_test)
  Y_test=np.array(Y_test)
  return X_train,Y_train,X_test,Y_test


def channelsIdentification(df):
    df['SR']=np.arange(1,len(df)+1)
    m, b = np.polyfit(df['SR'],df['CLOSE'], 1)
    df['Mid']=(m*df['SR'])+b
    diffH=df['HIGH']-df['Mid']
    diffL=df['Mid']-df['LOW']
    mx=int(diffH.max())
    mn=int(diffL.min())
    mn=-(mn)
    countMax=[]
    countMin=[]
    for i in range(1,mx+1):
        m,b=np.polyfit(df['SR'],df['Mid']+i,1)
        count=0
        for i in range(len(df)):
            yy=int(m*df['SR'][i] + b)
            if yy==int(df['HIGH'][i]):
                count=count+1
        countMax.append([count,m,b])
    for i in range(1,mn+1):
        m,b=np.polyfit(df['SR'],df['Mid']-i,1)
        count=0
        for i in range(len(df)):
            yy=int(m*df['SR'][i] + b)
            if yy==int(df['LOW'][i]):
                count=count+1
        countMin.append([count,m,b])
    
    mmax=0
    cmax=0
    count=0
    for i in countMax:
        if i[0]==3:
            mmax=i[1]
            cmax=i[2]
        elif i[0]>3:
            mmax=i[1]
            cmax=i[2]
    mmin=0
    cmin=0
    count=0
    for i in countMin:
        if i[0]==3:
            mmin=i[1]
            cmin=i[2]
        elif i[0]>3:
            mmin=i[1]
            cmin=i[2]
    df['Uval']=0.0
    df['Lval']=0.0
    for i in range(len(df)):
        print(i)
        df['Uval'][i]=(mmax*i)+cmax
    for i in range(len(df)):
        df['Lval'][i]=(mmin*i)+cmin
    return df

def ichimokuCloud(df):
    NPH=df.HIGH.rolling(window=9).max() #nine period high
    NPL=df.LOW.rolling(window=9).min() #nine period low
    df['ConvLine']=(NPH+NPL)/2  # conversion line
    TPH=df.HIGH.rolling(window=26).max() #twenty six period high
    TPL=df.LOW.rolling(window=26).min() #twenty six period low
    df['BaseLine']=(TPH+TPL)/2  # conversion line
    df['LeadingSpanA']=((df['ConvLine']+df['BaseLine'])/2).shift(26) #leading span A
    FPH=df.HIGH.rolling(window=52).max() #fifty two period high
    FPL=df.LOW.rolling(window=52).min() #fifty two  period low
    df['LeadingSpanB']=(FPH+FPL)/2  #leading span A
    df['LaggingSpan']=df.CLOSE.shift(-26) # lagging span
    return df


def RSIcalculator(df):
    df['delta']=df.CLOSE.diff()
    df['up']=df.delta.clip(lower=0)
    df['down']=(-1)*df.delta.clip(upper=0)
    ema_up=df['up'].ewm(com=13,adjust=False).mean()
    ema_down=df['down'].ewm(com=13,adjust=False).mean()
    rs=ema_up/ema_down
    df['RSI']=100-(100/(1+rs))
    x=np.arange(0,len(df))
    df['x']=x
    df['y1']=30
    df['y2']=70
    return df

def bollingerCalculate(df,days=20):
    df['SMA']=df.CLOSE.rolling(window=days).mean()
    df['STD']=df.CLOSE.rolling(window=days).std()
    df['UPPER']=df['SMA']+(df['STD']*2)
    df['LOWER']=df['SMA']-(df['STD']*2)
    return df


def RSIcalculator(df,lv=30,uv=70):
    df['delta']=df.CLOSE.diff()
    df['up']=df.delta.clip(lower=0)
    df['down']=(-1)*df.delta.clip(upper=0)
    ema_up=df['up'].ewm(com=13,adjust=False).mean()
    ema_down=df['down'].ewm(com=13,adjust=False).mean()
    rs=ema_up/ema_down
    df['RSI']=100-(100/(1+rs))
    x=np.arange(0,len(df))
    df['x']=x
    df['y1']=lv
    df['y2']=uv
    return df

def MACDcalculate(df):
    shortEMA=df.CLOSE.ewm(span=12,adjust=False).mean()
    longEMA=df.CLOSE.ewm(span=26,adjust=False).mean()
    df['MACD']=-(longEMA-shortEMA)
    df['Signal']=df['MACD'].ewm(span=9,adjust=False).mean()
    df['MACD_Hist']=df['MACD']-df['Signal']
    return df


def hikenAshiCandles(df):
    heikenAshi=df[['LDCP','OPEN','HIGH','CLOSE','LOW','VOLUME']]
    heikenAshi.index=df.index
    heikenAshi['CLOSE'] = round(((df['OPEN'] + df['HIGH'] + df['LOW'] + df['CLOSE'])/4),2)
    for i in range(len(df)):
        if i == 0:
            heikenAshi.iat[0,0] = round(((df['OPEN'].iloc[0] + df['CLOSE'].iloc[0])/2),2)
        else:
            heikenAshi.iat[i,0] = round(((heikenAshi.iat[i-1,0] + heikenAshi.iat[i-1,2])/2),2)
    heikenAshi['HIGH'] = heikenAshi.loc[:,['OPEN', 'CLOSE']].join(df['HIGH']).max(axis=1)
    heikenAshi['LOW'] = heikenAshi.loc[:,['OPEN', 'CLOSE']].join(df['LOW']).min(axis=1)
    return heikenAshi

def lineCharts(df,emas,chanal,ichimoku,bollinger,macd,rsi):
    Rows=2
    row_height=[0.8,0.2]
    heightG=600
    rsiRow=3
    macdRow=3
    if macd ==True and rsi==True:
        Rows=4
        macdRow=4
        row_height=[0.4,0.2,0.2,0.2]
        heightG=1000
    elif macd==True or rsi==True:
        Rows=3
        row_height=[0.5,0.2,0.3]
        heightG=800
    figure=make_subplots(rows=Rows, cols=1, shared_xaxes=True,vertical_spacing=0.01,row_heights=row_height)

    figure.add_trace(
        go.Scatter(
            x=df.index,
            y=df.CLOSE,
            line=dict(color='#7CFC00'),
            fill='tonexty',
            #thickness=1,
            fillcolor='rgba(124,252,0,0.1)',
            name='CLOSE'
        ),row=1,col=1
    )
    colors = ['green' if row['OPEN'] - row['CLOSE'] >= 0 
          else 'red' for index, row in df.iterrows()]
    figure.add_trace(
        go.Bar(
            x=df.index,
            y=df.VOLUME,
            marker_color=colors
        ),row=2,col=1
    )
    for ema in emas:
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df[str(ema)],
                
                #line=dict(color=emas),
                name=str(ema)+ 'days EMA'
            ),row=1,col=1
        )
    
    if chanal==True:
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['Lval'],
                line=dict(color='#F0E68C'),
                name='Support'
            ),row=1,col=1
        )
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['Uval'],
                line=dict(color='#F0E68C'),
                fill='tonexty',
                fillcolor='rgba(240,230,140,0.2)',
                name='Resistance'
            ),row=1,col=1
        )

    if ichimoku==True:
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['BaseLine'],
                line=dict(color='#FFA500'),
                name='Base Line'
            ),row=1,col=1
        )
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['LeadingSpanA'],
                
                line=dict(color='#006400'),
                name='Leading Span A'
            ),row=1,col=1
        )
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['LeadingSpanB'],
                line=dict(color='#FF0000'),
                name='Leading Span B',
                fill='tonexty',
                fillcolor='rgba(00,64,00,0.5)',
                opacity=0.1
            ),row=1,col=1
        )
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['LaggingSpan'],
                line=dict(color='#90ee90'),
                name='Lagging Span'
            ),row=1,col=1
        )
    if bollinger==True:
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['UPPER'],
                line=dict(color='#0000FF'),
                name='UPPER'
            ),row=1,col=1
        )
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['LOWER'],
                line=dict(color='#0000FF'),
                name='LOWER',
                fill='tonexty',
                fillcolor='rgba(26,150,65,0.5)',
                opacity=0.1
            ),row=1,col=1
        )
    
    if macd==True:
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['Signal'],
                line=dict(color='#0000ff', width=2),
                legendgroup='2',
                name='signal'
            ), row=macdRow, col=1
        )
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['MACD'],
                line=dict(color='#00ff00', width=2),
                legendgroup='2',
                name='MACD'
            ), row=macdRow, col=1
        )
        colors = np.where(df['MACD_Hist'] < 0, '#FF0000', '#00FF00')
        # Plot the histogram
        figure.add_trace(
            go.Bar(
                x=df.index,
                y=df['MACD_Hist'],
                marker_color=colors,
            ), row=macdRow, col=1
        )
    
    if rsi==True:
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['RSI'],
                line=dict(color='#00ff00', width=1),
                name='RSI',
                # showlegend=False,
                legendgroup='1',
            ), row=rsiRow, col=1
        )
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['y1'],
                line=dict(color='#ff0000', width=1),
                name='Lower 20',
                # showlegend=False,
                legendgroup='1',
            ), row=rsiRow, col=1
        )
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df['y2'],
                line=dict(color='#ff0000', width=1),
                name='Higher 80',
                # showlegend=False,
                legendgroup='1',
            ), row=rsiRow, col=1
        )
    figure.layout.xaxis.type='category'
    figure.update_layout( 
        xaxis_rangeslider_visible=False,
        height=heightG,
        
    )
    return figure
  


def cleanedHeatMap(df):
    df=df[['SYMBOL','LDCP','OPEN','HIGH','LOW','CLOSE','VOLUME','Date','Name','Sector']]
    cols=['LDCP','OPEN','HIGH','LOW','CLOSE','VOLUME']
    for col in cols:
        op=df[col].tolist()
        opn=[]
        for i in op:
            opn.append(float(i.replace(',','')))
        df[col]=opn
    Date=df.Date.max()
    df=df[df['Date']==str(Date)]
    return df

def treeMapGenerator(df,val='VOLUME'):
    fig = px.treemap(df, path=[px.Constant("PSX"), 'Sector', 'SYMBOL'], values=val,
                  color_continuous_scale='orrd'
                  )
    fig.data[0].textinfo = 'label+text+value'
    fig.update_layout(height=700)
    return fig

def twentyfifty(df):
    df['20_EMA'] = df['CLOSE'].ewm(span = 20, adjust = False).mean()
    df['50_EMA'] = df['CLOSE'].ewm(span = 50, adjust = False).mean()
    #dfT=df
    df['Action']=''
    for i in range(len(df)):
        if (df['CLOSE'][i]>=df['20_EMA'][i]) and (df['20_EMA'][i]>=df['50_EMA'][i]):
            df['Action'][i]='BUY'
        else:
            df['Action'][i]='SELL'
    df['Sell']=np.nan
    df['Buy']=np.nan
    if df['Action'][0]=='SELL':
        df['Sell'][0]=df['CLOSE'][0]
    elif df['Action'][0]=='BUY':
        df['Buy'][0]=df['CLOSE'][0]
    for i in range(1,len(df)):
        if df['Action'][i]!=df['Action'][i-1]:
            if df['Action'][i]=='BUY':
                df['Buy'][i]=df['CLOSE'][i]
            elif df['Action'][i]=='SELL':
                df['Sell'][i]=df['CLOSE'][i]
            else:
                continue
    return df

def showEMA2050(df,title):
    figure=go.Figure(
        data=[
            go.Candlestick(
                x=df.index,
                open=df.OPEN,
                high=df.HIGH,
                close=df.CLOSE,
                low=df.LOW,
                
            )
        ],
        
    )
    
    figure.add_trace(go.Scatter(x=df.index, y=df['Buy'], mode = 'markers',
              marker =dict(symbol='triangle-down', size = 8,color='#00FFF0'),
              name='Buy Point'))
    figure.add_trace(go.Scatter(x=df.index, y=df['Sell'], mode = 'markers',
              marker =dict(symbol='triangle-up', size = 8,color='#FF00FF'),
              name='Sell Point'))

    figure.add_trace(
        go.Scatter(
            x=df.index,
            y=df['50_EMA'],
            line=dict(color='#FF00EE'),
            name='50 days EMA'
        )
    )
    figure.add_trace(
        go.Scatter(
            x=df.index,
            y=df['20_EMA'],
            line=dict(color='#0000EE'),
            name='20 days EMA'
        )
    )
    figure.update_layout( 
        xaxis_rangeslider_visible=False,
        
    )
    figure.show()


def buySellReturn(df):
    sb2050=sellBuytwentyfifty(df)
    df=df[['LDCP','OPEN','HIGH','LOW','CLOSE','CHANGE','VOLUME']]
    sb20200=sellBuytwentytwoHundred(df)
    df=df[['LDCP','OPEN','HIGH','LOW','CLOSE','CHANGE','VOLUME']]
    dfich=ichimokuCloud(df)
    bsich=ichimokuCloudBuySell(dfich)
    df=df[['LDCP','OPEN','HIGH','LOW','CLOSE','CHANGE','VOLUME']]
    dfmacd=MACDcalculate(df)
    bsmacd=MACD_strategy(dfmacd)
    df=df[['LDCP','OPEN','HIGH','LOW','CLOSE','CHANGE','VOLUME']]
    dfrsi=RSIcalculator(df)
    bsrsi=RSI_strategy(dfrsi)
    df=df[['LDCP','OPEN','HIGH','LOW','CLOSE','CHANGE','VOLUME']]
    dfboll=bollingerCalculate(df)
    bsboll=bollingerStrategy(dfboll)
    df=df[['LDCP','OPEN','HIGH','LOW','CLOSE','CHANGE','VOLUME']]
    buySell=pd.DataFrame()
    buySell['Action2050']=sb2050['Action'].tolist()
    buySell['Action20200']=sb20200['Action'].tolist()
    buySell['ActionIch']=bsich['Action'].tolist()
    buySell['ActionMacd']=bsmacd['Action'].tolist()
    buySell['ActionRSI']=bsrsi['Action'].tolist()
    buySell['ActionBoll']=bsboll['Action'].tolist()
    buySell.index=df.index
    return buySell


def oneMinuteGoldPrices():
    url='https://finance.yahoo.com/quote/GOLD?p=GOLD&.tsrc=fin-srch'
    response=requests.get(url)
    if(response.status_code==200):
        soup=BeautifulSoup(response.text,'html.parser')
        oneM=soup.find_all('fin-streamer',{'data-symbol':"GOLD"})
        oneMd=[]
        for o in oneM:
            oneMd.append(o.text)
    return oneMd[:3]

def goldScrap():
    url='https://finance.yahoo.com/quote/CL=F?p=CL=F&.tsrc=fin-srch'
    response=requests.get(url)
    if(response.status_code==200):
        soup=BeautifulSoup(response.text,'html.parser')
        tables=soup.find_all('table',{'class':'W(100%)'})
        dataList=[]
        for tab in tables:
            for data in tab.find_all('td'):
                dataList.append(data.text)
    return dataList

def deltaGraphs(data,predictions):
  for v in predictions:
    data.append(v)
  figures=[]
  for i in range(len(data)-1):
    print(data[i],data[i+1])
    figures.append(deltaGraphIM(data[i],data[i+1]))
  return figures

def deltaGraphIM(d1,d2):
    day_start = d1
    day_end = d2
    fig = go.Figure(go.Indicator(
        mode="delta",
        value=day_end,
        delta={'reference': day_start, 'relative': True, 'valueformat':'.2%'}))
    fig.update_traces(delta_font={'size':13})
    fig.update_layout(height=25, width=120)

    if day_end >= day_start:
        fig.update_traces(delta_increasing_color='green')
    elif day_end < day_start:
        fig.update_traces(delta_decreasing_color='red')
    return fig

def predictClean(predictions):
  predictions=np.squeeze(predictions)
  predictions=predictions.tolist()
  showPre=[]
  for v in predictions:
    showPre.append("{:.2f}".format(v))
  return predictions,showPre

def dataExt(df):
  data=df.filter(['Close'])
  dataset=data.values
  x=dataset[len(data)-8:]
  vals=np.squeeze(x)
  vals=vals.tolist()
  showData=[]
  for v in vals:
    showData.append("{:.2f}".format(v))
  return vals,showData

def cleanDataGold(dataList):
    dataReturn=[]
    for i in range(len(dataList)):
        if dataList[i]=='Open':
            dataReturn.append(dataList[i+1])
        if dataList[i]=='Bid':
            dataReturn.append(dataList[i+1])
        if dataList[i]=="Day's Range":
            data=dataList[i+1].split(' - ')
            for val in data:
                dataReturn.append(val)
        if dataList[i]=='Volume':
            dataReturn.append(dataList[i+1]) 
        if dataList[i]=='Ask':
            dataReturn.append(dataList[i+1]) 
    return dataReturn

def marketGoldPre(df):
  data=df.filter(['Close'])
  dataset=data.values
  scaler=MinMaxScaler(feature_range=(0,1))
  model=load_model(os.path.join('E:\8th semester\FYP\stockMarketApp\models\goldModel.h5'))
  predictions=[]
  for i in range(0,7):
    scaledData=scaler.fit_transform(dataset)
    scaledData=scaledData[len(dataset)-60:]
    predata=scaledData.reshape(1,60,1)
    pre=model.predict(predata)[0][0]
    pre=pre.reshape(-1,1)
    val=scaler.inverse_transform(pre)
    val=val[0].tolist()
    try:
      dataset=dataset.tolist()
    except:
      pass
    dataset.append(val)
    predictions.append(val)
  return predictions


def oneMinuteOilPrices():
    url='https://finance.yahoo.com/quote/CL%3DF?p=CL%3DF'
    response=requests.get(url)
    if(response.status_code==200):
        soup=BeautifulSoup(response.text,'html.parser')
        oneM=soup.find_all('fin-streamer',{'data-symbol':"CL=F"})
        oneMD=[]
        for o in oneM:
            oneMD.append(o.text)
    return oneMD[:3]

def oilScrap():
    url='https://finance.yahoo.com/quote/CL%3DF?p=CL%3DF'
    response=requests.get(url)
    if(response.status_code==200):
        soup=BeautifulSoup(response.text,'html.parser')
        tables=soup.find_all('table',{'class':'W(100%)'})
        dataList=[]
        for tab in tables:
            for data in tab.find_all('td'):
                dataList.append(data.text)
    return dataList


def marketOilPre(df):
  data=df.filter(['Close'])
  dataset=data.values
  scaler=MinMaxScaler(feature_range=(0,1))
  model=load_model(os.path.join('E:\8th semester\FYP\stockMarketApp\models\crudeOilModel.h5'))
  predictions=[]
  for i in range(0,7):
    scaledData=scaler.fit_transform(dataset)
    scaledData=scaledData[len(dataset)-60:]
    predata=scaledData.reshape(1,60,1)
    pre=model.predict(predata)[0][0]
    pre=pre.reshape(-1,1)
    val=scaler.inverse_transform(pre)
    val=val[0].tolist()
    try:
      dataset=dataset.tolist()
    except:
      pass
    dataset.append(val)
    predictions.append(val)
  return predictions




def dataCleaningPortfolio(df):
    df.index=df['Date']
    df.drop('Unnamed: 0',axis=1,inplace=True)
    df.drop('Unnamed: 0.1',axis=1,inplace=True)
    df.drop('LDCP',axis=1,inplace=True)
    df.drop('OPEN',axis=1,inplace=True)
    df.drop('HIGH',axis=1,inplace=True)
    df.drop('LOW',axis=1,inplace=True)
    df.drop('CHANGE',axis=1,inplace=True)
    df.drop('CHANGE (%)',axis=1,inplace=True)
    df.drop('VOLUME',axis=1,inplace=True)
    df.drop('Date',axis=1,inplace=True)
    clo=df.CLOSE.tolist()
    close=[]
    for i in clo:
        close.append(float(i.replace(',','')))
    df['CLOSE']=close
    return df

def byCompanies(df,symbols):
    conDf=pd.DataFrame()
    for symb in symbols:
        conDf[symb]=df[df['SYMBOL']==symb]['CLOSE']
    null_percentage = conDf.isnull().sum()/conDf.shape[0]*100
    col_to_drop = null_percentage[null_percentage>20].keys()
    conDf.drop(col_to_drop, axis=1,inplace=True)
    conDf.fillna(method='ffill',inplace=True)
    conDf.fillna(method='bfill',inplace=True)
    return conDf

def portfolioCalculation(conDf,amount,lowRisk=True):
    mu=expected_returns.mean_historical_return(conDf)
    S=risk_models.risk_matrix(conDf)
    ef= EfficientFrontier(mu,S)
    ef.add_objective(objective_functions.L2_reg, gamma=0.5)
    
    if lowRisk==True:
        weights=ef.efficient_risk(target_volatility=10)
    else:
        weights=ef.max_sharpe()
    cleanedWeights=ef.clean_weights()
    ef.portfolio_performance(verbose=True)

    portfolio_val=amount
    latest_prices=get_latest_prices(conDf)
    weights=cleanedWeights
    da=DiscreteAllocation(weights,latest_prices,total_portfolio_value=portfolio_val)
    allocation,leftover=da.greedy_portfolio()

    portfolioTable=pd.DataFrame()
    portfolioTable['Ticker']=allocation.keys()
    portfolioTable['Shares']=allocation.values()
    amount=[]
    for i in range(len(portfolioTable)):
        amount.append(latest_prices[portfolioTable['Ticker'][i]]*portfolioTable['Shares'][i])
    portfolioTable['Amount']=amount
    return portfolioTable,leftover



def lineReturnPortfolio(d,symb):
    fig = px.line(d, x=d.index, y=symb,
                   range_y=[d[symb].min(), d[symb].max()],
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
    temp=d.sort_index(ascending=False)
    
    day_start = temp[symb][len(temp)-1]
    day_end = temp[symb][0]
    print(day_start)
    print(day_end)
    if day_end > day_start:
        return fig.update_traces(fill='tozeroy',line={'color':'green'})
    elif day_end < day_start:
        return fig.update_traces(fill='tozeroy',line={'color': 'red'})
    else:
        return fig.update_traces(fill='tozeroy',line={'color': 'blue'})

def deltaGraphPortfolio(d,symb):
    temp=d.sort_index(ascending=False)
    day_start = temp[symb][1]
    day_end = temp[symb][0]
    fig = go.Figure(go.Indicator(
        mode="delta",
        value=day_end,
        delta={'reference': day_start, 'relative': True, 'valueformat':'.2%'}))
    fig.update_traces(delta_font={'size':20})
    fig.update_layout(height=50, width=150)

    if day_end >= day_start:
        fig.update_traces(delta_increasing_color='green')
    elif day_end < day_start:
        fig.update_traces(delta_decreasing_color='red')
    return fig

def portfolioMaker(conDf,amount,choice='ST'):
    conDf=conDf.sort_index(ascending=False)
    if choice=='ST':
        sel=conDf.iloc[:30]
    elif choice=='AT':
        sel=conDf.iloc[:60]
    else:
        sel=conDf.iloc[:120]
    valDiff={}
    minIn=sel.index.min()
    maxIn=sel.index.max()
    for col in sel.columns:
        valDiff[col]=sel[col][sel.index==maxIn][0]-sel[col][sel.index==minIn][0]
    pV=[]
    for k,v in valDiff.items():
        if v>0:
            pV.append(v)
    avg=sum(pV)/len(pV)
    valus=[]
    for k,v in valDiff.items():
        if v>avg:
            valus.append(v)
    selectedComp=sorted(valus,reverse=True)
    keys=[]
    for s in selectedComp:
        for k,v in valDiff.items():
            if s==v:
                keys.append(k)
    
    od=OrderedDict()
    for i in range(len(selectedComp)):
        od[keys[i]]=selectedComp[i]/sum(selectedComp)
    
    latest_prices=get_latest_prices(sel)
    da=DiscreteAllocation(od,latest_prices,total_portfolio_value=amount)
    allocation,leftover=da.greedy_portfolio()

    portfolioTable=pd.DataFrame()
    portfolioTable['Ticker']=allocation.keys()
    portfolioTable['Shares']=allocation.values()
    amount=[]
    for i in range(len(portfolioTable)):
        amount.append(latest_prices[portfolioTable['Ticker'][i]]*portfolioTable['Shares'][i])
    portfolioTable['Amount']=amount
    return portfolioTable,leftover

def deltaGraphRecomender(v1,v2):
    day_start = v2
    day_end = v1
    fig = go.Figure(go.Indicator(
        mode="delta",
        value=day_end,
        delta={'reference': day_start, 'relative': True, 'valueformat':'.2%'}))
    fig.update_traces(delta_font={'size':13})
    fig.update_layout(height=25, width=120)

    if day_end >= day_start:
        fig.update_traces(delta_increasing_color='green')
    elif day_end < day_start:
        fig.update_traces(delta_decreasing_color='red')
    return fig

def recommendationReturn(conDf):
    conDf=conDf.sort_index(ascending=False)
    recomender=pd.DataFrame(columns=['Company','1D','1W','1M','3M','6M'])
    for col in conDf.columns:
        row={}
        row['Company']=col
        row['1D']=conDf[col][0]-conDf[col][1]
        row['1W']=conDf[col][0]-conDf[col][5]
        row['1M']=conDf[col][0]-conDf[col][20]
        row['3M']=conDf[col][0]-conDf[col][60]
        row['6M']=conDf[col][0]-conDf[col][120]
        recomender=recomender.append(row,ignore_index=True)
    recomender.index=recomender['Company']
    recomender.drop('Company',axis=1,inplace=True)
    positives=[]
    for v in recomender.index:
        count=0
        for j in range(5):
            if recomender.loc[v][j]>0:
                count=count+1
        positives.append(count)
    recomender['Positive']=positives
    
    recomender=recomender[recomender['Positive']>1]
    
    deltagraphs=[]
    for col in recomender.index:
        row=[]
        row.append(deltaGraphRecomender(conDf[col][0],conDf[col][1]))
        row.append(deltaGraphRecomender(conDf[col][0],conDf[col][5]))
        row.append(deltaGraphRecomender(conDf[col][0],conDf[col][20]))
        row.append(deltaGraphRecomender(conDf[col][0],conDf[col][60]))
        row.append(deltaGraphRecomender(conDf[col][0],conDf[col][120]))
        deltagraphs.append(row)
    return recomender,deltagraphs