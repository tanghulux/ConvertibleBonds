import os

import pandas_datareader.data as web
import datetime
import yfinance as yf
import pandas as pd

stock = yf.download('127079.SS', datetime.datetime.strptime('2023-02-07', '%Y-%m-%d'),datetime.date.today())
#stock = yf.download('600519.SS', datetime.datetime.strptime('2023-02-07', '%Y-%m-%d'),datetime.date.today())
#stock = web.DataReader('AAPL', 'yahoo', datetime.datetime.strptime('2023-01-28', '%Y-%m-%d'),datetime.date.today())
print(stock)
current_path = os.path.dirname(__file__)
df = pd.read_excel(current_path + '/jisilu.xlsx')

for idx, row in df.iterrows():
    # 第一个是正股代码， 第二个是可转债代码
    ticker = [c.strip() for c in row['证券代码'][1:-1].replace('\'','').split(',')]
    name = [c.strip() for c in row['证券名称'][1:-1].replace('\'','').split(',')]
    # 可转债上市日期
    listing_date = row['上市公告日期']
    # 可转债配售股权登记日
    registration = row['股权登记日']
    #print(ticker, name, listing_date, registration)
    #stock = yf.download()