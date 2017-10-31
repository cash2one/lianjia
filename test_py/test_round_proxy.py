proxy_list = [{"http": "http://101.200.1.235:731"},\
                {"http": "http://101.201.152.116:731"},\
                {"http": "http://182.92.4.179:731"},\
                {"http": "http://123.56.87.39:731"},\
                {"http": "http://123.56.114.204:731"}]
proxy = {'index': -1}
for i in range(50):
    if i % 10 == 0:
        if proxy['index'] <= 4:
            proxy['index'] += 1
        else:
            proxy['index'] = 0
    print proxy
