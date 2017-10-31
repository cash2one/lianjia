#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import pymysql
import time
import re
from time import sleep
import random

requests_xiaoqu_url = 'http://bj.lianjia.com/xiaoqu/'
sql_list = []
# 链家网站变量
#re_xiaoqu_id = 'a href="http://bj.lianjia.com/xiaoqu/([0-9]{13})/"'
re_xiaoqu_id = '([0-9]{14,20})/" class'
re_xiaoqu_name = 'alt="(.+)"'
re_avg_price = '"totalPrice"><span>(.+)</span>'
re_bulit_year = 'nbsp;(.+)'+ '年建成'.decode("utf8")
re_county = 'class="district" title="(.+)'+ '小区'.decode("utf8")
re_district = 'class="bizcircle" title="(.+)' + '小区'.decode("utf8")
re_current_sale = 'class="totalSellCount"><span>([0-9]{1,3})</span>'
re_thirtydays_deal = '30天成交'.decode("utf8") + '([0-9]{1,3})' + '套'.decode("utf8")
#re_xiaoqu_url = 'a href="(http://bj.lianjia.com/xiaoqu/[0-9]{13}/)"'

# 代理服务器
proxy_list = [{"http": "http://101.200.1.235:731"},\
                {"http": "http://101.201.152.116:731"},\
                {"http": "http://182.92.4.179:731"},\
                {"http": "http://123.56.87.39:731"},\
                {"http": "http://123.56.114.204:731"}]
#proxy_list = [{"http": "http://101.201.152.116:731"},\
#                {"http": "http://182.92.4.179:731"},\
#                {"http": "http://123.56.87.39:731"},\
#                {"http": "http://123.56.114.204:731"}]
proxy = {'index': 0}
# 每爬取10个页面，换一次代理
def round_proxy(page):
    if page % 10 == 0:
	if proxy['index'] < 4:
	    proxy['index'] += 1
	else:
	    proxy['index'] = 0


# 网站访问session
def request_session(xiaoqu_url, current_proxy):
    headers = {
            'Host': 'bj.lianjia.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
            }
    session = requests.Session()
    s = session.get(xiaoqu_url, headers=headers, proxies=current_proxy, timeout=10)
    s.encoding = 'utf-8'
    return s

# 批量生成sql语句
def generate_sql(s_page):
    page_text = s_page.text
    xiaoqu_id_list = re.findall(re_xiaoqu_id, page_text) 		# 数字小区ID
    xiaoqu_name_list = re.findall(re_xiaoqu_name, page_text)	# 中文小区名
    avg_price_list = re.findall(re_avg_price, page_text) 		# 数字小区价格
    bulit_year_list = re.findall(re_bulit_year, page_text) 	# 数字小区年份
    county_list = re.findall(re_county, page_text) 		# 中文小区区县
    district_list = re.findall(re_district, page_text) 		# 中文小区片区
    current_sale_list = re.findall(re_current_sale, page_text) 	# 数字小区套数
    thirtydays_deal_list = re.findall(re_thirtydays_deal, page_text) # 数字小区套数
    #xiaoqu_url_list = re.findall(re_xiaoqu_url, page_text) 	# url小区链接
    #print len(xiaoqu_id_list), xiaoqu_url_list

    # 生成每一页的sql_list
    for i in range(len(xiaoqu_id_list)):
	xiaoqu_id = xiaoqu_id_list[i]
	xiaoqu_name = xiaoqu_name_list[i]
	# 有的小区均价未知，显示'暂无参考均价'
	if avg_price_list[i].isdigit():
	    avg_price = avg_price_list[i]
	else:
	    avg_price = 0
	# 有的小区年限未知，显示'未知年建成'
	if bulit_year_list[i].isdigit():
	    bulit_year = bulit_year_list[i]
	else:
	    bulit_year = 0
	county = county_list[i]
	district = district_list[i]
	current_sale = current_sale_list[i]
	thirtydays_deal = thirtydays_deal_list[i]
	#xiaoqu_url = xiaoqu_url_list[i]
	#sql = u'insert into lj_xiaoqu values( NULL, \''\
	#	+ xiaoqu_id + '\', \''\
	#	+ xiaoqu_name + '\', \''\
	#	+ avg_price + '\', \''\
	#	+ bulit_year + '\', \''\
	#	+ county + '\', \''\
	#	+ district + '\', \''\
	#	+ current_sale + '\', \''\
	#	+ thirtydays_deal + '\', \''\
	#	+ xiaoqu_url + '\');'

	sql = u'insert into lj_xiaoqu values( NULL, \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\');'\
		.format(xiaoqu_id,\
		xiaoqu_name,\
		avg_price,\
		bulit_year,\
		county,\
		district,\
		current_sale,\
		thirtydays_deal)
	#sleep(1)
	sql_list.append(sql)

def db_insert(sql_list):
    set_utf8_sql = "set character_set_client='utf8';\
		set character_set_filesystem='utf8';\
		set character_set_results=utf8;\
		set character_set_connection=utf8;\
		set character_set_database=utf8;"

    s_connect = pymysql.connect(host='rdsdld66mt04nt1lt3k5o.mysql.rds.aliyuncs.com',
		port=3306,
		user='lianjia_user',
		passwd='JN7lebwqHhwCtYGq',
		db='lianjia_db',
		charset='utf8mb4',
		cursorclass=pymysql.cursors.DictCursor,
		autocommit=False,)
    
    try:
        with s_connect.cursor() as s_cursor:
	    s_cursor.execute(set_utf8_sql)
	    # 从每一页的sql_list中读取sql，然后插入数据库
	    for sql in sql_list:
            	s_cursor.execute(sql)
            s_connect.commit()
    finally:
	s_connect.close()

if __name__ == '__main__':
    f = open('page_list.txt', 'r')
    page = 0
    for xiaoqu_page_url in f:
        #xiaoqu_page_url = "http://bj.lianjia.com/xiaoqu/dongcheng/pg14/"
        page += 1
        xiaoqu_page_url = xiaoqu_page_url.strip('\n')
        # 获取当前proxy的索引号（每10个页面换一次）
        current_proxy_index = round_proxy(page)
        # 针对每一个页面，生成访问session
        s_page = request_session(xiaoqu_page_url, proxy_list[proxy['index']])
        # 针对每一个页面中的30个小区，生成小区详情sql语句
        generate_sql(s_page)
        # 针对每一个页面的sql列表（30个sql语句），插入数据库
        db_insert(sql_list)
        
        # 以计数方式显示执行进程，并打印到屏幕
        print 'page %d:  %d sql insert is done.' % (page, len(sql_list))
        # 每一页的sql执行完之后，清空sql_list
        sql_list = []
        # 每个页面之间随机睡眠3到18秒
        sleep(random.randint(8, 23))

