
import sys
sys.path.insert(0,'../..')
import datetime



from DOConn import connection
from DOsshTunnel import DOConnect
from depthCharts import pullDepthCharts
from injuries import pullInjuries

now = datetime.datetime.now()


years = range(2015,2016)
weeks = range(4,5)
day = ''
time = ''


with DOConnect() as tunnel:
    c, conn = connection(tunnel)

#week1 9/11

    for year in years:
        for week in weeks:
            print(str(year)+"_"+str(week))

            try:
                sql = pullInjuries(year,week,day,time)

                c.execute(sql)

                conn.commit()
            except Exception as e:
                print(str(e))




    conn.close()
