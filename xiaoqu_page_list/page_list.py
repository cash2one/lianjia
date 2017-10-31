# -*- coding: utf-8 -*-
import requests
import pymysql
import re
from time import sleep
import random


def select_url():
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
            sql = 'select xiaoqu_page_url from lj_xiaoqu_page_url;'
            s_cursor.execute(sql)
	    s_result = s_cursor.fetchall()
	    return s_result
    finally:
        s_connect.close()

result = select_url()
for i in result:
    print i['xiaoqu_page_url']
