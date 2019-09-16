
'''
need long td bonues, fumbles, lostFumbles, fgLenghts,
2pt convs, qbhits, passdefeneded, st touchdowns
'''

'''
drop table if exists scrapped_data.playerStats;
create table scrapped_data.playerStats
(statYear int default 0, statWeek int default 0, statPlayer varchar(50) default '',
	statPosition varchar(25) default '', statTeam varchar(25) default '',
    gamePlayed int, comp int, attempt int, 
    passYard int, passTd int, passInt int, passTD40bonus int,
    rushAtt int, rushYard int, rushTD int, rushTD40bonus int,
    target int, recept int, receivYard int, 
    receivTD int, receivTD40bonus int,
    fumble int, fumbleLoss int,
    fgMade int, fgAttmpt int, xPointMade int, xPointAttmpt int,
    fg40_49made int, fg40_49miss int, fg50made int, fg50miss int,
    defSack int, qbHit int, forceFumble int,
    fumbleRecov int, defInt int, passDef int,
    defTD int, fumbleTD int, intTD int, 
    puntTD int, kickTD int, 
    pointsAgainst int, defPassYards int, defRunYards int, 
    safety int, blockKick int, blockTD int,
    passPoints float,
    runPoints float,
    receivPoints float,
    fumblePoints float,
    stPoints float,
    kickPoints float,
    defPoints float,
    totalPoints float,
    
    dataCreate datetime,
    
primary key (statYear, statWeek, statPlayer, statPosition, statTeam));
'''

import requests
import pandas as pd
import re
from bs4 import BeautifulSoup as bs


import sys
sys.path.insert(0,'..')

from DOConn import connection
from DOsshTunnel import DOConnect

from references import statDict, errorSQL, fullName, ffTeam, fullToMascot


