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
#stock = ak.stock_zh_a_hist(symbol="600519", start_date="20230116", end_date="20230208")
#cb = ak.bond_zh_hs_cov_daily(symbol="sz127079")
#cb.insert(0,'symbol','127079',allow_duplicates=True)
#print(cb)

current_path = os.path.dirname(__file__)
df = pd.read_excel(current_path + '/jisilu.xlsx')

# 判断可转债是深市上市还是沪市上市
def exchange(symbol):
    if(re.match('11', symbol)):
        return 'sh'
    elif(re.match('12', symbol)):
        return 'sz'
    return ''

engine = sqlalchemy.create_engine('mysql+pymysql://root:@localhost/convertible_bond?charset=utf8')
#cb.to_sql('cb_price', engine, if_exists="replace", index=False)
cb_price = pd.DataFrame()
i = 0
for idx, row in df.iterrows():
    # 第一个是正股代码， 第二个是可转债代码
    symbol = [c.strip() for c in row['证券代码'][1:-1].replace('\'','').split(',')]
    name = [c.strip() for c in row['证券名称'][1:-1].replace('\'','').split(',')]
    # 可转债上市日期
    listing_date = row['上市公告日期']
    # 可转债配售股权登记日
    registration = row['股权登记日']
    #print(symbol, name, listing_date, registration)
    cb = ak.bond_zh_hs_cov_daily(exchange(symbol[1])+symbol[1])
    # 数据库每行记录多添加两个字段，一个正股代码，一个可转债代码
    cb.insert(0, 'stock', symbol[0], allow_duplicates=True)
    cb.insert(0,'symbol',symbol[1],allow_duplicates=True)
    cb_price = pd.concat([cb_price, cb], ignore_index=True)
    i += 1
    if(i % 50 == 0):
        print("-------------------------------------------------------------------------" + str(i))
        print(cb_price.head())
        cb_price.to_sql('cb_price', engine, if_exists="append", index=False)
        cb_price = pd.DataFrame()
        time.sleep(1)
print("-------------------------------------------------------------------------" + str(i))
print(cb_price.head())
cb_price.to_sql('cb_price', engine, if_exists="append", index=False)
