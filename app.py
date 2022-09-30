import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
from PIL import Image
import time
import requests
import plotly.graph_objects as go

def main_page():
	
    image = Image.open('images/henrylogo1.png')
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(' ')

    with col2:
        st.image(image)

    with col3:
        st.write(' ')
    st.markdown("<h1 style='text-align: center; color: white;'>DE CARA HACIA EL FUTURO</h1>", unsafe_allow_html=True) 
 

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
                        vertical_spacing=0.1, subplot_titles=(market_name, 'Volume'), 
                        row_width=[0.2, 0.7],column_widths=[2])

# Plot OHLC on 1st row
    fig.add_trace(go.Candlestick(x = df.index, open = df['open'], high = df['high'], low = df['low'], close = df['close'], name="OHLC")
                  , row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['20 SMA'], line=dict(color='yellow', width=1)), row=1, col=1)

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
                        vertical_spacing=0.1, subplot_titles=(symbol, 'Volume'), 
                        row_width=[0.2, 0.7],column_widths=[2])

# Plot OHLC on 1st row
    fig.add_trace(go.Candlestick(x = df.index, open = df['open'], high = df['high'], low = df['low'], close = df['close'], name="OHLC")
                #,go.Scatter(x=df.index, y=df['20 SMA'], line=dict(color='purple', width=1))]),
                , row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['20 SMA'], line=dict(color='yellow', width=1)), row=1, col=1)
    

# Bar trace for volumes on 2nd row without legend
    fig.add_trace(go.Bar(x=df.index, y=df['volume'], showlegend=False), row=2, col=1)

# Do not show OHLC's rangeslider plot 
    fig.update(layout_xaxis_rangeslider_visible=False)
    st.plotly_chart(fig)

def pageV():
    st.markdown("<h3 style='text-align: center; color: white;'>INDICE DEL MIEDO Y CODICIA</h1>", unsafe_allow_html=True)
    f = open('miedo.png','wb')
    response = requests.get('https://alternative.me/crypto/fear-and-greed-index.png')
    f.write(response.content)
    f.close()
    image = Image.open('miedo.png')
    st.sidebar.image(image)
    
    url2 = 'https://api.alternative.me/fng/?limit=180'
    res = requests.get(url2).json()
    df = pd.DataFrame(res['data'])
    df['timestamp'] = df['timestamp'].astype(int, errors = 'raise')
    df['value'] = df['value'].astype(int, errors = 'raise')
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

    fig = make_subplots(rows=1, cols=1, column_widths=[3])
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['value'], line=dict(color='yellow', width=1)))
    st.plotly_chart(fig)

page_names_to_funcs = {
    'I. Introducción': main_page,
    'II. ¿Es el momento oportuno?': pageII,
    'III. El CriptoInvierno' : pageIII,
    'IV. Las Acciones de las Empresas Tecnológicas': pageIV,
    'V. El Indice de Miedo y Codicia' : pageV
}

selected_page = st.sidebar.selectbox("Seleccione página", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()





  