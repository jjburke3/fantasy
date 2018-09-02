'''
use http://www.fftoday.com
for all 2017 data
'''
import requests
import pandas as pd
import re
from bs4 import BeautifulSoup

import sys
sys.path.insert(0,'..')

from DOConn import connection
from DOsshTunnel import DOConnect
from references import wayBack

with DOConnect() as tunnel:
    c, conn = connection(tunnel)

    '''
    drop table if exists scrapped_data.depthCharts;
    create table scrapped_data.depthCharts
    (chartSeason int, chartWeek int, chartTeam varchar(15),
    chartPosition varchar(25), chartRank int, playerName varchar(50),
    dataCreate datetime,
    primary key(chartSeason, chartWeek, chartTeam, 
    chartPosition, chartRank));
    '''
    c.execute("delete from scrapped_data.depthCharts where "
              + " chartSeason = 2018 and chartWeek = 0;")
    conn.commit()
    wayBackURL = 'https://web.archive.org/web/%d/'

    #for per in wayBack:
    season = 2018
    week = 0
    print('season: ' + str(season) + "_week: " + str(week))
    #url = wayBackURL % per['urlCode']
    url = 'https://www.ourlads.com/nfldepthcharts/depthcharts.aspx'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find_all('table', id=re.compile("gvChart"))
    tdf = pd.read_html(str(table), flavor='bs4')[0]
    tdf = tdf.iloc[1:,0:]
    priorPos = ''
    sqlQuery = "insert into scrapped_data.depthCharts values "
    allData = {}
    playerCells = [3,5,7,9,11]
    for player in playerCells:
        for index, row in tdf.iterrows():
            if row[1] == row[1] and row[0] == row[0]:
                team = row[0]
                pos = row[1]
                if row[player] == row[player]:
                    if (team + "-" + pos) in allData:
                        allData[team + "-" + pos] +=1
                    else:
                        allData[team + "-" + pos] = 1
                    chartPos = allData[team + "-" + pos]
                    playerName = row[player].replace("'","_")
                    lastName = playerName.split(',')[0]
                    firstName = playerName.split(', ',1)[1]
                    if ' ' in firstName:
                        firstName = firstName[:firstName.rindex(' ')]
                    priorPos = pos
                    info = {'team' : team,
                            'position' : pos,
                            'player' : firstName + " " + lastName,
                            'chartPos' : chartPos}
                    sqlQuery += "(" + str(season) + ","
                    sqlQuery += str(week) + ","
                    sqlQuery += "'" + info['team'] + "'," 
                    sqlQuery += "'" + info['position'] + "'," 
                    sqlQuery += str(info['chartPos']) + "," 
                    sqlQuery += "'" + info['player'] + "'," 
                    sqlQuery += "current_timestamp()" 
                    sqlQuery += "),"
    sqlQuery = sqlQuery[:-1]
    c.execute(sqlQuery)
    conn.commit()

    conn.close()
