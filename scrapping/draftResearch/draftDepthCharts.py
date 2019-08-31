import pymysql
from espnff import League, ESPNFF, playerPos, nflTeamsAbbrev

import sys
sys.path.insert(0,'../..')
sys.path.insert(0,'../automated/')
sys.path.insert(0,'..')

from security import fantasy_league
from references import fullName
from depthCharts import pullDepthCharts



conn = pymysql.connect(host="localhost",
                       user="root",
                       passwd="",
                       db="draft")

year = 2019
week = 0
day = ""
time = ""

c = conn.cursor()

try:
    c.execute("delete from scrapped_data.depthCharts where " +
              "chartSeason = " + str(year) + " and " +
              "chartWeek = " + str(week) + ";")
    
    sql = pullDepthCharts(year,week,day,time)

    c.execute(sql)

    conn.commit()
except Exception as e:
    print(str(e))




conn.close()
