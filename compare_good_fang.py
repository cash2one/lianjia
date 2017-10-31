#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import pymysql
import time
import re
import subprocess as subp
from time import sleep
import random

# 核心变量 
bj_value_price = 3000
bj_chengqu_id = 0
#search_key = '/co32ng1hu1nb1lc1lc2lc3lc5sf1ba30ea140bp100ep1000'
process_num = 1
# 新上，200万到500万，30平到100平, 非底层
search_key = 'tt2lc1lc2lc3lc5sf1ba30ea100bp200ep500'
# 链家网站变量
page_url_list = []
bj_chengqu_list = ['dongcheng', #1
                'xicheng', 	#2
                'chaoyang', 	#3
                'haidian', 	#4
                'fengtai', 	#5
                'shijingshan', 	#6
                'tongzhou', 	#7
                'changping', 	#8
                'daxing', 	#9
                'yizhuangkaifaqu',#10 
                'shunyi', 	#11
                'fangshan', 	#12
                'mentougou', 	#13
                'pinggu', 	#14
                'huairou', 	#15
                'miyun', 	#16
                'yanqing', 	#17
                'yanjiao',	#18
		'']		#0
ershoufang_url = "http://bj.lianjia.com/ershoufang/"
page_abb = '/pg'
re_xiaoqu_id = 'xiaoqu/([0-9]{13,20})'
re_fang_id = '\<a class=\"img \" href="http://bj\.lianjia\.com/ershoufang/([0-9]{12,20})\.html'
re_fang_url = '\<a class=\"img \" href="(http://bj\.lianjia\.com/ershoufang/[0-9]{12,20}\.html)'
#re_xiaoqu_price = 'xiaoquUnitPrice\">([0-9]{5,6})'
re_danjia_price = 'data-price=\"([0-9]{5,6})\"'
re_totalpage = '"totalPage":([0-9]{1,3})'
# 组合城区url
chengqu = bj_chengqu_list[bj_chengqu_id - 1]
chengqu_url = ershoufang_url + chengqu + search_key

# 代理服务器列表
proxy_list = [{"http": "http://101.200.177.178:731"}, \
		{"http": "http://101.200.1.235:731"}, \
		{"http": "http://101.201.152.116:731"}, \
		{"http": "http://182.92.4.179:731"}, \
		{"http": "http://123.56.87.39:731"}, \
		{"http": "http://123.56.114.204:731"}]
#proxy_list = [{"http": "http://101.200.1.235:731"}, \
#		{"http": "http://101.201.152.116:731"}, \
#		{"http": "http://182.92.4.179:731"}, \
#		{"http": "http://123.56.87.39:731"}, \
#		{"http": "http://123.56.114.204:731"}]
proxy = {'index': random.randint(0,5)}
# 每爬取10个页面，换一次代理
def round_proxy(page):
    if page % 10 == 0:
        if proxy['index'] < 5:
            proxy['index'] += 1
        else:
            proxy['index'] = 0


#* 获取总页数,并生成所有页面链接
def generate_page_url_list():
    headers = {
            'Host': 'bj.lianjia.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
            }
    session = requests.Session()
    s = session.get(chengqu_url, headers=headers, timeout=60)
    s.encoding = 'utf-8'
    # 根据城区url生成所有页面的url
    totalpage = re.findall(re_totalpage, s.text)
    for page in range(1, int(totalpage[0]) + 1):
        page_url = ershoufang_url \
                + chengqu \
                + page_abb \
                + str(page) \
                + search_key
        page_url_list.append(page_url)

#* 通过小区id，从数据库中读取当前小区均价
def db_xiaoqu_avg_price(xiaoqu_id):
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
            sql = "select avg_price from lj_xiaoqu where xiaoqu_id=" + str(xiaoqu_id) + ";"
	    # 从数据库中查询相应id的小区均价
            s_cursor.execute(sql)
            s_result = s_cursor.fetchall()
	    if s_result:
                return s_result[0]['avg_price']
	    else:
		return 0
    finally:
        s_connect.close()

