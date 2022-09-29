from altair.vegalite.v4.schema import Color
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import numpy as np
from PIL import Image
import time
import requests
import plotly.graph_objects as go



def main_page():
	# Título y subtítulo.
	#st.title('Introducción a Streamlit')
    image = Image.open('images/henrylogo1.png')
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(' ')

    with col2:
        st.image(image)

    with col3:
        st.write(' ')
    st.markdown("<h1 style='text-align: center; color: white;'>DE CARA HACIA EL FUTURO</h1>", unsafe_allow_html=True) 
    #st.sidebar.markdown('''
	#* La Revolución Henry 
	#* El HENRYCOIN
	#* Crisis U Oportunidad''')

    st.markdown('''
	### "Estamos repensando la educación en latinoamerica para brindar oportunidades y desarrollar talento. Súmate a nuestra revolución."
    ''')
    st.markdown("<h1 style='text-align: center; color: white;'>¿Y si ahora repensamos la Economía?</h1>", unsafe_allow_html=True)   


def pageII():
    st.markdown("<h1 style='text-align: center; color: white;'>HENRYCOIN</h1>", unsafe_allow_html=True) 
    image = Image.open('images/henrycoin.jpeg')
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(' ')

    with col2:
        st.image(image)

    with col3:
        st.write(' ')
    st.markdown("<h3 style='text-align: center; color: white;'>¿ES EL MOMENTO OPORTUNO PARA EL LANZAMIENTO?</h1>", unsafe_allow_html=True) 
   
def pageIII():  
    st.markdown("<h3 style='text-align: center; color: white;'>¿OTRO CRIPTOINVIERNO?</h1>", unsafe_allow_html=True)
    #st.sidebar.markdown('CRIPTOMONEDA')
    market_name = 'BTC'
    resolution = 60 * 60
    start = round(time.time() - 24*60*60) 
    market_name = st.sidebar.selectbox('CRIPTOMONEDA',['BTC', 'ETH', 'USDT', 'SOL', 'DOGE', 'DAI', 'MATIC', 'SHIB', 'TRX', 'AVAX'])
    vs = st.sidebar.selectbox('VS',['USD', 'BTC', 'ETH', 'USDT', 'SOL', 'DOGE', 'DAI', 'MATIC', 'SHIB', 'TRX', 'AVAX'])
    
    tiempo = st.sidebar.selectbox("Ciclo de tiempo", ['6 meses', '1 mes', '1 dia'])
    
    if tiempo == '1 dia':
        resolution = 60 * 60
        start = round(time.time() - 24*60*60) 
    elif tiempo == '1 mes':
        resolution = 60 * 60 * 24
        start = round(time.time() - 24*60*60*30)
    else:
        resolution = 60 * 60 * 24
        start = round(time.time() - 24*60*60*30*6)
    api_url = 'https://ftx.us/api'
    path = f'/markets/{market_name}/{vs}/candles?resolution={resolution}&start_time={start}'
    url = api_url + path
    
    res = requests.get(url).json()
    df = pd.DataFrame(res['result'])
    df.drop(['startTime'], axis = 1, inplace=True)
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    df.set_index('time', inplace=True)
    df['20 SMA'] = df.close.rolling(20).mean()
    last = df.loc[df.index[-1], "close"]
    msj = 'Valor actual: 1'+ market_name + '=' + str(last) + ' ' + vs
    st.sidebar.markdown(msj)
    var = df.close.var()
    msj = 'Var: '+ str(var)
    st.sidebar.markdown(msj)

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.1, subplot_titles=('OHLC', 'Volume'), 
                        row_width=[0.2, 0.7],column_widths=[2])

# Plot OHLC on 1st row
    fig.add_trace(go.Candlestick(x = df.index, open = df['open'], high = df['high'], low = df['low'], close = df['close'], name="OHLC")
                #,go.Scatter(x=df.index, y=df['20 SMA'], line=dict(color='purple', width=1))]),
                , row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['20 SMA'], line=dict(color='purple', width=1)), row=1, col=1)

# Bar trace for volumes on 2nd row without legend
    fig.add_trace(go.Bar(x=df.index, y=df['volume'], showlegend=False), row=2, col=1)

# Do not show OHLC's rangeslider plot 
    fig.update(layout_xaxis_rangeslider_visible=False)
    st.plotly_chart(fig)

def pageIV():
    st.markdown("<h3 style='text-align: center; color: white;'>¿Y COMO ESTAN LAS EMPRESAS TECNOLOGICAS?</h1>", unsafe_allow_html=True)
    st.sidebar.markdown('Empresa')
    key = 'VS12DFNCBNZZ71BZ' #https://www.alphavantage.co/
    symbol = 'AAPL' #'IBM', AAPL, MSFT, YHOO, GOOG, RHT, LNVGY, BABA, CAT, AMZN
    funct = 'TIME_SERIES_DAILY'
    size = 'compact' #compact,full
    symbol = st.sidebar.selectbox('Simbolo', ['META', 'IBM', 'AAPL', 'MSFT', 'YHOO', 'GOOG', 'LNVGY', 'BABA', 'CAT', 'AMZN', 'TSLA', 'SHOP'])
    api_url2 = 'https://www.alphavantage.co'
    path2 = f'/query?function={funct}&symbol={symbol}&outputsize={size}&apikey={key}&datatype=csv'
    url2 = api_url2 + path2
    df = pd.read_csv(url2)
    df.set_index('timestamp', inplace=True)
    df.sort_index(ascending=True, inplace=True)
    df['20 SMA'] = df.close.rolling(20).mean()
    df['20 var'] = df.close.rolling(20).var()
    #st.dataframe(df)

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.1, subplot_titles=('OHLC', 'Volume'), 
                        row_width=[0.2, 0.7],column_widths=[2])

# Plot OHLC on 1st row
    fig.add_trace(go.Candlestick(x = df.index, open = df['open'], high = df['high'], low = df['low'], close = df['close'], name="OHLC")
                #,go.Scatter(x=df.index, y=df['20 SMA'], line=dict(color='purple', width=1))]),
                , row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['20 SMA'], line=dict(color='purple', width=1)), row=1, col=1)
    

# Bar trace for volumes on 2nd row without legend
    fig.add_trace(go.Bar(x=df.index, y=df['volume'], showlegend=False), row=2, col=1)

# Do not show OHLC's rangeslider plot 
    fig.update(layout_xaxis_rangeslider_visible=False)
    st.plotly_chart(fig)

def pageVI():
    #st.markdown("<h3 style='text-align: center; color: black;'>INFLACION EN ESTADOS UNIDOS</h1>", unsafe_allow_html=True)
    image = Image.open('images/united-states-inflation-cpi.png')
    st.image(image)
    #col1, col2, col3 = st.columns(3)

    #with col1:
     #   st.write(' ')

    #with col2:
     #   st.image(image)

    #with col3:
     #   st.write(' ')
page_names_to_funcs = {
    'I. Introducción': main_page,
    'II. ¿Es el momento oportuno?': pageII,
    'III. El CriptoInvierno' : pageIII,
    'IV. Las Acciones de las Empresas Tecnológicas': pageIV,
    'VI. La Inflacion en Estados Unidos y la Cotización del Dólar' : pageVI
}

selected_page = st.sidebar.selectbox("Seleccione página", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()





  
