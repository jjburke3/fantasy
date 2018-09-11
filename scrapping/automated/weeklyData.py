
import sys
sys.path.insert(0,'../..')
from datetime import date, datetime, timedelta
import calendar




from DOConn import connection
from DOsshTunnel import DOConnect
from playerStats_ffdata import ffData
from playerStats_pro-football import pftData

now = datetime.utcnow() - timedelta(hours=4)


year = 2018

if now.date() <= date(year, 9, 15) and now.date() >= date(year,9,8):
    week = 1
elif now.date() <= date(year, 9, 22):
    week = 2
elif now.date() <= date(year, 9, 29):
    week = 3
elif now.date() <= date(year, 10, 6):
    week = 4
elif now.date() <= date(year, 10, 13):
    week = 5
elif now.date() <= date(year, 10, 20):
    week = 6
elif now.date() <= date(year, 10, 27):
    week = 7
elif now.date() <= date(year, 11, 3):
    week = 8
elif now.date() <= date(year, 11, 10):
    week = 9
elif now.date() <= date(year, 11, 17):
    week = 10
elif now.date() <= date(year, 11, 24):
    week = 11
elif now.date() <= date(year, 12, 1):
    week = 12
elif now.date() <= date(year, 12, 8):
    week = 13
elif now.date() <= date(year, 12, 15):
    week = 14
elif now.date() <= date(year, 12, 22):
    week = 15
elif now.date() <= date(year, 12, 29):
    week = 16
elif now.date() <= date(year + 1, 1, 5):
    week = 17
else:
    week = 0

    


with DOConnect() as tunnel:
    c, conn = connection(tunnel)
    try:
        sql = ffData(year,week)
        for sqlCode in sql:
            try:
                c.execute(sql)
                conn.commit()
            except Exception as e:
                print(str(e))
    except Exception as e:
        print(str(e))
    try:
        sql = pftData(year,week)
        for sqlCode in sql:
            try:
                c.execute(sql)
                conn.commit()
            except Exception as e:
                print(str(e))
    except Exception as e:
        print(str(e))




    conn.close()
