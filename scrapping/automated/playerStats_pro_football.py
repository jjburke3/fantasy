'''
need long td bonues, fumbles, lostFumbles, fgLenghts,
2pt convs, qbhits, passdefeneded, st touchdowns
'''



import requests
import pandas as pd
import re
from bs4 import BeautifulSoup as bs, Comment


import sys
sys.path.insert(0,'../..')

from references import errorSQL, fullName, pfrAbbrName, fullToMascot, abbrToMascot

from references import statDict



def pftData(year,week):
    sqlCodes = []
    snapSQLpart = ''
    
    url = 'https://www.pro-football-reference.com/years/%d/week_%d.htm'


    links = []
    try:
        r = requests.get(url % (year, week))
        soup = bs(r.content, 'html.parser')
        linkGroup = soup.find_all('table', {'class' : 'teams'})

        for i, game in enumerate(linkGroup):
            linktd = game.find_all('td', {'class' : 'gamelink'})[0]
            linkA = linktd.find_all('a')[0]['href']
            gameR = requests.get('https://www.pro-football-reference.com' +
                             linkA)

            gameInfo = {}
            defStats = {}
            gameSoup = bs(gameR.content, 'html.parser')
                

            names = gameSoup.find_all('a', {'itemprop' : 'name'})

            #homeTeam
            gameInfo['homeTeam'] = fullName[names[0].get_text()]                    
            #awayTeam
            gameInfo['awayTeam'] = fullName[names[1].get_text()]
            #homeScore
            gameInfo['homeScore'] = gameSoup.find_all('div', {'class' : 'score'})[0].get_text()
            #awayScore
            gameInfo['awayScore'] = gameSoup.find_all('div', {'class' : 'score'})[1].get_text()
            #homeCoach
            gameInfo['homeCoach'] = gameSoup.find_all('div', {'class' : 'datapoint'})[0].find_all('a')[0].get_text().replace("'","_")
            #awayCoach
            gameInfo['awayCoach'] = gameSoup.find_all('div', {'class' : 'datapoint'})[1].find_all('a')[0].get_text().replace("'","_")
            #gameDate
            scoreBox = gameSoup.find_all('div', {'class' : 'scorebox_meta'})[0]
            gameInfo['gameDate'] = scoreBox.find_all('div')[0].get_text()
            #gameTime
            gameInfo['gameTime'] = scoreBox.find_all('div')[1].get_text()
            #gameVenue
            gameInfo['gameVenue'] = scoreBox.find_all('div')[2].find_all('a')[0].get_text().replace("'","_")
            for instance in gameSoup(text=lambda text:isinstance(text, Comment)):
                instance2 = bs(instance,'html.parser')
                gameIDtable = instance2.find_all('table', {'id' : 'game_info'})
                if len(gameIDtable) > 0:
                    gameInfo['gameWeather'] = ''
                    gameInfo['venueRoof'] = ''
                    gameInfo['venueSurface'] = ''
                    gameInfo['vegasLine'] = ''
                    for row in gameIDtable[0].find_all('tr'):
                        if len(row.find_all('th'))>0:
                            #venueRoof
                            if row.find('th').get_text() == 'Roof':
                                gameInfo['venueRoof'] = row.find_all('td')[0].get_text().replace("'","_")
                            #venueSurface
                            if row.find('th').get_text() == 'Surface':
                                gameInfo['venueSurface'] = row.find_all('td')[0].get_text().replace("'","_")
                            #gameWeather
                            if row.find('th').get_text() == 'Weather':
                                gameInfo['gameWeather'] = row.find_all('td')[0].get_text().replace("'","_")
                            #gameVegasLine
                            if row.find('th').get_text() == 'Vegas Line':
                                gameInfo['vegasLine'] = row.find_all('td')[0].get_text().replace("'","_")
                    
                playerOffTable = instance2.find_all('table', {'id' : 'player_offense'})
                if len(playerOffTable) > 0:
                    for row in playerOffTable[0].find_all('tr'):
                        if len(row.find('th').find_all('a'))>0:
                            player = row.find('th').find('a').get_text().replace("'",'_')
                            team = pfrAbbrName[row.find_all('td')[0].get_text()]
                            fumbles = row.find_all('td')[19].get_text()
                            fumblesLost = row.find_all('td')[20].get_text()
                            if fumbles not in ['0',''] or fumblesLost not in ['0','']:
                                if fumbles == '':
                                    fumbles = '0'
                                if fumblesLost == '':
                                    fumblesLost = '0'
                                sql = ('update scrapped_data.playerStats ' +
                                       "set fumble = " + str(fumbles) + "," +
                                       " fumbleLoss = " + str(fumblesLost) +
                                       ' where statYear = ' + str(year) + ' ' +
                                       ' and statWeek = ' + str(week) + ' ' +
                                       " and statPlayer = '" + player + "' " +
                                       " and statTeam = '" + team + "';")
                                try:
                                    sqlCodes.append(sql)
                                except Exception as e:
                                    print(str(e))

                                    
                
                
                    
                playerDefTable = instance2.find_all('table', {'id' : 'player_defense'})
                if len(playerDefTable) > 0:
                    for row in playerDefTable[0].find_all('tr'):
                        if len(row.find('th').find_all('a'))>0:
                               team = pfrAbbrName[row.find_all('td')[0].get_text()]
                               player = abbrToMascot[team]
                               intTD = row.find_all('td')[3].get_text()
                               fumR = row.find_all('td')[8].get_text()
                               fumTD = row.find_all('td')[10].get_text()
                               fumF = row.find_all('td')[11].get_text()

                               if (player + ' D/ST') not in defStats:
                                   defStats[(player + ' D/ST')] = {'team' : team,
                                                                   'intTD' : 0,
                                                                   'fumR' : 0,
                                                                   'fumTD' : 0,
                                                                   'fumF' : 0,
                                                                   'kickTD' : 0,
                                                                   'puntTD' : 0
                                                                   }

                               defStats[(player + ' D/ST')]['intTD'] += int(intTD)
                               defStats[(player + ' D/ST')]['fumR'] += int(fumR)
                               defStats[(player + ' D/ST')]['fumTD'] += int(fumTD)
                               defStats[(player + ' D/ST')]['fumF'] += int(fumF)


                kickPuntTable = instance2.find_all('table', {'id' : 'returns'})
                if len(kickPuntTable) > 0:
                    for row in kickPuntTable[0].find_all('tr'):
                        if len(row.find('th').find_all('a')) > 0:
                               player = row.find('th').find('a').get_text().replace("'",'_')
                               team = pfrAbbrName[row.find_all('td')[0].get_text()]
                               playerDef = abbrToMascot[team]
                               kickTD = row.find_all('td')[4].get_text()
                               puntTD = row.find_all('td')[9].get_text()
                               if kickTD not in ['0',''] or puntTD not in ['0','']:
                                   if kickTD == '':
                                       kickTD = '0'
                                   if puntTD == '':
                                       puntTD = '0'
                                   sql = ('update scrapped_data.playerStats ' +
                                           "set puntTD = " + str(puntTD) + "," +
                                           " kickTD = " + str(kickTD) +
                                           ' where statYear = ' + str(year) + ' ' +
                                           ' and statWeek = ' + str(week) + ' ' +
                                           " and statPlayer = '" + player + "' " +
                                           " and statTeam = '" + team + "';")
                                   try:
                                       sqlCodes.append(sql)
                                   except Exception as e:
                                        print(str(e))
                                   if (playerDef + ' D/ST') not in defStats:
                                       defStats[(playerDef + ' D/ST')] = {'team' : team,
                                                                       'intTD' : 0,
                                                                       'fumR' : 0,
                                                                       'fumTD' : 0,
                                                                       'fumF' : 0,
                                                                       'kickTD' : 0,
                                                                       'puntTD' : 0
                                                                       }
                                   defStats[(playerDef + ' D/ST')]['kickTD'] += int(kickTD)
                                   defStats[(playerDef + ' D/ST')]['puntTD'] += int(puntTD)


                snapCountTableHome = instance2.find_all('table', {'id' : 'home_snap_counts'})
                if len(snapCountTableHome) > 0:
                    for row in snapCountTableHome[0].find_all('tr'):
                        if len(row.find('th').find_all('a')) > 0:
                            if row.find_all('td')[0].get_text() in ['QB','TE','RB','WR']:
                                player = row.find('th').find('a').get_text().replace("'","_")
                                team = gameInfo['homeTeam']
                                position = row.find_all('td')[0].get_text()
                                snapCount = row.find_all('td')[1].get_text()
                                snapPert = row.find_all('td')[2].get_text().replace("%",'')

                                snapSQLpart += ("(" + str(year) + "," + str(week) + "," + str(i) + "," +
                                                   "'" + player + "','" + position + "','" + team + "'," +
                                                   str(snapCount) + "," +
                                                   str(float(snapPert)/100) + "),")
                
                snapCountTableAway = instance2.find_all('table', {'id' : 'away_snap_counts'})
                if len(snapCountTableAway) > 0:
                    for row in snapCountTableAway[0].find_all('tr'):
                        if len(row.find('th').find_all('a')) > 0:
                            if row.find_all('td')[0].get_text() in ['QB','TE','RB','WR']:
                                player = row.find('th').find('a').get_text().replace("'","_")
                                team = gameInfo['AwayTeam']
                                position = row.find_all('td')[0].get_text()
                                snapCount = row.find_all('td')[1].get_text()
                                snapPert = row.find_all('td')[2].get_text().replace("%",'')

                                snapSQLpart += ("(" + str(year) + "," + str(week) + "," + str(i) + "," +
                                                   "'" + player + "','" + position + "','" + team + "'," +
                                                   str(snapCount) + "," +
                                                   str(float(snapPert)/100) + "),")
                                                   
                             
            #run game numbers
            sql = ("insert into scrapped_data.gameData values (" + str(year) + "," + str(week) +
                   "," + str(i) + ",'" + gameInfo['homeTeam'] + "','" + gameInfo['awayTeam'] +
                          "'," + str(gameInfo['homeScore']) + "," + str(gameInfo['awayScore']) + ",'" +
                          gameInfo['homeCoach'] + "','" + gameInfo['awayCoach'] + "','" + gameInfo['gameDate'] +
                          "','" + gameInfo['gameTime'] + "','" + gameInfo['gameVenue'] + "','" +
                          gameInfo['venueRoof'] + "','" + gameInfo['venueSurface'] + "','" +
                          gameInfo['gameWeather'] + "','" + gameInfo['vegasLine'] + "', current_timestamp())" +
                          " on duplicate key update gameVegasLine = values(gameVegasLine)")
            try:
                sqlCodes.append(sql)
            except Exception as e:
                print(str(e))
            #run def numbers
            for key, value in defStats.items():
                sql = ("insert into scrapped_data.playerStats (statYear, statWeek, statPlayer, statTeam, statPosition, "+
                       "intTD, forceFumble, fumbleRecov, fumbleTD, puntTD, kickTD, dataCreate) values (" +
                       str(year) + "," + str(week) + ",'" + key + "','" + value['team'] + "','D/ST'," +
                       str(value['intTD']) + "," + str(value['fumF']) + "," + str(value['fumR']) + "," +
                       str(value['fumTD']) + "," + str(value['puntTD']) + "," + str(value['kickTD']) + ", current_timestamp()) " +
                       "on duplicate key update intTD = values(intTD), forceFumble = values(forceFumble), " +
                       "fumbleRecov = values(fumbleRecov), fumbleTD = values(fumbleTD), " +
                       "puntTD = values(puntTD), kickTD = values(kickTD);")
                try:
                    sqlCodes.append(sql)
                except Exception as e:
                    print(str(e))                                    
            #run snap counts
            try:
                snapSQL = "insert into scrapped_data.snapCounts values %s on duplicate key update snapCount = values(snapCount)" % (snapSQLpart[:-1])
                sqlCodes.append(snapSQL)
            except Exception as e:
                print(str(e))
            
            
    except Exception as e:
        print(str(e))
                        


    return sqlCodes
