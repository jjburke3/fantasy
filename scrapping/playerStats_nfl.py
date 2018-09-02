'''
http://api.fantasy.nfl.com/v1/players/stats?statType=weekStats&season=2017&week=1&format=json
players/advanced
players/researchinfo
players/editorweekranks
players/editorweekranks
'''

'''
just use for most recent season
only pull qbHits, passDenf, bigPlay, 2 points
'''

import requests
import pandas as pd


import sys
sys.path.insert(0,'..')

from DOConn import connection
from DOsshTunnel import DOConnect

from references import statDict
yearRange = range(2009,2018)
weekRange = range(1,18)

with DOConnect() as tunnel:
    c, conn = connection(tunnel)

    '''
    drop table if exists scrapped_data.playerStats;
    create table scrapped_data.playerStats
    (statsSeason integer, statsWeek int,
    statsPlayerId int, statsStat varchar(50),
    statsPlayer varchar(50), statsPosition varchar(15),
    statsTeam varchar(25), statValue float,
    dataCreate datetime,
    primary key (statsSeason, statsWeek,
    references.pyd, statsStat))'''
    
    url = 'http://api.fantasy.nfl.com/v1/players/stats?statType=weekStats&season=%d&week=%d&format=json'

    for year in yearRange:
        for week in weekRange:


            r = requests.get(url % (year,week))

            data = r.json()

            players = data['players']


            sqlScript = 'insert into scrapped_data.playerStats values '

            for player in players:
                for key in player['stats']:
                    sqlData = {'season' : int(data['season']),
                               'week' : int(data['week']),
                               'id' : player['id'],
                               'Player' : player['name'],
                               'Position' : player['position'],
                               'Team' : player['teamAbbr'],
                               'stat' : key,
                               'value' : player['stats'][key]
                               }
                    if statDict[int(key)] != '':
                        sqlData['stat'] = statDict[int(key)]

                    sqlScriptAddend = ("(" +
                        str(sqlData['season']) + "," +
                        str(sqlData['week']) + "," +
                        str(sqlData['id']) + "," +
                        "'" + sqlData['stat'] + "'," +
                        "'" + sqlData['Player'].replace("'","_") + "'," +
                        "'" + sqlData['Position'] + "'," +
                        "'" + sqlData['Team'] + "'," +
                        sqlData['value'] + "," +
                        "current_timestamp()),")

                    sqlScript += sqlScriptAddend

            sqlScript = sqlScript[:-1]
            c.execute(sqlScript)
            print('year: ' + str(year) + "_week: " + str(week))
            conn.commit()



    conn.close()
