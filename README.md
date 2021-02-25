# streamlit-crypto-forecaster
![Alt text](streamlit-crypto-forecaster.png?raw=true "Streamlit Crypto Forecaster")

This repository contains a Streamlit app, which predicts the future price of a user specified crypto ticker from Coinmarketcap using Facebook Prophet! By no means do I believe the predictions are 100% accurate, nor would it be any kind of financial advice. However, it's interesting to see what the model predicts & check its accuracy over time.


Additionally, you could use these files as a template for your own (forecasting) applications, which need not be crypto related at all (predicting COVID cases, sales of the company you work at, you name it)!


I've created a simple Heroku deployment of the app. You can go to this url & play around with it yourself!

https://streamlit-crypto-forecaster.herokuapp.com/


If you like to learn more about how the app is built, check out the Medium article I've written about it:

https://michaeltuijp.medium.com/predicting-cryptocurrency-prices-using-facebook-prophet-a1509415224f


In order to use this application locally:
  - Clone the repository in your own local folder
  - Open up your command prompt and run _cd \your\local\folder_
  - Run _streamlit run streamlit_crypto_forecaster.py_
  - You're done!
