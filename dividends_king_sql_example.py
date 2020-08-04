import pymysql

HOST = "0.0.0.0"
USERNAME = "root"
PASSWORD = "app"
DB_NAME = "finance_db"

conn = pymysql.connect(host='0.0.0.0', user= USERNAME, password=PASSWORD, db=DB_NAME,charset='utf8')
cursor = conn.cursor()

#여기서부터
#0 -> none
#1 킹
#2 귀족
#3 챔피언

sql = "insert into finance_db.finance_info(symbol, hot_dividends) values('NVT', '1') \
on duplicate key \
update hot_dividends = '1'"

cursor.execute(sql)
#여기까지 포문 돌면됩니다.

conn.commit()
