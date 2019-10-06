#!/usr/bin/env python
# coding: utf-8

#!pip install quandl
#!pip install plotly
#!pip install matplotlib
#!pip install seaborn
#!pip install pandas
#!pip install numpy

import plotly 
plotly.tools.set_credentials_file(username='W1185156', api_key='P0Mh0hxLIz1joJ2fNcmK')
import quandl
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
import numpy as np
import seaborn as sns
import plotly.graph_objs as go
import plotly.plotly as py
import os
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

#get_ipython().run_line_magic('matplotlib', 'inline')

#import data set
df = pd.read_csv('companylist.csv')

#Turn dataframe into two columns
stockingdata = df.drop(["LastSale", "MarketCap", "ADR TSO", "IPOyear", "Sector", "Industry", "Summary Quote"], axis=1)
if len(stockingdata.columns) == 3:
    stockingdata = stockingdata.iloc[:, :-1]

#Turn dataframe columns into two lists
symbol = df['Symbol'].tolist()
name = df['Name'].tolist()

# Create a zip object from two lists
zipbObj = zip(name, symbol)

#Turn two lists into dictionary
symboldictionary = dict(zipbObj)

while True:
    #have user pick company to search
    ucompany = input("What company would you like to see the financial data for? ")

    if ucompany in symbol:
        e = ucompany
        break

    if ucompany in name:
        e = symboldictionary.get(ucompany, '')
        break

    print("invalid company name or ticker.")


#get stock information from quandl
ndataset = quandl.get('WIKI/'+ e)

dataset = ndataset.drop(["Ex-Dividend", "Split Ratio", "Adj. Open", "Adj. High", "Adj. Low", "Adj. Close", "Adj. Volume"], axis=1)

#ask user what information they would like to see visualized
options = ['Highs and Lows of '+ucompany+' over time',
           'Open and Close of '+ucompany+' over time',
           'Highs, Lows, and Closing Price of '+ucompany+' over time']
df = pd.DataFrame(options, index = ['Option 1', 'Option 2', 'Option 3'],
                 columns = ['Information'])

print(df)

uinfo = input("What option would you like to see? ")

#'Option 1'

def plot1():
    high = dataset['High']

    low = dataset['Low']

    time = dataset.index

    trace_high = go.Scatter(
                    x=time,
                    y=high,
                    name = ucompany +" High",
                    line = dict(color = '#bddb51'),
                    opacity = 0.8)

    trace_low = go.Scatter(
                    x=time,
                    y=low,
                    name = ucompany + " Low",
                    line = dict(color = '#3f4a85'),
                    opacity = 0.8)

    data = [trace_high,trace_low]

    layout = go.Layout(
        title=go.layout.Title(
            text= '          ' + ucompany + "  Highs and Lows From 1996 Until Present",
            font=dict(
                    family='Avenir',
                    size=18,
                    color='#3d0b51'
                ),
            xref='paper',
            x=0
        ),
        xaxis=go.layout.XAxis(
            title=go.layout.xaxis.Title(
                text='Time',
                font=dict(
                    family='Avenir',
                    size=18,
                    color='#3d0b51'
                )
            )
        ),
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text='Stock Price',
                font=dict(
                    family='Avenir',
                    size=18,
                    color='#3d0b51'
                )
            )
        )
    )

    plotly.offline.plot({"data": data, "layout": layout})

#if user chooses 'Option 2'
def plot2():
    high = dataset['High']

    low = dataset['Low']

    open1 = dataset['Open']

    close = dataset['Close']

    volume = dataset['Volume']

    time = dataset.index

    trace_comp0 = go.Scatter(
        x=time,
        y=close,
        mode='markers',
        marker=dict(size=12,
                    line=dict(width=1),
                    color='#3f4a85'
                ),
        name='Closing Stock Price',
        )

    trace_comp1 = go.Scatter(
        x=time,
        y=open1,
        mode='markers',
        marker=dict(size=12,
                    line=dict(width=1),
                    color='#bddb51'
                ),
        name='Opening Stock Price',
            )

    data_comp = [trace_comp0, trace_comp1]
    layout_comp = go.Layout(
        title='Opening v. Closing Stock Price, 1996 - Present',
        hovermode='closest',
        xaxis=dict(
            title='Time (Years)',
            ticklen=5,
            zeroline=False,
            gridwidth=2,
        ),
        yaxis=dict(
            title='Stock Price',
            ticklen=5,
            gridwidth=2,
        ),
    )

    plotly.offline.plot({"data": data_comp, "layout": layout_comp})

#if user chooses 'Option 3'
def plot3():
    high = dataset[['High']]

    low = dataset[['Low']]

    open1 = dataset[['Open']]

    close = dataset[['Close']]

    volume = dataset[['Volume']]

    time = dataset.index

    trace1 = go.Scatter3d(
        x= time,
        y= high,
        z= low,
        mode='markers',
        marker=dict(
            size=13,
            color= close,          # set color to an array/list of desired values
            colorscale='Viridis',   # choose a colorscale
            colorbar = dict(title = 'Closing Stock Price'),
            opacity=0.8
        )
    )

    data = [trace1]

    layout2 = go.Layout(
        
        font=dict(
                    family='Avenir',
                    size=13,
                    color='#3d0b51'
                ),
                        scene = dict(
                        xaxis = dict(
                            title='Time'),
                        yaxis = dict(
                            title='High Stock Price'),
                        zaxis = dict(
                            title='Low Stock Price'),),
                        width=700,
                        margin=dict(
                        r=20, b=10,
                        l=10, t=10)
    )

    fig3 = go.Figure(data=data, layout=layout2)
    py.plot(fig3)          # works, online
    #py.offline.plot(fig3)  # doesnt work, offline?

#if statement for choosing options
if uinfo == 'Option 1':
    plot1()
elif uinfo == 'Option 2':
    plot2()
else:
    plot3()
