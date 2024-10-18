import yfinance as yf
import pandas as pd


ticker = yf.Ticker("NVDA")
nvidia = ticker.history(period="max")
nvidia['Date'] = nvidia.index
nvidia['Year'] = nvidia['Date'].dt.year

pd.DataFrame(nvidia).to_csv('data/NVIDIA.csv')