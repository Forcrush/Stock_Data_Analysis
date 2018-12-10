## 基于 Python 的沪深市场股票数据分析


### 运行环境

* Windows 8.1 64 位系统 

* Python 3.5.x ( 64 位)

* MySQL 8.0.12

* PyCharm 2018.1.3

**注意：**

* **1. 涉及到中文文本的处理，请使用 UTF-8 编码！**

* **2. 部分路径设置需根据实际情况进行调整！（`initialize.py` 和 `analysis.py` 中词典路径）**

* **3. MySQL的用户名和密码需手动修改**


### 项目结构

该项目是使用 python 语言，使用基于 Django 开发的 Web 界面，主要结构如下：

* `analysis` 包，进行股票数据的分析
* `data` 包，获取股票数据并处理
* `fin` 包，基于 Django 框架的主要业务逻辑与后端处理
* `Finance` 包，项目的相关设置
* `static` 文件夹，网页端使用到的 css 样式和一些 js 代码，用于渲染网页
* `templates` 文件夹，html 网页代码，通过 Django 注入数据，作为前端 UI
* `util` 包，爬取股票数据并提供一些小的功能函数
* `db.sqlite3`，Django 默认的一个数据库设置
* `initialize.py`，初始化项目，预准备数据
* `manage.py`，Django Web 运行的入口
* `stocklist.txt`，保存了沪深股票的股票代码和股票名称，由`initialize.py`运行后得到


### 主要代码文件

* `__init__.py` 表明这个文件夹是一个 python 包

* `analysis` 中的 `analysis.py`，实现四个函数，`analysis_stock` 根据股票代码，查找数据库并从外部获取最新的股票行情，得到实际股价、预测股价等数据；`analysis_stock_news` 则根据选择的股票，从新浪股吧获取股民的讨论，综合这些讨论分析情感记性，预测涨或者跌的可能性；`extract_keywords`根据文本信息提取关键词；`analysis_bull_or_bear`根据预测出的数据分析牛熊市概率

* `data` 中的 `get_data.py`，获取对应股票的一定时间段内的行情，并保存在本地 MySQL 数据库中；`invalid_stock_check.py`返回沪深股市中的无效股票（爬不到数据的股票或是无数据的股票），并将结果存在`invalid_stocks.txt`中

* `fin` 中，主要是 `views.py`，根据前端的数据，后台处理，并返回处理结果（预测股价等信息），供前端解析渲染，其他的文件都是 Django 项目创建时生成的；此外，`Finance` 中的代码中，也基本上保持 Django 项目创建时的内容，仅需要在 `urls.py`中添加一些路径映射

* `static` 下的 `js/stock.js`，`js/stock1.js`，`js/stock2.js`等可以根据数据在前端异步渲染数据

* `templates` 下的 `index.html` 为网页元素布局

* `util` 下的 `utils.py` 中实现了一些辅助函数，`get_stock_list` 可以爬取数据并生成股票名称与代码文件：`stocklist.txt`


### 准备工作

1. 安装好所需 python 包：

* `numpy`

* `pandas`

* `scipy`

* `scikit-learn`

* `lxml`

* `requests`

* `beautifulsoup4`

* `pymysql`

* `snownlp`

* `jieba`

* `Django`

* `djangorestframework`

2. 搭建好 MySQL 数据库，设置好数据库的用户名和密码，在 `data/get_data.py` 和 `analysis/analysis.py` 中的相关代码处填入对应的用户名、密码及地址（localhost），端口（port，默认为 3306），并在MySQL中创建数据库 `create database finance`

3. 运行 `initialize.py`（这一步比较耗时但只需执行一次），爬取数据写入本地数据库并生成`stocklist.txt`


### 程序运行方式

运行前记得先启动数据库服务 `net start mysql80`， mysql80 为要连接的服务器名（关闭数据库连接为 `net stop mysql80`）

可以通过 PyCharm 打开（两种方式）：

* 直接运行 Django 项目

* 运行 `manage.py`，主要运行时需要将参数设置为 `runserver 8000`

通过命令行运行：

* `cd` 到 `manage.py` 目录下，执行指令 `python manage.py runserver 8000`


### Web UI 演示运行

上述两种方式运行完毕后，若出现如下的提示，可以访问 <http://127.0.0.1:8000> ，看到项目的 UI 界面，根据内容直接在网页上操作即可

```
December 10, 2018 - 13:07:42
Django version 2.1.4, using settings 'Finance.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```