def ffData(year, week):

    posRange = [
            {'id' : 10, 'pos' : 'QB',
                 'columns' : [
                        {'id' : 1, 'label' : 'statTeam'},
                        {'id' : 2, 'label' : 'gamePlayed'},
                        {'id' : 3, 'label' : 'comp'},
                        {'id' : 4, 'label' : 'attempt'},
                        {'id' : 5, 'label' : 'passYard'},
                        {'id' : 6, 'label' : 'passTD'},
                        {'id' : 7, 'label' : 'passInt'},
                        {'id' : 8, 'label' : 'rushAtt'},
                        {'id' : 9, 'label' : 'rushYard'},
                        {'id' : 10, 'label' : 'rushTD'}
                     ]
             },
            {'id' : 20, 'pos' : 'RB',
                 'columns' : [
                        {'id' : 1, 'label' : 'statTeam'},
                        {'id' : 2, 'label' : 'gamePlayed'},
                        {'id' : 3, 'label' : 'rushAtt'},
                        {'id' : 4, 'label' : 'rushYard'},
                        {'id' : 5, 'label' : 'rushTD'},
                        {'id' : 6, 'label' : 'target'},
                        {'id' : 7, 'label' : 'recept'},
                        {'id' : 8, 'label' : 'receivYard'},
                        {'id' : 9, 'label' : 'receivTD'}
                     ]
             },
            {'id' : 30, 'pos' : 'WR',
                 'columns' : [
                        {'id' : 1, 'label' : 'statTeam'},
                        {'id' : 2, 'label' : 'gamePlayed'},
                        {'id' : 7, 'label' : 'rushAtt'},
                        {'id' : 8, 'label' : 'rushYard'},
                        {'id' : 9, 'label' : 'rushTD'},
                        {'id' : 3, 'label' : 'target'},
                        {'id' : 4, 'label' : 'recept'},
                        {'id' : 5, 'label' : 'receivYard'},
                        {'id' : 6, 'label' : 'receivTD'}
                     ]
             },
            {'id' : 40, 'pos' : 'TE',
                 'columns' : [
                        {'id' : 1, 'label' : 'statTeam'},
                        {'id' : 2, 'label' : 'gamePlayed'},
                        {'id' : 3, 'label' : 'target'},
                        {'id' : 4, 'label' : 'recept'},
                        {'id' : 5, 'label' : 'receivYard'},
                        {'id' : 6, 'label' : 'receivTD'}
                     ]
             },
            {'id' : 80, 'pos' : 'K',
                 'columns' : [
                        {'id' : 1, 'label' : 'statTeam'},
                        {'id' : 2, 'label' : 'gamePlayed'},
                        {'id' : 3, 'label' : 'fgMade'},
                        {'id' : 4, 'label' : 'fgAttmpt'},
                        {'id' : 6, 'label' : 'xPointMade'},
                        {'id' : 7, 'label' : 'xPointAttmpt'}
                     ]
             },
            {'id' : 99, 'pos' : 'D/ST',
                 'columns' : [
                        {'id' : 1, 'label' : 'gamePlayed'},
                        {'id' : 2, 'label' : 'defSack'},
                        {'id' : 3, 'label' : 'fumbleRecov'},
                        {'id' : 4, 'label' : 'defInt'},
                        {'id' : 5, 'label' : 'defTD'},
                        {'id' : 6, 'label' : 'pointsAgainst'},
                        {'id' : 7, 'label' : 'defPassYards'},
                        {'id' : 8, 'label' : 'defRunYards'},
                        {'id' : 9, 'label' : 'safety'},
                        {'id' : 10, 'label' : 'kickTD'}
                     ]
             }
        ]



    
    url = 'http://www.fftoday.com/stats/playerstats.php'
    sqlCodes = []
    for position in posRange:
        curPage = 0
        nextPage = True
        while nextPage:

            sqlStat = 'insert into scrapped_data.playerStats'
            sqlStat += '(statYear, statWeek, statPlayer, '
            sqlStat += 'statPosition, '
            if position['pos'] == 'D/ST':
                sqlStat += 'statTeam, '
            for column in position['columns']:
                sqlStat += column['label']
                sqlStat += ','

            sqlStat += ' dataCreate)'

            sqlStat += ' values '

            params = {
                'Season' : year,
                'GameWeek' : week,
                'PosID' : position['id'],
                'cur_page' : curPage
            }

            r = requests.get(url,params=params)

            soup = bs(r.content, 'html.parser')
            table = soup.find_all('table')[9]
            table = table.find_all('table')[0]
            rows = table.find_all('tr')
            for row in rows[2:]:
                tds = row.find_all('td')
                sqlStat += '('
                sqlStat += str(year) + ','
                sqlStat += str(week) + ','
                playerName = tds[0].get_text().replace("'",'_')
                playerName = playerName[(playerName.index('. ')+2):]
                playerName2 = playerName
                if position['pos'] == 'D/ST':
                    playerName = fullToMascot[playerName] + ' D/ST'
                sqlStat += "'" + playerName + "',"
                sqlStat += "'" + position['pos'] + "',"
                if position['pos'] == 'D/ST':
                    sqlStat += "'" + fullName[playerName2] + "',"
                for column in position['columns']:
                    columnValue = tds[column['id']].get_text()
                    if columnValue == '':
                        columnValue = '0'
                    sqlStat += "'" + columnValue + "',"
                sqlStat += ' current_timestamp()),'

            sqlStat = sqlStat[:-1]
            sqlStat += ' on duplicate key update '
            for column in position['columns']:
                if column['label'] != 'statTeam':
                    sqlStat += column['label']
                    sqlStat += ' = values('
                    sqlStat += column['label'] + '), '
            sqlStat += 'dataCreate = current_timestamp();'

            if len(rows) > 2:
                sqlCodes.append(sqlStat)
                
            
            if len(rows) < 52:
                nextPage = False
            else:
                curPage += 1

    return sqlCodes


                        



