import os
import time

import pandas
import pandas_datareader.data as web
import datetime

import pymysql
import yfinance as yf
import pandas as pd
import akshare as ak
import sqlalchemy
import re

current_path = os.path.dirname(__file__)
df = pd.read_excel(current_path + '/jisilu.xlsx')

engine = sqlalchemy.create_engine('mysql+pymysql://root:@localhost/convertible_bond?charset=utf8')

cb_data = pd.DataFrame()

for idx, row in df.iterrows():
    # 第一个是正股代码， 第二个是可转债代码
    symbol = [c.strip() for c in row['证券代码'][1:-1].replace('\'','').split(',')]
    name = [c.strip() for c in row['证券名称'][1:-1].replace('\'','').split(',')]
    # 可转债上市日期
    listing_date = row['上市公告日期']
    # 可转债配售股权登记日, 也就是T-1日（T日是申购日）
    registration = row['股权登记日']
    sql = "select * from (select * from stock_price where symbol='" + symbol[0] + "' and date>'" + registration + "') as t limit 1"
    print(sql)
    stock = pd.read_sql(sql=sqlalchemy.text(sql), con=engine.connect())
    print(stock)
    sql = "select * from (select * from stock_price where symbol='" + symbol[0] + "' and date<='" + registration + "' order by date desc) as t limit 2"
    print(sql)
    res = pd.read_sql(sql=sqlalchemy.text(sql), con=engine.connect())
    print(res)
    stock = pd.concat([stock, res])
    print(stock)
    break
