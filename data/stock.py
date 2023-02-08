import os
import time

import pandas
import pandas_datareader.data as web
import datetime
import yfinance as yf
import pandas as pd
import akshare as ak
import sqlalchemy
import re

#stock = yf.download('000001.SZ', datetime.datetime.strptime('2023-02-07', '%Y-%m-%d'),datetime.date.today())
#stock = yf.download('600519.SS', datetime.datetime.strptime('2023-02-07', '%Y-%m-%d'),datetime.date.today())
#stock = web.DataReader('AAPL', 'yahoo', datetime.datetime.strptime('2023-01-28', '%Y-%m-%d'),datetime.date.today())
#stock = ak.stock_zh_a_hist(symbol="003043", start_date="20221115", end_date="20230114")
#print(stock)

current_path = os.path.dirname(__file__)
df = pd.read_excel(current_path + '/jisilu.xlsx')

engine = sqlalchemy.create_engine('mysql+pymysql://root:@localhost/convertible_bond?charset=utf8')

stock_price = pd.DataFrame()
i = 0
for idx, row in df.iterrows():
    # 第一个是正股代码， 第二个是可转债代码
    symbol = [c.strip() for c in row['证券代码'][1:-1].replace('\'','').split(',')]
    name = [c.strip() for c in row['证券名称'][1:-1].replace('\'','').split(',')]
    # 可转债上市日期
    listing_date = row['上市公告日期']
    # 可转债配售股权登记日, 也就是T-1日（T日是申购日）
    registration = row['股权登记日']
    #print(symbol, name, listing_date, registration)
    registr = datetime.datetime.strptime(registration, "%Y-%m-%d")
    # 要抓取T日前后几个交易日的股价，但是股市开市可能受休息日的影响，这里时间间隔取大一点
    t_start = (registr - datetime.timedelta(days=30)).strftime("%Y%m%d")
    t_end = (registr + datetime.timedelta(days=30)).strftime("%Y%m%d")
    #print(t_start, t_end)
    stock = ak.stock_zh_a_hist(symbol=symbol[0], start_date=t_start, end_date=t_end)
    if(stock.empty):
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        print(symbol[0])
    stock.drop(stock.columns[6:], axis=1, inplace=True)
    stock.columns = ['date', 'open', 'close', 'high', 'low', 'volume']
    stock.insert(0, 'symbol', symbol[0], allow_duplicates=True)

    stock_price = pd.concat([stock_price, stock], ignore_index=True)
    i += 1
    if (i % 50 == 0):
        print("-------------------------------------------------------------------------" + str(i))
        print(stock_price.head())
        stock_price.to_sql('stock_price', engine, if_exists="append", index=False)
        stock_price = pd.DataFrame()
        time.sleep(1)
print("-------------------------------------------------------------------------" + str(i))
print(stock_price.head())
stock_price.to_sql('stock_price', engine, if_exists="append", index=False)
