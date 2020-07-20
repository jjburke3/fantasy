
import sys, os
sys.path.insert(0,'../..')
from datetime import date
import calendar
import requests



from DOConn import connection
from DOsshTunnel import DOConnect
from depthCharts import pullDepthCharts
from injuries import pullInjuries


day = ''
time = ''

startUrl = 'http://web.archive.org/cdx/search/cdx?url=https://subscribers.footballguys.com/apps/depthchart.php&collapse=digest&output=json'

r2 = requests.get(startUrl).json()


pages = [i[1] for i in r2[1:]]

pages = ['20151003013142',
         '20151105131831'
    ]

with DOConnect() as tunnel:
    c, conn = connection(tunnel)
    for way in pages:

        year = 'NULL'
        week = 'NULL'
        url = "https://web.archive.org/web/%s/https://subscribers.footballguys.com/apps/depthchart.php" % way

        print(way)

        try:
            
            sql = pullDepthCharts(year,week,day,time,url,way)


            for sqlScript in sql:
                c.execute(sqlScript)
    
            conn.commit()
        except Exception as e:
            print(str(e))



    conn.close()
