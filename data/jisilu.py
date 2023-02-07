
import requests
from bs4 import BeautifulSoup
from datetime import datetime

"""
# 集思录可转债数据查询地址
r = requests.get('https://www.jisilu.cn/web/data/cb/pre')
print(r.text)
"""

try:
    with open('/Users/tanghulux/Programs/pythonProjects/ConvertibleBonds/data/jisilu.html', 'r') as f:
        soup = BeautifulSoup(f.read(), 'lxml')
except IOError as argument:
    print(argument)
    exit(1)

trs = soup.select('tbody tr')

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
    # 配售10张所需股数 （股）
    res.append(tr.select('.el-table_1_column_16 span'))
    # 股权登记日
    res.append(tr.select('.el-table_1_column_17 div'))
    # 网上规模 （亿元）
    res.append(tr.select('.el-table_1_column_18 div'))
    # 中签率
    res.append(tr.select('.el-table_1_column_19 div'))
    # 单账户中签（顶格）
    res.append(tr.select('.el-table_1_column_20 div'))
    # 申购户数 （万户）
    res.append(tr.select('.el-table_1_column_21 span'))
    # 网下顶格 （亿元）
    res.append(tr.select('.el-table_1_column_22 div'))
    # 顶格获配（万元）
    res.append(tr.select('.el-table_1_column_23 div'))
    # 网下户数（户）
    res.append(tr.select('.el-table_1_column_24 div'))
    # 包销比例
    res.append(tr.select('.el-table_1_column_25 div'))

    return res

i = 0
for tr in trs:
    #
    res = readRow(tr)
    for j in res:
        print(j)
    if i == 0:
        break

