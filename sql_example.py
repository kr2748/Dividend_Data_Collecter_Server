import pymysql


HOST = "0.0.0.0"
USERNAME = "root"
PASSWORD = "app"
DB_NAME = "finance_db"

conn = pymysql.connect(host='0.0.0.0', user= USERNAME, password=PASSWORD, db=DB_NAME,charset='utf8')

# 여기서부터
cursor = conn.cursor()
ticker = 'NVT',
dividend_date = '2020-07-25' # Date로 바꿔야함
allocation = 0.175
dividend_payment_date = '2020-07-25'
dividend_payment_rate = 3.89

sql = "insert into finance_db.finance_info(symbol, dividends_date, dividends, payment_date, dividends_rate) \
values('afklasjfjasdkfjsa', '{}', '{}', '{}', '{}') on duplicate key \
update \
dividends_date = '{}', \
dividends = '{}', \
payment_date = '{}', \
dividends_rate = '{}'".format(dividend_date,allocation,dividend_payment_date,dividend_payment_rate, dividend_date,allocation,dividend_payment_date,dividend_payment_rate)

print("sql : {}".format(sql))

cursor.execute(sql)
#여기까지 포문 돌면됩니다. 

conn.commit()

'''
insert into finance_db.finance_info(dividends_date, dividends, payment_date, dividends_rate) values(('NVT',), 2020-07-25, 0.175, 2020-07-25, 3.89) on duplicate key update dividends_date = '2020-07-25', dividends = '0.175', payment_date = '2020-07-25', dividends_rate = '3.89'
'''

#0 -> none
#1 킹
#2 귀족
#3 챔피언
