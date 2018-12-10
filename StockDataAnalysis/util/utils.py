"""
获取沪深股市的股票名称与代码
"""

import re
import requests
from bs4 import BeautifulSoup

# 设置请求 headers
headers = {
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
}

name_code_map = {}
code_name_map = {}
with open('stocklist.txt', 'r', encoding='utf-8') as f:
  while True:
    line = f.readline()
    if not line:
      break
    parts = line.strip().split(',')
    name_code_map[parts[0]] = parts[1]
    code_name_map[parts[1]] = parts[0]

def get_stock_list():
  # 获取东方财富网的股票列表的网页内容
  stock_list_html = requests.get('http://quote.eastmoney.com/stock_list.html', headers=headers)
  # 使用 BeautifulSoup 解析
  soup = BeautifulSoup(stock_list_html.content.decode('gbk'), 'lxml')
  quotebody = soup.find('div', 'quotebody')
  # 写入文件
  with open('stocklist.txt', 'w', encoding='utf-8') as f:
    for li in quotebody.find_all('li'):
      if li.text:
        name_code = re.split('[()]', li.text)
        f.write("{},{}\n".format(name_code[0], name_code[1]))
    # 需要手动添加两项：
    # 上证指数,sh000001
    # 深证成指,399001
    f.write("上证指数,sh000001\n")
    f.write("深证成指,399001\n")

def name2code(name: str):
  if name in name_code_map:
    return name_code_map[name]
  else:
    return name

def code2name(code: str):
  if code in code_name_map:
    return code_name_map[code]
  else:
    return code

def valid_stock(code: str):
  # 表示code为股票代码
  if code in code_name_map:
    return 1
  # 表示code为股票名称
  if code in name_code_map:
    return 2
