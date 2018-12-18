from espnff import League

from espnff import ESPNFF

import sys
sys.path.insert(0,'../..')
sys.path.insert(0,'..')
from security import fantasy_league
from references import fullName

def pullLeagueData():
    client = ESPNFF(fantasy_league['username'], fantasy_league['password'])
    try:
        client.authorize()
    except AuthorizationError:
        print('failed to authorize')


    league = client.get_league(fantasy_league['league_id'], 2018)

    sql = """insert into la_liga_data.pointsScored values %s
            on duplicate key update
            vsTeam = values(vsTeam),
            player = values(player),
            playerTeam = values(playerTeam),
            playerSlot = values(playerSlot),
            playerPosition = values(playerPosition),
            playerPosition2 = values(playerPosition2),
            opponent = values(opponent),
            points = values(points),
            dataCreate = current_timestamp();"""
    sql2 = """insert into la_liga_data.wins values %s
            on duplicate key update
            winPoints = values(winPoints),
            winPointsAgs = values(winPointsAgs),
            winWin = values(winWin),
            winLoss = values(winLoss),
            winTie = values(winTie),
            dataCreate = current_timestamp();"""
    sqlInsert = ''
    sqlInsert2 = ''
    for team in range(1,15):
        matchup = league.boxscore(week=14,team=team)
        teamId = {1 : 'Andrew Lamb',
                  2 : 'Billy Beirne',
                  3 : 'Tom Buckley',
                  4 : 'JJ Burke',
                  5 : 'mike guiltinan',
                  6 : 'Chris Hammitt',
                  7 : 'Matthew Singer',
                  8 : 'Chris Curtin',
                  9 : 'Mike DeRusso',
                  10 : 'Joe Young',
                  11 : 'Ricky Garcia',
                  12 : 'Jordan Hiller',
                  13 : 'Parker King',
                  14 : 'Mark Krizmanich',
                  0 : ''}

        teamName = teamId[matchup['teamId']]
        season = matchup['season']
        week = matchup['week']
        teamPoints = matchup['teamPoints']
        opp = teamId[matchup['opponentId']]
        oppPoints = matchup['opponentPoints']
        win = int(teamPoints > oppPoints)
        loss = int(teamPoints < oppPoints)
        tie = int(teamPoints == oppPoints)

        sqlInsert2 += ("(" + str(season) + "," +
                       str(week) + "," +
                       "'" + teamName + "'," +
                       "'" + opp + "'," +
                       str(teamPoints) + "," +
                       str(oppPoints) + "," +
                       str(win) + "," +
                       str(loss) + "," +
                       str(tie) + "," +
                       "null," +
                       "current_timestamp()),")

        for i, player in enumerate(matchup['playerList']):
            try:
                sqlInsert += ("(" + str(season) + "," +
                             str(week) + "," +
                             "'" + teamName + "'," +
                             str(i) + "," +
                             "'" + opp + "'," +
                             "'" + player['playerName'].replace("'","_") + "'," +
                             "'" + fullName[player['playerTeam']] + "'," +
                              "'" + player['slot'] + "'," +
                              "'" + player['playerPos'] + "'," +
                              "null," +
                              "null," +
                              "null," +
                              str(player['Points']) + "," +
                              "current_timestamp()),")
            except:
                True

        
                             
                
            

            


    sqlInsert = sqlInsert[:-1]
    sqlInsert2 = sqlInsert2[:-1]
    
    return [sql % sqlInsert, sql2 % sqlInsert2]

