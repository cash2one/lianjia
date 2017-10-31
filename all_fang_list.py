#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import time
import re
from time import sleep
import random

all_fang_id_list = []
# 链家网站变量 
bj_chengqu_id = 8
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
ershoufang_url = "http://bj.lianjia.com/ershoufang/"
page_abb = '/pg'
search_key = '/co32ng1hu1nb1bp100ep600'
re_xiaoqu_id = 'http://bj.lianjia.com/xiaoqu/([0-9]{13})'
re_fang_id = '\<a class=\"img \" href="(http://bj\.lianjia\.com/ershoufang/[0-9]{12,13}\.html)'
re_totalpage = '"totalPage":([0-9]{2,3})'

# 代理服务器列表
proxy_list = [{"http": "http://101.200.177.178:731"}, \
                {"http": "http://101.200.1.235:731"}, \
                {"http": "http://101.201.152.116:731"}, \
                {"http": "http://182.92.4.179:731"}, \
                {"http": "http://123.56.87.39:731"}, \
                {"http": "http://123.56.114.204:731"}]

#* 获取城区url
chengqu = bj_chengqu_list[bj_chengqu_id - 1]
chengqu_url = ershoufang_url \
                + chengqu \
                + search_key

#* 初始网站访问session
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

#* 获取总页数,并生成所有页面链接
def get_page_url_list():
    global page_url_list
    page_url_list = []
    totalpage = re.findall(re_totalpage, s_page.text)
    for page in range(1, int(totalpage[0])):
        page_url = ershoufang_url \
                + chengqu \
                + page_abb \
                + str(page) \
                + search_key
        page_url_list.append(page_url)

#* 主程序
get_page_url_list()
for page_url in page_url_list:
    proxies = random.choice(proxy_list)
    s_danjia = session.get(page_url, headers=headers, proxies=proxies)
    s_danjia.encoding = 'utf-8'

    xiaoqu_id_list = re.findall(re_xiaoqu_id, s_danjia.text)
    all_fang_id_list += xiaoqu_id_list    
    print xiaoqu_id_list
    sleep(random.randint(8, 26))

f = open('a.txt', 'a')
f.write(str(all_fang_id_list))





