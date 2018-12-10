import re
import pymysql
import tushare as ts

nonedata = 0
emptystable = 0
with open('stocklist.txt', 'r', encoding='utf-8') as f:
  for i in f:
    tem = [t for t in re.split("\,|\\n", i) if t]
    data = ts.get_hist_data(tem[-1], start='2018-01-01', end='2018-12-31')
    try:
      if len(data.index)==0:
        emptystable += 1
        print(tem[-1],'is an empty table')
    except Exception as e:
        nonedata += 1
        print(tem[-1],'is none')
print("total nonedata", nonedata)
print("total emptystable", emptystable)
print("total invalid", nonedata + emptystable)