
import sys
sys.path.insert(0,'../..')
from datetime import date
import calendar




from DOConn import connection
from DOsshTunnel import DOConnect
from depthCharts import pullDepthCharts
from injuries import pullInjuries


day = ''
time = ''

#week1 9/11

wayBack = [
        {'urlCode' : 20100903053229,
         'year' : 2010,
         'week' : 1},
        {'urlCode' : 20110902054030,
         'year' : 2011,
         'week' : 1},
        {'urlCode' : 20120919102314,
         'year' : 2012,
         'week' : 1},
        {'urlCode' : 20130908075330,
         'year' : 2013,
         'week' : 1},
        {'urlCode' : 20140914082552,
         'year' : 2014,
         'week' : 1},
        {'urlCode' : 20150908015559,
         'year' : 2015,
         'week' : 1},
        {'urlCode' : 20161021064551,
         'year' : 2016,
         'week' : 1},
        {'urlCode' : 20170907025357,
         'year' : 2017,
         'week' : 1},
        {'urlCode' : 20180907063926,
         'year' : 2018,
         'week' : 1},
        {'urlCode' : 20170911105133,
         'year' : 2017,
         'week' : 2},
        {'urlCode' : 20170920205109,
         'year' : 2017,
         'week' :3},
        {'urlCode' : 20171013190031,
         'year' : 2017,
         'week' : 6},
        {'urlCode' : 20171024210311,
         'year' : 2017,
         'week' : 8},
        {'urlCode' : 20171115152125,
         'year' : 2017,
         'week' : 11},
        {'urlCode' : 20171219191402,
         'year' : 2017,
         'week' : 16},
        {'urlCode' : 20171225211754,
         'year' : 2017,
         'week' : 17},
        {'urlCode' : 20180914012353,
         'year' : 2018,
         'week' : 2},
        {'urlCode' : 20180920233048,
         'year' : 2018,
         'week' : 3},
        {'urlCode' : 20180928211519,
         'year' : 2018,
         'week' : 4},
        {'urlCode' : 20181006005446,
         'year' : 2018,
         'week' : 5},
        {'urlCode' : 20181011233225,
         'year' : 2018,
         'week' : 6},
        {'urlCode' : 20181019003007,
         'year' : 2018,
         'week' : 7},
        {'urlCode' : 20181025232037,
         'year' : 2018,
         'week' : 8},
        {'urlCode' : 20181102031131,
         'year' : 2018,
         'week' : 9},
        {'urlCode' : 20181109173845,
         'year' : 2018,
         'week' : 10},
        {'urlCode' : 20181117200115,
         'year' : 2018,
         'week' : 11},
        {'urlCode' : 20181122191103,
         'year' : 2018,
         'week' : 12},
        {'urlCode' : 20181130010643,
         'year' : 2018,
         'week' : 13},
        {'urlCode' : 20181207011100,
         'year' : 2018,
         'week' : 14},
        {'urlCode' : 20181220171607,
         'year' : 2018,
         'week' : 16},
        {'urlCode' : 20181229055428,
         'year' : 2018,
         'week' : 17}

    ]



with DOConnect() as tunnel:
    c, conn = connection(tunnel)
    for way in wayBack:

        year = way['year']
        week = way['week']

        url = "https://web.archive.org/web/%d/https://subscribers.footballguys.com/apps/depthchart.php" % way['urlCode']

        print(str(year)+"_"+str(week))

        try:
            sql = pullDepthCharts(year,week,day,time,url)

            
            c.execute(sql)

            conn.commit()
        except Exception as e:
            print(str(e))



    conn.close()
