# pip install pandas numpy matplotlib streamlit fbprophet cryptocmd plotly
import streamlit as st
from datetime import date

from cryptocmd import CmcScraper
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go

# START = "2015-01-01"
# today = date.today().strftime("%Y-%m-%d")

st.title('Crypto Forecaster')

### Select ticker & number of days to predict on
selected_ticker = st.text_input("Select a ticker for prediction (i.e. BTC, ETH, LINK, etc.)", "BTC")
period = st.number_input('Number of days to predict:', min_value=0.0, max_value=5000.0, value=30.0, step=0.1)

### Initialise scraper without time interval
@st.cache
def load_data(selected_ticker):
	init_scraper = CmcScraper(selected_ticker)
	df = init_scraper.get_dataframe()
	min_date = pd.to_datetime(min(df['Date']))
	max_date = pd.to_datetime(max(df['Date']))
	# data.reset_index(inplace=True)
	return init_df, min_date, max_date

data_load_state = st.text('Loading data...')
init_df, min_date, max_date = load_data(selected_ticker)
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

	### Create model
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