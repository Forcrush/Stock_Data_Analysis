import re
from util import utils
from data import get_data
from analysis import analysis


def add_stock_to_dict():
  # 将股票名称及代码加入jieba词典
  namecode = []
  with open('stocklist.txt', 'r', encoding='utf-8') as f:
    for i in f:
      tem = [t for t in re.split("\,|\\n", i) if t]
      namecode.extend(tem)

  # 此处需修改路径，对应为jieba包所在绝对路径
  with open('C:\Python35\Lib\site-packages\jieba\mydict.txt', 'w', encoding='utf-8') as f:
    f.write("{} 1 n\n".format(i))


def add_stock_to_mysql():
  # 将股票信息写入数据库
  with open('stocklist.txt', 'r', encoding='utf-8') as f:
    for i in f:
      tem = [t for t in re.split("\,|\\n", i) if t]
      get_data.get_hist_data_by_code(tem[-1])


if __name__ == '__main__':
  # 获取股票代码和名称的映射 
  # utils.get_stock_list()

  # add_stock_to_dict()
  # add_stock_to_mysql()

  # 以上为初始化函数 运行一次即可

  # 下列为测试函数 检测是否初始化成功
  # get_data.get_hist_data_by_code('500039')
  # print(analysis.analysis_stock_news('500039'))
  # print(analysis.extract_keywords("基金金泰sh000001受到204004波动，GC004股票进入牛市"))
  