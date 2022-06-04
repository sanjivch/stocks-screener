# Stocks Screener and Predictor

This repo use Plotly-dash to screen and predict stocks. yFinance library is used to fetch the data for the stocks. only the top 200 NSE listed stocks are analysed in this project.

The python code for this project consist of the following files

1. `app.py` - Flask server to run the Dash application
2. `stocks.py` - contains the list of top 200 NSE stocks
3. `model.py` - Machine learning model to forecast stock price. TODO

## Folder structure

├── stocks-screener-and-predictor
    ├── assets
    │    └── app.css
    ├── app.py
    ├── model.py
    ├── stocks.py
    ├── Procfile
    ├── requirements.txt
    ├── LICENSE
    └── README.md

## Python libraries used

- Plotly
- Dash
- dash_mantine_components
- dash_iconify
- datetime
- yfinance
- pandas
- plotly_express
