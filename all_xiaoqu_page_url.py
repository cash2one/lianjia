#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import pymysql
import re
from time import sleep
import random

# 链家网站变量 
chengqu_url_list = []
all_page_url_list = []
bj_chengqu_list = ['dongcheng', 
                'xicheng', 
                'chaoyang', 
                'haidian', 
                'fengtai', 
                'shijingshan', 
                'tongzhou', 
                'changping', 
                'daxing', 
                'yizhuangkaifaqu', 
                'shunyi', 
                'fangshan', 
                'mentougou', 
                'pinggu', 
                'huairou', 
                'miyun', 
                'yanqing', 
                'yanjiao']
xiaoqu_url = "http://bj.lianjia.com/xiaoqu/"
page_abb = '/pg'
re_totalpage = '"totalPage":([0-9]{1,3})'

# 代理服务器列表
proxy_list = ['http://101.200.177.178:731', \
                'http://101.200.1.235:731', 
                'http://101.201.152.116:731', \
                'http://182.92.4.179:731', \
                'http://123.56.87.39:731', \
                'http://123.56.114.204:731']

#* 获取城区url
def generate_chengqu_url():
    for chengqu in bj_chengqu_list:
        chengqu_url = xiaoqu_url + chengqu
        chengqu_url_list.append(chengqu_url)

#* 初始网站访问session
def request_url(chengqu_url):
    headers = {
            'Host': 'bj.lianjia.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
            }
    session = requests.Session()
    s_page = session.get(chengqu_url, headers=headers)
    s_page.encoding = 'utf-8'
    return s_page

#* 获取总页数,并生成所有页面链接
def get_page_url_list():
    for chengqu_url in chengqu_url_list:
        s = request_url(chengqu_url)
        totalpage = re.findall(re_totalpage, s.text)
        sleep(random.randint(1, 15))
        print totalpage, '-', chengqu_url
        for page in range(1, int(totalpage[0])):
            page_url = chengqu_url \
                    + page_abb \
                    + str(page)
            all_page_url_list.append(page_url)

def db_insert(url_list):
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
            for page_url in url_list:
                sql = 'insert into lj_xiaoqu_page_url values(NULL, \'' + page_url + '\')'
                s_cursor.execute(sql)
            s_connect.commit()
    finally:
        s_connect.close()

if __name__ == '__main__':
    generate_chengqu_url()
    get_page_url_list()
    db_insert(all_page_url_list)

