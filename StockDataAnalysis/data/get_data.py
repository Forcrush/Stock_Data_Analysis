import pymysql
import tushare as ts

headers = ['date', 'open', 'high', 'close', 'low', 'volume', 'price_change', 'p_change',
           'ma5', 'ma10', 'ma20', 'v_ma5', 'v_ma10', 'v_ma20', 'turnover']

def get_hist_data_by_code(code, start='2018-01-01', end='2018-12-31'):
  if code:
    data = ts.get_hist_data(code, start, end)
    try:
      data['date'] = data.index
      # 下面开始写入数据库
      connection = pymysql.connect(host='localhost',
                           user='root',
                           password='970827',
                           db='finance',
                           charset='utf8mb4')
      try:
        with connection.cursor() as cursor:
          sql = """SELECT * FROM `{}`""".format(code)
          cursor.execute(sql)
          results = cursor.fetchone()
          if not results:
            print("无数据！ 等待插入数据...")
      except Exception as e:
        print("创建数据表...")
        with connection.cursor() as cursor_ex:
          sql_create_datatable = """CREATE TABLE `{}`
                                    (
                                      date         DATE   NOT NULL
                                        PRIMARY KEY,
                                      open         DOUBLE NULL,
                                      high         DOUBLE NULL,
                                      close        DOUBLE NULL,
                                      low          DOUBLE NULL,
                                      volume       DOUBLE NULL,
                                      price_change DOUBLE NULL,
                                      p_change     DOUBLE NULL,
                                      ma5          DOUBLE NULL,
                                      ma10         DOUBLE NULL,
                                      ma20         DOUBLE NULL,
                                      v_ma5        DOUBLE NULL,
                                      v_ma10       DOUBLE NULL,
                                      v_ma20       DOUBLE NULL,
                                      turnover     DOUBLE NULL
                                    )
                                      ENGINE = InnoDB;""".format(code)
          cursor_ex.execute(sql_create_datatable)
          print("数据表已创建！")
      # 将股票信息写入数据库
      print('写入数据...')
      with connection.cursor() as cursor_write:
        sql_check = """SELECT * FROM `{}` WHERE `date` = '{}'"""
        total_length = len(data)
        for i in range(total_length):
          current_date = data.iloc[i].date
          cursor_write.execute(sql_check.format(code, current_date))
          r = cursor_write.fetchone()
          if r:
            # 该日期的数据已经存在了，所以不需要重复插入了
            print("重复数据，终止插入！")
            break
          else:
            turnover = 0.0
            if 'turnover' in data.columns:
              turnover = data.iloc[i].turnover
            sql_insert = """INSERT INTO `{}` (`date`, `open`, `high`, `close`, `low`, `volume`, `price_change`, `p_change`,
                              `ma5`, `ma10`, `ma20`, `v_ma5`, `v_ma10`, `v_ma20`, `turnover`) VALUES 
                            ('{}', {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});""".format(
              code, data.iloc[i].date, data.iloc[i].open, data.iloc[i].high, data.iloc[i].close, data.iloc[i].low,
              data.iloc[i].volume, data.iloc[i].price_change, data.iloc[i].p_change,
              data.iloc[i].ma5, data.iloc[i].ma10, data.iloc[i].ma20, data.iloc[i].v_ma5, data.iloc[i].v_ma10, data.iloc[i].v_ma20,
              turnover)
            try:
              cursor_write.execute(sql_insert)
              connection.commit()
            except:
              connection.rollback()
    except Exception as e:
      print(e,'(无法爬取到数据，此基金或已不存在！)')