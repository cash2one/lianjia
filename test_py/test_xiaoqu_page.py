import requests
import re
xiaoqu_url = 'http://bj.lianjia.com/xiaoqu/dongcheng/pg10/'
headers = {
        'Host': 'bj.lianjia.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
session = requests.Session()
s = session.get(xiaoqu_url, headers=headers, timeout=10)
s.encoding = 'utf-8'

#f = open('xiaoqu_page.html', 'r')
re_id = '([0-9]{13})/" class'
xiaoqu_id = re.findall(re_id, s.text)
#i = 0
#cc = []
#while i < 66:
#    cc.append(xiaoqu_id[i])
#    i += 2
print len(xiaoqu_id)
print xiaoqu_id
#print len(cc)
#print cc
#f.close()
