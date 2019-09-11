
import sys
sys.path.insert(0,'../..')
from datetime import date, datetime, timedelta
import calendar




from DOConn import connection
from DOsshTunnel import DOConnect
from playerStats_ffdata import ffData
from playerStats_pro_football import pftData
from updateQueries import updateFunc

now = datetime.utcnow() - timedelta(hours=4)


year = 2019

if now.date() <= date(year, 9, 13) and now.date() >= date(year,9,3):
    week = 1
elif now.date() <= date(year, 9, 20):
    week = 2
elif now.date() <= date(year, 9, 27):
    week = 3
elif now.date() <= date(year, 10, 4):
    week = 4
elif now.date() <= date(year, 10, 11):
    week = 5
elif now.date() <= date(year, 10, 18):
    week = 6
elif now.date() <= date(year, 10, 25):
    week = 7
elif now.date() <= date(year, 11, 1):
    week = 8
elif now.date() <= date(year, 11, 8):
    week = 9
elif now.date() <= date(year, 11, 15):
    week = 10
elif now.date() <= date(year, 11, 22):
    week = 11
elif now.date() <= date(year, 11, 29):
    week = 12
elif now.date() <= date(year, 12, 6):
    week = 13
elif now.date() <= date(year, 12, 13):
    week = 14
elif now.date() <= date(year, 12, 20):
    week = 15
elif now.date() <= date(year, 12, 27):
    week = 16
elif now.date() <= date(year+1,1,3):
    week = 17
else:
    week = 0




with DOConnect() as tunnel:
    c, conn = connection(tunnel)
    try:
        sql = ffData(year,week)
        for sqlCode in sql:
            try:
                c.execute(sqlCode)
                conn.commit()
            except Exception as e:
                print(str(e))
    except Exception as e:
        print(str(e))
    try:
        sql = pftData(year,week)
        for sqlCode in sql:
            try:
                temp = 1
                #c.execute(sqlCode)
                #conn.commit()
            except Exception as e:
                print(str(e))
    except Exception as e:
        print(str(e))
    try:
        sql = updateFunc()
        for sqlCode in sql:
            try:
                temp = 1
                c.execute(sqlCode)
                conn.commit()
            except Exception as e:
                print(str(e))
    except Exception as e:
        print(str(e))




    conn.close()
