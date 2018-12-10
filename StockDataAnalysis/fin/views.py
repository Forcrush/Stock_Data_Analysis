import pymysql
import re
from django.shortcuts import render

# Create your views here.
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

from analysis import analysis
from util import utils

class HomeView(View):
  def get(self, request, *args, **kwargs):
    return render(request, 'index.html')

class GetData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
      data = {}
      print(request.GET)
      # 默认是获取上证指数
      stock_info = request.GET.get('stockid', 'sh000001 -- 50')
      stock_id = utils.name2code(re.split('\-|\ |\，|\,|\:|\.', stock_info.strip())[0])
      stock_day = int(re.split('\-|\ |\，|\,|\:|\.', stock_info.strip())[-1])
      stock_idp = request.GET.get('stockmid', 'sh000001')
      stock_idp = utils.name2code(stock_idp)
      stock_kw = request.GET.get('stocknid', 'Chitarra')
      stock_kw = analysis.extract_keywords(stock_kw.strip())
      if stock_kw == None:
        data['text'] = 'None'
      else:
        data['text'] = stock_kw
      if utils.valid_stock(stock_id) or stock_id == 'sh000001' or utils.valid_stock(stock_idp) or stock_idp == 'sh000001':
        # 对于数据库空表(无数据股票)
        if analysis.analysis_stock(stock_id, stock_day) == None:
          data['stockname'] = utils.code2name(stock_id) + ' (' + stock_id + ')'
          data['open'] = 0
          data['open_pred'] = 0
          data['close'] = 0
          data['close_pred'] = 0
          data['x_ax'] = 0
          data['ymin'] = 0
          data['ymax'] = 0
          data['y_open'] = 0
          data['y_close'] = 0
          data['delta'] = 0
          data['delta_percent'] = 0
          data['flag'] = 0

          return Response(data)

        if analysis.analysis_stock(stock_idp) == None:
          data['stocknamep'] = utils.code2name(stock_idp) + ' (' + stock_idp + ')'
          data['openp'] = 0
          data['open_predp'] = 0
          data['closep'] = 0
          data['close_predp'] = 0
          data['x_axp'] = 0
          data['yminp'] = 0
          data['ymaxp'] = 0
          data['y_openp'] = 0
          data['y_closep'] = 0
          data['deltap'] = 0
          data['delta_percentp'] = 0
          data['flag'] = 0
          data['senti'] = '0 (近期无人讨论，估计已凉，不推荐投资)'

          return Response(data)

        # 此部分为第一个按钮功能实现
        open_list, open_pred_list, close_list, close_pred_list, y_open, y_close = analysis.analysis_stock(stock_id, stock_day)
        data['stockname'] = utils.code2name(stock_id) + ' (' + stock_id + ')'
        data['open'] = [round(x, 2) for x in open_list]
        data['open_pred'] = [round(x, 2) for x in open_pred_list]
        data['close'] = [round(x, 2) for x in close_list]
        data['close_pred'] = [round(x, 2) for x in close_pred_list]
        data['x_ax'] = list(range(1, len(open_list) + 1))
        data['ymin'] = round(min(open_list + open_pred_list + close_list + close_pred_list) * 0.85, 2)
        data['ymax'] = round(max(open_list + open_pred_list + close_list + close_pred_list) * 1.15, 2)
        data['y_open'] = round(y_open, 2)
        data['y_close'] = round(y_close, 2)
        data['delta'] = round(y_close - y_open, 2)
        data['delta_percent'] = round(round(y_close - y_open, 2) / y_open * 100.0, 2)

        # 此部分为第二个按钮功能实现
        open_listp, open_pred_listp, close_listp, close_pred_listp, y_openp, y_closep = analysis.analysis_stock(stock_idp, stock_day)
        bull, bear = analysis.analysis_bull_or_bear(y_openp, y_closep)
        senti = analysis.analysis_stock_news(stock_idp)
        data['stocknamep'] = utils.code2name(stock_idp) + ' (' + stock_idp + ')'
        data['openp'] = [round(x, 2) for x in open_listp]
        data['open_predp'] = [round(x, 2) for x in open_pred_listp]
        data['closep'] = [round(x, 2) for x in close_listp]
        data['close_predp'] = [round(x, 2) for x in close_pred_listp]
        data['x_axp'] = list(range(1, len(open_listp) + 1))
        data['yminp'] = round(min(open_listp + open_pred_listp + close_listp + close_pred_listp) * 0.85, 2)
        data['ymaxp'] = round(max(open_listp + open_pred_listp + close_listp + close_pred_listp) * 1.15, 2)
        data['y_openp'] = round(y_openp, 2)
        data['y_closep'] = round(y_closep, 2)
        data['deltap'] = round(y_closep - y_openp, 2)
        data['delta_percentp'] = round(round(y_closep - y_openp, 2) / y_openp * 100.0, 2)
        data['flag'] = 1
        data['bull'] = "%.5f" % bull  # string
        data['bear'] = "%.5f" % bear  # string
        data['stable'] = "%.5f" % (1 - float("%.5f" % bull) - float("%.5f" % bear))
        data['senti'] = round(senti, 2) if y_closep > y_openp else round(1.0 - senti, 2)


      else:
          data['error_message'] = '请输入正确的股票代码或股票名称！'

      return Response(data)

