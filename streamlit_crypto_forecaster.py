# pip install pandas numpy matplotlib streamlit pystan fbprophet cryptocmd plotly
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib as plt
from datetime import date, datetime

from cryptocmd import CmcScraper
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go

st.title('Crypto Forecaster')

st.markdown("This application enables you to predict on the future value of any cryptocurrency (available on Coinmarketcap.com), for \
	any number of days into the future! The application is built with Streamlit (the front-end) and the Facebook Prophet model, \
	which is an advanced open-source forecasting model built by Facebook, running under the hood. You can select to train the model \
	on either all available data or a pre-set date range. Finally, you can plot the prediction results on both a normal and log scale.") 
	### Add save prediction dataset + image option?

### Change sidebar color
st.markdown(
    """
<style>
.sidebar .sidebar-content {
    background-image: linear-gradient(#D6EAF8,#D6EAF8);
    color: white;
}
</style>
""",
    unsafe_allow_html=True,
)

st.sidebar.subheader("Forecaster Settings")

### Select ticker & number of days to predict on
selected_ticker = st.sidebar.text_input("Select a ticker for prediction (i.e. BTC, ETH, LINK, etc.)", "BTC")
period = int(st.sidebar.number_input('Number of days to predict:', min_value=0, max_value=100000, value=30, step=1))

### Initialise scraper without time interval
@st.cache
def load_data(selected_ticker):
	init_scraper = CmcScraper(selected_ticker)
	df = init_scraper.get_dataframe()
	min_date = pd.to_datetime(min(df['Date']))
	max_date = pd.to_datetime(max(df['Date']))
	return min_date, max_date

data_load_state = st.sidebar.text('Loading data...')
min_date, max_date = load_data(selected_ticker)
data_load_state.text('Loading data... done!')


### Select date range
date_range = st.sidebar.selectbox("Select the data timeframe:", options=["All available data", "Specific date range"])

if date_range == "All available data":

	### Initialise scraper without time interval
	scraper = CmcScraper(selected_ticker)

elif date_range == "Specific date range":

	### Initialise scraper with time interval
	start_date = st.sidebar.date_input('Select start date:', min_value=min_date, max_value=max_date, value=max_date)
	end_date = st.sidebar.date_input('Select end date:', min_value=min_date, max_value=max_date, value=max_date)
	scraper = CmcScraper(selected_ticker, str(start_date.strftime("%d-%m-%Y")), str(end_date.strftime("%d-%m-%Y")))

### Pandas dataFrame for the same data
data = scraper.get_dataframe()


st.subheader('Raw data')
st.write(data.head())

### Plot functions
def plot_raw_data():
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="Close"))
	fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
	st.plotly_chart(fig)

def plot_raw_data_log():
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="Close"))
	fig.update_yaxes(type="log")
	fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
	st.plotly_chart(fig)
	
### Plot (log) data
plot_log = st.checkbox("Plot log scale")
if plot_log:
	plot_raw_data_log()
else:
	plot_raw_data()

### Predict forecast with Prophet
if st.button("Predict"):

	df_train = data[['Date','Close']]
	df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

	### Create Prophet model
	m = Prophet()
	m.fit(df_train)
	future = m.make_future_dataframe(periods=period)
	forecast = m.predict(future)

	### Show and plot forecast
	st.subheader('Forecast data')
	st.write(forecast.head())
	    
	st.write(f'Forecast plot for {period} days')
	fig1 = plot_plotly(m, forecast)
	if plot_log:
		fig1.update_yaxes(type="log")
	st.plotly_chart(fig1)

	st.write("Forecast components")
	fig2 = m.plot_components(forecast)
	st.write(fig2)