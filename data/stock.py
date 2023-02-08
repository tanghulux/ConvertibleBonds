import os

import pandas_datareader.data as web
import datetime
import yfinance as yf
import pandas as pd
import akshare as ak
import sqlalchemy

#stock = yf.download('000001.SZ', datetime.datetime.strptime('2023-02-07', '%Y-%m-%d'),datetime.date.today())
#stock = yf.download('600519.SS', datetime.datetime.strptime('2023-02-07', '%Y-%m-%d'),datetime.date.today())
#stock = web.DataReader('AAPL', 'yahoo', datetime.datetime.strptime('2023-01-28', '%Y-%m-%d'),datetime.date.today())
#stock = ak.stock_zh_a_hist(symbol="600519", start_date="20230116", end_date="20230208")
stock = ak.bond_zh_hs_cov_daily(symbol="sz127079")
stock.insert(0,'symbol','127079',allow_duplicates=True)
print(stock)
current_path = os.path.dirname(__file__)
df = pd.read_excel(current_path + '/jisilu.xlsx')

for idx, row in df.iterrows():
    # 第一个是正股代码， 第二个是可转债代码
    symbol = [c.strip() for c in row['证券代码'][1:-1].replace('\'','').split(',')]
    name = [c.strip() for c in row['证券名称'][1:-1].replace('\'','').split(',')]
    # 可转债上市日期
    listing_date = row['上市公告日期']
    # 可转债配售股权登记日
    registration = row['股权登记日']
    #print(ticker, name, listing_date, registration)
    #stock = yf.download()

engine = sqlalchemy.create_engine('mysql+pymysql://root:@localhost/convertible_bond?charset=utf8')
stock.to_sql('cb_price', engine, if_exists="replace", index=False)