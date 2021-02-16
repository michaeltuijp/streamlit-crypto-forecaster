# pip install pandas numpy matplotlib streamlit pystan fbprophet neuralprophet cryptocmd plotly
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib as plt
from datetime import date

from cryptocmd import CmcScraper
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
# from neuralprophet import NeuralProphet
from plotly import graph_objs as go

# START = "2015-01-01"
# today = date.today().strftime("%Y-%m-%d")

st.title('Crypto Forecaster')

### Select ticker & number of days to predict on
selected_ticker = st.text_input("Select a ticker for prediction (i.e. BTC, ETH, LINK, etc.)", "BTC")
period = int(st.number_input('Number of days to predict:', min_value=0, max_value=5000, value=30, step=1))

### Initialise scraper without time interval
@st.cache
def load_data(selected_ticker):
	init_scraper = CmcScraper(selected_ticker)
	df = init_scraper.get_dataframe()
	min_date = pd.to_datetime(min(df['Date']))
	max_date = pd.to_datetime(max(df['Date']))
	# data.reset_index(inplace=True)
	return min_date, max_date

data_load_state = st.text('Loading data...')
min_date, max_date = load_data(selected_ticker)
data_load_state.text('Loading data... done!')


### Select date range
date_range = st.selectbox("Select the data timeframe:", options=["All available data", "Specific date range"])

if date_range == "All available data":

	### Initialise scraper without time interval
	scraper = CmcScraper(selected_ticker)

elif date_range == "Specific date range":

	### Initialise scraper with time interval
	start_date = st.date_input('Select start date:', min_value=min_date, max_value=max_date, value=max_date)
	end_date = st.date_input('Select end date:', min_value=min_date, max_value=max_date, value=max_date)
	scraper = CmcScraper(selected_ticker, start_date, end_date)

### Pandas dataFrame for the same data
data = scraper.get_dataframe()


st.subheader('Raw data')
st.write(data.tail())

### Plot functions
def plot_raw_data():
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="Open"))
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="Close"))
	fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
	st.plotly_chart(fig)

def plot_raw_data_log():
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="Open"))
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="Close"))
	fig.update_xaxes(type="log")
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
	st.write(forecast.tail())
	    
	st.write(f'Forecast plot for {period} days')
	fig1 = plot_plotly(m, forecast)
	st.plotly_chart(fig1)

	st.write("Forecast components")
	fig2 = m.plot_components(forecast)
	st.write(fig2)


	# ### Create NeuralProphet model
	# # m2 = NeuralProphet()
	# m2 = NeuralProphet(
	#     n_forecasts=period,
	#     # n_lags=60,
	#     n_changepoints=100,
	#     yearly_seasonality=True,
	#     weekly_seasonality=True,
	#     daily_seasonality=True,
	#     batch_size=64,
	#     epochs=100,
	#     learning_rate=1.0,
	# )

	# ### Fit the model
	# m2.fit(df_train, 
	#           freq='D',
	#           valid_p=0.2,
	#           epochs=100)

	# ### Predict using Neural Prophet
	# neural_future = m2.make_future_dataframe(df_train, periods=period)
	# neural_forecast = m2.predict(neural_future)

	# ### Show and plot forecast
	# st.subheader('Forecast Neural Prophet data')
	# st.write(neural_forecast.tail())
	    
	# st.write(f'Forecast Neural Prophet plot for {period} days')
	# fig3 = plot_plotly(m2, neural_forecast)
	# st.plotly_chart(fig3)

	# st.write("Neural Prophet Forecast components")
	# fig4 = m.plot_components(neural_forecast)
	# st.write(fig4)

	# # ### Plot the model
	# # try:
	# # 	st.markdown(plot_forecast(m2, df_train, periods=period, historic_predictions=True))
	# # except:
	# # 	None

	# # metrics = m2.fit(df_train, validate_each_epoch=True, 
	# #                     valid_p=0.2, freq='D', 
	# #                     plot_live_loss=True, epochs=10)