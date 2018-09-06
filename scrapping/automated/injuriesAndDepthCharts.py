
import sys
sys.path.insert(0,'../..')
import datetime



from DOConn import connection
from DOsshTunnel import DOConnect
from depthCharts import pullDepthCharts
from injuries import pullInjuries

now = datetime.datetime.now()

print(now.year)

year = now.year

week1 9/11



'''
with DOConnect() as tunnel:
    c, conn = connection(tunnel)

    sql = pullInjuries(2017,16,'Mon','Afternoon')

    c.execute(sql)

    conn.commit()

    sql = pullDepthCharts(2017,16,'Mon','Afternoon')

    
    c.execute(sql)

    conn.commit()



    conn.close()'''
