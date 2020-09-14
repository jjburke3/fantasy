from espnff import League

from espnff import ESPNFF

import sys
sys.path.insert(0,'../..')
sys.path.insert(0,'..')
from security import fantasy_league, espn_cookie, swid
from references import fullName

def pullDraftData(year):
    client = ESPNFF(swid=swid, s2=espn_cookie)
    try:
        client.authorize()
    except AuthorizationError:
        print('failed to authorize')

    league = client.get_league(fantasy_league['league_id'], year)

    sql = """insert into la_liga_data.draftData values %s """
    sqlInsert = ''
    sqlInsert2 = ''
    draft = league.draftData()
    for pick in draft:
        sqlInsert += ("(" +
                      str(year) + "," +
                      str(pick['round']) + "," +
                      str(pick['pick']) + ","  +
                      "'" + pick['teamId'] + "'," +
                      "'" + pick['playerName'] + "'," +
                      str(pick['playerId']) + "," +
                      "'" + pick['playerPosition'] + "'," +
                      "'" + pick['nflTeam'] + "'," +
                      "current_timestamp()),")

        
                             
                
            

            


    sqlInsert = sqlInsert[:-1]
    
    return sql % sqlInsert
    


