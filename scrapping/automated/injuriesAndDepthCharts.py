
import sys
sys.path.insert(0,'../..')
from datetime import date, datetime, timedelta
import calendar




from DOConn import connection
from DOsshTunnel import DOConnect
from depthCharts import pullDepthCharts
from injuries import pullInjuries

now = datetime.utcnow() - timedelta(hours=4)


year = (now - timedelta(days=20)).year


if now.date() <= date(year, 9, 14) and now.date() >= date(year,9,7):
    week = 1
elif now.date() <= date(year, 9, 21):
    week = 2
elif now.date() <= date(year, 9, 28):
    week = 3
elif now.date() <= date(year, 10, 5):
    week = 4
elif now.date() <= date(year, 10, 12):
    week = 5
elif now.date() <= date(year, 10, 19):
    week = 6
elif now.date() <= date(year, 10, 26):
    week = 7
elif now.date() <= date(year, 11, 2):
    week = 8
elif now.date() <= date(year, 11, 9):
    week = 9
elif now.date() <= date(year, 11, 16):
    week = 10
elif now.date() <= date(year, 11, 23):
    week = 11
elif now.date() <= date(year, 11, 30):
    week = 12
elif now.date() <= date(year, 12, 7):
    week = 13
elif now.date() <= date(year, 12, 14):
    week = 14
elif now.date() <= date(year, 12, 21):
    week = 15
elif now.date() <= date(year, 12, 28):
    week = 16
elif now.date() <= date(year+1, 1,4):
    week = 17
elif now.date() > date(year+1, 1,4):
    sys.exit()
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
