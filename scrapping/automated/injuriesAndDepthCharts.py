
import sys
sys.path.insert(0,'../..')
from datetime import date, datetime, timedelta
import calendar




from DOConn import connection
from DOsshTunnel import DOConnect
from depthCharts import pullDepthCharts
from injuries import pullInjuries

now = datetime.utcnow() - timedelta(hours=4)


year = 2020

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

day = calendar.day_name[now.weekday()]

nowTime = now.time()
if now.hour > 3 and now.hour < 14:
    time = 'Morning'
elif now.hour < 18:
    time = 'Afternoon'
elif now.hour < 20:
    time = 'Evening'
else:
    time = 'Night'
    

with DOConnect() as tunnel:
    c, conn = connection(tunnel)
    try:
        sql = pullInjuries(year,week,day,time)
        for statement in sql:
            c.execute(statement)

        conn.commit()
    except Exception as e:
        print(str(e))

    try:
        sql = pullDepthCharts(year,week,day,time)
        for statement in sql:
            c.execute(statement)

        conn.commit()
    except Exception as e:
        print(str(e))



    conn.close()
