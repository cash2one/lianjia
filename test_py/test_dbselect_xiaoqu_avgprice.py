import pymysql

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
            s_cursor.execute(sql)
	    s_result = s_cursor.fetchall()
	    print s_result[0]['avg_price']
    finally:
        s_connect.close()

db_xiaoqu_avg_price(117962894283635)
