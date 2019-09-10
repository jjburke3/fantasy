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


    league = client.get_league(fantasy_league['league_id'], 2019)


            
    trans = league.transactions()
            


    sqlInsert = sqlInsert[:-1]
    sqlInsert2 = sqlInsert2[:-1]
    
    return [sql % sqlInsert, sql2 % sqlInsert2]



pullLeagueData()
