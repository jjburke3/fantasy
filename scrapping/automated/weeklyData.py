
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

if now.date() <= date(year, 9, 10) and now.date() >= date(year,9,3):
    week = 1
elif now.date() <= date(year, 9, 17):
    week = 2
elif now.date() <= date(year, 9, 24):
    week = 3
elif now.date() <= date(year, 10, 1):
    week = 4
elif now.date() <= date(year, 10, 8):
    week = 5
elif now.date() <= date(year, 10, 15):
    week = 6
elif now.date() <= date(year, 10, 22):
    week = 7
elif now.date() <= date(year, 10, 29):
    week = 8
elif now.date() <= date(year, 11, 5):
    week = 9
elif now.date() <= date(year, 11, 12):
    week = 10
elif now.date() <= date(year, 11, 19):
    week = 11
elif now.date() <= date(year, 11, 26):
    week = 12
elif now.date() <= date(year, 12, 3):
    week = 13
elif now.date() <= date(year, 12, 10):
    week = 14
elif now.date() <= date(year, 12, 17):
    week = 15
elif now.date() <= date(year, 12, 24):
    week = 16
elif now.date() <= date(year, 12,31):
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
