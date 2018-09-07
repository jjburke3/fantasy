
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
        {'urlCode' : 20101018151239,
         'year' : 2010,
         'week' : 7},
        {'urlCode' : 20101122204351,
         'year' : 2010,
         'week' : 12},
        {'urlCode' : 20110726184406,
         'year' : 2011,
         'week' : 0},
        {'urlCode' : 20111006030858,
         'year' : 2011,
         'week' : 5},
        {'urlCode' : 20111017005641,
         'year' : 2011,
         'week' : 7},
        {'urlCode' : 20111223163629,
         'year' : 2011,
         'week' : 16},
        {'urlCode' : 20120831234854,
         'year' : 2012,
         'week' : 0},
        {'urlCode' : 20121001130701,
         'year' : 2012,
         'week' : 5},
        {'urlCode' : 20121014150324,
         'year' : 2012,
         'week' : 6},
        {'urlCode' : 20121021150910,
         'year' : 2012,
         'week' : 7},
        {'urlCode' : 20121028133519,
         'year' : 2012,
         'week' : 8},
        {'urlCode' : 20121105075359,
         'year' : 2012,
         'week' : 9},
        {'urlCode' : 20121111135417,
         'year' : 2012,
         'week' : 10},
        {'urlCode' : 20121118155256,
         'year' : 2012,
         'week' : 11},
        {'urlCode' : 20121125170027,
         'year' : 2012,
         'week' : 12},
        {'urlCode' : 20121203144040,
         'year' : 2012,
         'week' : 13},
        {'urlCode' : 20121210035110,
         'year' : 2012,
         'week' : 14},
        {'urlCode' : 20121220015830,
         'year' : 2012,
         'week' : 15},
        {'urlCode' : 20121224114654,
         'year' : 2012,
         'week' : 16},
        {'urlCode' : 20130819141435,
         'year' : 2013,
         'week' : 0},
        {'urlCode' : 20130902133233,
         'year' : 2013,
         'week' : 1},
        {'urlCode' : 20130918161134,
         'year' : 2013,
         'week' : 3},
        {'urlCode' : 20130922231159,
         'year' : 2013,
         'week' : 4},
        {'urlCode' : 20131004080742,
         'year' : 2013,
         'week' : 5},
        {'urlCode' : 20140701185147,
         'year' : 2014,
         'week' : 0},
        {'urlCode' : 20150901003059,
         'year' : 2015,
         'week' : 0},
        {'urlCode' : 20150905175556,
         'year' : 2015,
         'week' : 1},
        {'urlCode' : 20151031173009,
         'year' : 2015,
         'week' : 8},
        {'urlCode' : 20151225164852,
         'year' : 2015,
         'week' : 16},
        {'urlCode' : 20151231084614,
         'year' : 2015,
         'week' : 17},
        {'urlCode' : 20160830140231,
         'year' : 2016,
         'week' : 0},
        {'urlCode' : 20160917141224,
         'year' : 2016,
         'week' : 2},
        {'urlCode' : 20161014062909,
         'year' : 2016,
         'week' : 6},
        {'urlCode' : 20161118151710,
         'year' : 2016,
         'week' : 11},
        {'urlCode' : 20170830090745,
         'year' : 2017,
         'week' : 0},
        {'urlCode' : 20171001041057,
         'year' : 2017,
         'week' : 4},
        {'urlCode' : 20171026092046,
         'year' : 2017,
         'week' : 8},
        {'urlCode' : 20171103153426,
         'year' : 2017,
         'week' : 9},
        {'urlCode' : 20171206230341,
         'year' : 2017,
         'week' : 14}

    ]



with DOConnect() as tunnel:
    c, conn = connection(tunnel)
    for way in wayBack:

        year = way['year']
        week = way['week']

        url = "https://web.archive.org/web/%d/http://fftoday.com/nfl/depth.php?o=one_page&order_by=" % way['urlCode']

        print(str(year)+"_"+str(week))

        try:
            sql = pullDepthCharts(year,week,day,time,url)

            
            c.execute(sql)

            conn.commit()
        except Exception as e:
            print(str(e))



    conn.close()
