
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pandas import DataFrame
import os

"""
# 集思录可转债数据查询地址
r = requests.get('https://www.jisilu.cn/web/data/cb/pre')
print(r.text)
"""
current_path = os.path.dirname(__file__)
try:
    with open(current_path + '/jisilu.html', 'r') as f:
        soup = BeautifulSoup(f.read(), 'lxml')
except IOError as argument:
    print(argument)
    exit(1)

# 读取一行
def readRow(tr):
    #
    res = []
    # 证券代码
    res.append(tr.select('.el-table_1_column_1 a'))
    # 证券名称
    res.append(tr.select('.el-table_1_column_2 a'))
    # 方案进展
    res.append(tr.select('.el-table_1_column_3 .color-fallgreen'))
    # 上市公告日期
    res.append(tr.select('.el-table_1_column_4 span'))
    # 发行规模（亿元）
    res.append(tr.select('.el-table_1_column_5 div'))
    # 证券类型
    res.append(tr.select('.el-table_1_column_6 div'))
    # 评级
    res.append(tr.select('.el-table_1_column_7 div'))
    # 股东配售率
    res.append(tr.select('.el-table_1_column_8 div'))
    # 转股价
    res.append(tr.select('.el-table_1_column_9 span'))
    # 正股价
    res.append(tr.select('.el-table_1_column_10 div'))
    # 正股涨幅
    res.append(tr.select('.el-table_1_column_11 span'))
    # 正股现价比转股价
    res.append(tr.select('.el-table_1_column_12 span'))
    # 正股pb
    res.append(tr.select('.el-table_1_column_13 div'))
    # 百元股票含权（元）
    res.append(tr.select('.el-table_1_column_14 span'))
    # 每股配售（元）
    res.append(tr.select('.el-table_1_column_15 div'))
    # 配售10张所需股数（股）
    res.append(tr.select('.el-table_1_column_16 span'))
    # 股权登记日
    res.append(tr.select('.el-table_1_column_17 div'))
    # 网上规模（亿元）
    res.append(tr.select('.el-table_1_column_18 div'))
    # 中签率
    res.append(tr.select('.el-table_1_column_19 div'))
    # 单账户中签（顶格）
    res.append(tr.select('.el-table_1_column_20 div'))
    # 申购户数（万户）
    res.append(tr.select('.el-table_1_column_21 span'))
    # 网下顶格（亿元）
    res.append(tr.select('.el-table_1_column_22 div'))
    # 顶格获配（万元）
    res.append(tr.select('.el-table_1_column_23 div'))
    # 网下户数（户）
    res.append(tr.select('.el-table_1_column_24 div'))
    # 包销比例
    res.append(tr.select('.el-table_1_column_25 div'))

    return res

def readCol1(col):
    return col[0].string, col[1].string

readCol2 = readCol1
def readCol3(col):
    return col[0].div['title'].replace(' ','')

def readCol4(col):
    return col[0].string

coldict = {
    1: readCol1,
    2: readCol2,
    3: readCol3,
    4: readCol4,
}
def getCol(idx, col):
    fun = coldict.get(idx, readCol4)
    return fun(col)
def readCol(tr):
    res = []
    for idx, col in enumerate(tr):
        res.append(getCol(idx+1, col))
    return res

trs = soup.select('tbody tr')
tbody = []
header = ['证券代码','证券名称','方案进展','上市公告日期','发行规模（亿元）','证券类型','评级',\
                     '股东配售率','转股价','正股价','正股涨幅','正股现价比转股价','正股pb','百元股票含权（元）',\
                     '每股配售（元）','配售10张所需股数（股）','股权登记日','网上规模（亿元）','中签率',\
                     '单账户中签（顶格）','申购户数（万户）','网下顶格（亿元）','顶格获配（万元）','网下户数（户）','包销比例']
for tr in trs:
    row = readRow(tr)
    tbody.append(readCol(row))

df = DataFrame(tbody, columns=header)
df.to_excel(current_path + '/jisilu2.xlsx', index=False)

