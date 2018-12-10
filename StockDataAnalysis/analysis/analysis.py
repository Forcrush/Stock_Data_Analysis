import numpy as np
import pymysql
import pandas as pd
import re
import requests
import jieba.analyse
from bs4 import BeautifulSoup
from snownlp import SnowNLP
from sklearn.svm import SVR

import util.utils as ut
from data.get_data import get_hist_data_by_code


headers = ['date', 'open', 'high', 'close', 'low', 'volume', 'price_change', 'p_change',
          'ma5', 'ma10', 'ma20', 'v_ma5', 'v_ma10', 'v_ma20', 'turnover']


def analysis_stock(code, recentdays=50, days=15):
  con = pymysql.connect(host='localhost',
                        user='root',
                        password='970827',
                        db='finance',
                        charset='utf8mb4')
  get_hist_data_by_code(code)
  try:
    with con.cursor() as cursor:
      sql = """SELECT * FROM `{}` ORDER BY `date` ASC""".format(code)
      cursor.execute(sql)
      # 数据库的信息放入 pandas DataFrame 之中，再转化为 numpy 数组，方便数据划分等操作
      field_names = [i[0] for i in cursor.description]
      get_data = [xx for xx in cursor]
      df = pd.DataFrame(get_data)
      df.columns = field_names
      df = df.drop('date', axis=1)
      data = df.as_matrix()
      all_days = len(data)
      # 选择 recentdays 的数据量，加上默认 15 的偏置
      if all_days > recentdays + days:
        data = data[-(recentdays+days):, :]
        all_days = recentdays + days
      X = []
      y_open = []
      y_close = []
      X_ax = []
      for i in range(all_days-days):
        X_i = data[i:i+days, :]
        y_open_i = data[i+days, 0]
        y_close_i = data[i+days, 2]
        X.append(X_i.flatten())
        y_open.append(y_open_i)
        y_close.append(y_close_i)
        X_ax.append(i+1)
      X_train = np.array(X, dtype=np.float32)
      y_open_train = np.array(y_open, dtype=np.float32)
      y_close_train = np.array(y_close, dtype=np.float32)

      print("Train model of open-price...")
      svr_open = SVR(kernel='rbf', C=1e3, gamma=0.1)
      svr_open.fit(X_train, y_open_train)
      y_open_pred = svr_open.predict(X_train)
      
      print("Train model of close-price......")
      svr_close = SVR(kernel='rbf', C=1e3, gamma=0.1)
      svr_close.fit(X_train, y_close_train)
      y_close_pred = svr_close.predict(X_train)

      X_test = data[-days:, :].flatten().reshape(1, -1)
      y_open_test = svr_open.predict(X_test)
      y_close_test = svr_close.predict(X_test)

      # print(y_open_train.tolist())
      # print(y_open_pred.tolist())
      # print(y_close_train.tolist())
      # print(y_close_pred.tolist())
      # print(y_open_test[0])
      # print(y_close_test[0])

      y_open_pred_test = y_open_test[0]
      y_close_pred_test = y_close_test[0]

      return y_open_train.tolist(), y_open_pred.tolist(), y_close_train.tolist(), y_close_pred.tolist(), \
             y_open_pred_test, y_close_pred_test


  except Exception as e:
    print(e)
    print("Database Error!")


def analysis_stock_news(code):
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
  }
  params = {'s': 'bar', 'name': code}
  # 从新浪股吧获取一些用户的讨论
  guba_html = requests.get('http://guba.sina.com.cn', params=params, headers=headers)
  # 使用 BeautifulSoup 解析
  soup = BeautifulSoup(guba_html.content.decode('gbk'), 'lxml')
  contents = soup.find('div', 'table_content') # 'b_cont'
  all_text = []
  for a_tags in contents.find_all('a', re.compile('link*')):
    all_text.append(a_tags.text)
  # 计算每一篇讨论的情感值，得到一个平均值
  all_sentiment = [SnowNLP(x).sentiments for x in all_text]
  # print(all_text)
  # print(all_sentiment)
  if len(all_sentiment)==0:
    return 0
  return (sum(all_sentiment) / len(all_sentiment))


def extract_keywords(text):
  # 导入股票名称及代码词典
  jieba.load_userdict("C:\Python35\Lib\site-packages\jieba\mydict.txt")

  tags = jieba.analyse.extract_tags(text, topK=5)
  keywords = []
  for item in tags:
    if ut.valid_stock(item) == 1:
      keywords.append('{}({})'.format(ut.code2name(item), item))
    if ut.valid_stock(item) == 2:
      keywords.append('{}({})'.format(item, ut.name2code(item)))
  nkw = list(set(keywords))
  newnext = ''
  # 无任何股票关键词
  if len(nkw) == 0:
    return None
  # 只有单个股票关键词
  elif len(nkw) == 1:
    return nkw[0]
  # 有多个股票关键词
  else:
    for i in nkw[:-1]:
      newnext += i
      newnext += '，'
    newnext += nkw[-1]
    return newnext


def analysis_bull_or_bear(open, close):
  if close - open == 0:
    # 牛市概率，熊市概率
    return 0.30, 0.30

  # 用分段线性函数拟合（简单版）
  elif close - open > 0:
    ratio = (close - open) / open
    if ratio > 0.5:
      if ratio > 1:
        bull = 0.95
      else:
        bull = 0.9 * ratio + 0.05
    else:
        bull = 0.2 * ratio + 0.4
    bear = (1 - bull) / 3
    return round(bull, 5), round(bear, 5)

  else:
    ratio = (open - close) / open
    if ratio > 0.5:
      if ratio > 1:
        bear = 0.95
      else:
        bear = 0.9 * ratio + 0.05
    else:
        bear = 0.2 * ratio + 0.4
    bull = (1 - bear) / 3
    return round(bull, 5), round(bear, 5)
