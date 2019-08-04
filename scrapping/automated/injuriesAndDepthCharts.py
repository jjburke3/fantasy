
import sys
sys.path.insert(0,'../..')
from datetime import date, datetime, timedelta
import calendar




from DOConn import connection
from DOsshTunnel import DOConnect
from depthCharts import pullDepthCharts
from injuries import pullInjuries

now = datetime.utcnow() - timedelta(hours=4)


year = 2019

if now.date() <= date(year, 9, 9) and now.date() >= date(year,9,2):
    week = 1
elif now.date() <= date(year, 9, 16):
    week = 2
elif now.date() <= date(year, 9, 23):
    week = 3
elif now.date() <= date(year, 9, 30):
    week = 4
elif now.date() <= date(year, 10, 7):
    week = 5
elif now.date() <= date(year, 10, 14):
    week = 6
elif now.date() <= date(year, 10, 21):
    week = 7
elif now.date() <= date(year, 10, 28):
    week = 8
elif now.date() <= date(year, 11, 4):
    week = 9
elif now.date() <= date(year, 11, 11):
    week = 10
elif now.date() <= date(year, 11, 18):
    week = 11
elif now.date() <= date(year, 11, 25):
    week = 12
elif now.date() <= date(year, 12, 2):
    week = 13
elif now.date() <= date(year, 12, 9):
    week = 14
elif now.date() <= date(year, 12, 16):
    week = 15
elif now.date() <= date(year, 12, 23):
    week = 16
elif now.date() <= date(year, 12, 30):
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
    '''try:
        sql = pullInjuries(year,week,day,time)

        c.execute(sql)

        conn.commit()
    except Exception as e:
        print(str(e))'''

    try:
        sql = pullDepthCharts(year,week,day,time)

        c.execute(sql)

        conn.commit()
    except Exception as e:
        print(str(e))



    conn.close()
