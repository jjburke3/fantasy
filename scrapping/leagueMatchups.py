from espnff import League

from espnff import ESPNFF

from security import fantasy_league

import sys
sys.path.insert(0,'..')

from DOConn import connection
from DOsshTunnel import DOConnect



with DOConnect() as tunnel:
    c, conn = connection(tunnel)

    client = ESPNFF(fantasy_league['username'], fantasy_league['password'])
    try:
        client.authorize()
    except AuthorizationError:
        print('failed to authorize')


    season = 2018
    week = 1

    league = client.get_league(fantasy_league['league_id'], 2018)

    sql = 'insert into la_liga_data.matchups values '

    for week in range(1,14):
        for team in range(1,15):
            matchup = league.boxscore(week=week,team=team)

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
                      14 : 'Mark Krizmanich'}

            sql += ('(' + str(season) + ',' +
                    str(week) + ',' +
                    "'" + teamId[matchup['teamId']] + "'," +
                    "'" + teamId[matchup['opponentId']] +"'),")


    sql = sql[:-1]

    c.execute(sql)

    conn.commit()


    conn.close()
