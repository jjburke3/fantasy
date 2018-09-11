
import sys
sys.path.insert(0,'../..')
from datetime import date, datetime, timedelta
import calendar




from DOConn import connection
from DOsshTunnel import DOConnect
from leagueResults import pullLeagueData

now = datetime.utcnow() - timedelta(hours=4)


year = 2018

if now.date() <= date(year, 9, 11) and now.date() >= date(year,9,4):
    week = 1
elif now.date() <= date(year, 9, 18):
    week = 2
elif now.date() <= date(year, 9, 25):
    week = 3
elif now.date() <= date(year, 10, 2):
    week = 4
elif now.date() <= date(year, 10, 9):
    week = 5
elif now.date() <= date(year, 10, 16):
    week = 6
elif now.date() <= date(year, 10, 23):
    week = 7
elif now.date() <= date(year, 10, 30):
    week = 8
elif now.date() <= date(year, 11, 6):
    week = 9
elif now.date() <= date(year, 11, 13):
    week = 10
elif now.date() <= date(year, 11, 20):
    week = 11
elif now.date() <= date(year, 11, 27):
    week = 12
elif now.date() <= date(year, 12, 4):
    week = 13
elif now.date() <= date(year, 12, 11):
    week = 14
elif now.date() <= date(year, 12, 18):
    week = 15
elif now.date() <= date(year, 12, 25):
    week = 16
elif now.date() <= date(year + 1, 1, 1):
    week = 17
else:
    week = 0

    


with DOConnect() as tunnel:
    c, conn = connection(tunnel)
    try:
        sql = pullLeagueData()
        try:
            c.execute(sql[0])
        except Exception as e:
            print(str(e))
        conn.commit()
        try:
            c.execute(sql[1])
        except Exception as e:
            print(str(e))
        conn.commit()
    except Exception as e:
        print(str(e))




    conn.close()
