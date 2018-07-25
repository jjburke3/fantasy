from espnff import League

from espnff import ESPNFF

from security import fantasy_league

client = ESPNFF(fantasy_league['username'], fantasy_league['password'])
try:
    client.authorize()
except AuthorizationError:
    print('failed to authorize')

league = client.get_league(fantasy_league['league_id'], 2017)




matchup = league.scoreboard(week=1)



print(matchup)
