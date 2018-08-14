'''{'urlCode' : 20120829100111,
                'season' : 2012,
                'week' : 0},
               {'urlCode' : 20120925042919,
                'season' : 2012,
                'week' : 4},
               {'urlCode' : 20121013223321,
                'season' : 2012,
                'week' : 6},
               {'urlCode' : 20121017090252,
                'season' : 2012,
                'week' : 7},
               {'urlCode' : 20121025151812,
                'season' : 2012,
                'week' : 8},
               {'urlCode' : 20121125082042,
                'season' : 2012,
                'week' : 12},
               {'urlCode' : 20130826104546,
                'season' : 2013,
                'week' : 0},
               {'urlCode' : 20130906025726,
                'season' : 2013,
                'week' : 1},
               {'urlCode' : 20130916075358,
                'season' : 2013,
                'week' : 3},
               {'urlCode' : 20130927180026,
                'season' : 2013,
                'week' : 4},
               {'urlCode' : 20131026055922,
                'season' : 2013,
                'week' : 8},
               {'urlCode' : 20131126032548,
                'season' : 2013,
                'week' : 13},
               {'urlCode' : 20140813022239,
                'season' : 2014,
                'week' : 0},
               {'urlCode' : 20140901182032,
                'season' : 2014,
                'week' : 1},
               {'urlCode' : 20140920211352,
                'season' : 2014,
                'week' : 3},
               {'urlCode' : 20141001080947,
                'season' : 2014,
                'week' : 5},
               {'urlCode' : 20141011191912,
                'season' : 2014,
                'week' : 6},
               {'urlCode' : 20141021232139,
                'season' : 2014,
                'week' : 8},
               {'urlCode' : 20141102064755,
                'season' : 2014,
                'week' : 9},
               {'urlCode' : 20141219012952,
                'season' : 2014,
                'week' : 16},
               '''
import requests
import pandas as pd
import re
from bs4 import BeautifulSoup

import sys
sys.path.insert(0,'..')

from DOConn import connection
from DOsshTunnel import DOConnect

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
    
    c.execute("delete from scrapped_data.depthCharts where "
              + " chartSeason = 2018 and chartWeek = 0;")'''
    conn.commit()
    wayBackURL = 'https://web.archive.org/web/%d/'
    wayBack = [{'urlCode' : 20150831053928,
                'season' : 2015,
                'week' : 0},
               {'urlCode' : 20150909051040,
                'season' : 2015,
                'week' : 1},
               {'urlCode' : 20150917072153,
                'season' : 2015,
                'week' : 2},
               {'urlCode' : 20150926045018,
                'season' : 2015,
                'week' : 3},
               {'urlCode' : 20151001053417,
                'season' : 2015,
                'week' : 4},
               {'urlCode' : 20151007001412,
                'season' : 2015,
                'week' : 5},
               {'urlCode' : 20151013050921,
                'season' : 2015,
                'week' : 6},
               {'urlCode' : 20151020040704,
                'season' : 2015,
                'week' : 7},
               {'urlCode' : 20151027070024,
                'season' : 2015,
                'week' : 8},
               {'urlCode' : 20151104001505,
                'season' : 2015,
                'week' : 9},
               {'urlCode' : 20151112123546,
                'season' : 2015,
                'week' : 10},
               {'urlCode' : 20151120131045,
                'season' : 2015,
                'week' : 11},
               {'urlCode' : 20151128094358,
                'season' : 2015,
                'week' : 12},
               {'urlCode' : 20151206133252,
                'season' : 2015,
                'week' : 13},
               {'urlCode' : 20151209085708,
                'season' : 2015,
                'week' : 14},
               {'urlCode' : 20151214204635,
                'season' : 2015,
                'week' : 15},
               {'urlCode' : 20151222132006,
                'season' : 2015,
                'week' : 16},
               {'urlCode' : 20151230071532,
                'season' : 2015,
                'week' : 17},
               {'urlCode' : 20160826033611,
                'season' : 2016,
                'week' : 0},
               {'urlCode' : 20160907093916,
                'season' : 2016,
                'week' : 1},
               {'urlCode' : 20160913152613,
                'season' : 2016,
                'week' : 2},
               {'urlCode' : 20160919024758,
                'season' : 2016,
                'week' : 3},
               {'urlCode' : 20160930224419,
                'season' : 2016,
                'week' : 4},
               {'urlCode' : 20161008062915,
                'season' : 2016,
                'week' : 5},
               {'urlCode' : 20161015053344,
                'season' : 2016,
                'week' : 6},
               {'urlCode' : 20161024054034,
                'season' : 2016,
                'week' : 8},
               {'urlCode' : 20161102095347,
                'season' : 2016,
                'week' : 9},
               {'urlCode' : 20161115174109,
                'season' : 2016,
                'week' : 11},
               {'urlCode' : 20161128113237,
                'season' : 2016,
                'week' : 13},
               {'urlCode' : 20170828093539,
                'season' : 2017,
                'week' : 0},
               {'urlCode' : 20170908203952,
                'season' : 2017,
                'week' : 1},
               {'urlCode' : 20170913153409,
                'season' : 2017,
                'week' : 2},
               {'urlCode' : 20170920112609,
                'season' : 2017,
                'week' : 3},
               {'urlCode' : 20171003052159,
                'season' : 2017,
                'week' : 5},
               {'urlCode' : 20171014020746,
                'season' : 2017,
                'week' : 6},
               {'urlCode' : 20171028163704,
                'season' : 2017,
                'week' : 8},
               {'urlCode' : 20171114230909,
                'season' : 2017,
                'week' : 11},
               {'urlCode' : 20171212061249,
                'season' : 2017,
                'week' : 15}
        ]
    for per in wayBack:
        season = per['season']
        week = per['week']
        print('season: ' + str(season) + "_week: " + str(week))
        url = wayBackURL % per['urlCode']
        url += 'https://www.ourlads.com/nfldepthcharts/depthcharts.aspx'
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