#* 将好房源的id和url写入数据库
def db_insert_good_fang(fang_id, fang_url):
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
	    s_sql = "SELECT id FROM lj_good_fang_url where fang_id=" + str(fang_id) + ";"
            i_sql = "insert into lj_good_fang_url values(NULL, '" + str(fang_id) + '\', \'' + fang_url + "\');"
	    l_sql = "insert into lj_good_fang_url values(NULL, '0', '---------------------------------------------');"
            # 从数据库中查询相应id的小区均价
            s_cursor.execute(s_sql)
	    s_result = s_cursor.fetchall()
	    if not s_result:
		s_cursor.execute(i_sql)
		s_connect.commit()
		shell_mail_cmd = 'echo "' + fang_url + '" | mail -s "new good fang url" zmqtb2008@126.com'
		subp.Popen(shell_mail_cmd, stdout=subp.PIPE, stderr=subp.PIPE, shell=True)
    finally:
        s_connect.close()
    
#* 初始网站访问session
def request_session(fang_url, current_proxy):
    agent_list=[
    	{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
    	{'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
    	{'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},\
    	{'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},\
    	{'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},\
    	{'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    	{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    	{'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},\
    	{'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    	{'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    	{'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},\
    	{'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},\
    	{'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}
    	]
    
    headers = {
            'Host': 'bj.lianjia.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            }
    headers['User-Agent'] = random.choice(agent_list)['User-Agent']
    session = requests.Session()
    s = session.get(fang_url, headers=headers, proxies=current_proxy, timeout=60)
    s.encoding = 'utf-8'
    return s

#* 对比房屋单价和小区均价，并打印指的投资的房子链接及价格详情
def compare_price(s_page):
    fang_id_list = re.findall(re_fang_id, s_page.text)
    fang_url_list = re.findall(re_fang_url, s_page.text)
    xiaoqu_id_list = re.findall(re_xiaoqu_id, s_page.text)
    danjia_list = re.findall(re_danjia_price, s_page.text)
    print "单价  " + '--' + "小区均价"

    for i in range(len(fang_id_list)):
	fang_id = fang_id_list[i]
	fang_url = fang_url_list[i]
        xiaoqu_id = xiaoqu_id_list[i]
        danjia = danjia_list[i]
	xiaoqu_avg_price = db_xiaoqu_avg_price(xiaoqu_id)
	if not xiaoqu_avg_price:
	    print "Without this xiaoqu in the db."
	    continue

        # 比较单价和小区均价，如果单价小于小区均价5000，则显示
        price_key = int(xiaoqu_avg_price) - bj_value_price
        if int(danjia) < price_key:
	    good_fang_detail = danjia + '--' + str(xiaoqu_avg_price) + '--' + fang_url + '\n'
            print good_fang_detail,
	    # 将结果插入数据库（判断数据库中没有的结果）
	    db_insert_good_fang(fang_id, fang_url)
	    # 将结果写入文件
	    #file_name = 'good_fang_list/' + chengqu + '.txt'
	    #f = open(file_name, 'a')
	    #f.write(good_fang_detail)
	    #f.close()
        else:
            print "This is market price."

#* 访问每一页，并针对每一页的每一个房子对比价格
def main():
    generate_page_url_list()
    page = 0
    for fang_page_url in page_url_list[process_num - 1:]:
	# 从第几页开始对比（用于程序中途断掉之后，从中断的页继续执行，避免结果重复）
	page = page_url_list.index(fang_page_url) + 1
        # 以计数方式显示执行进程，并打印到屏幕
        print '%s page %d:  compare result: ' % (chengqu, page)
	# 轮询代理地址
	current_proxy_index = round_proxy(page)
	# 访问页面
	s_page = request_session(fang_page_url, proxy_list[proxy['index']])
	# 对比房子单价和小区价格
	compare_price(s_page)
        # 每个页面之间随机睡眠3到18秒
        sleep(random.randint(8, 23))

if __name__ == '__main__':
    main()
