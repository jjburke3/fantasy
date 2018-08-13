from espnff import League

from espnff import ESPNFF

from security import fantasy_league

client = ESPNFF(fantasy_league['username'], fantasy_league['password'])
try:
    client.authorize()
except AuthorizationError:
    print('failed to authorize')

league = client.get_league(fantasy_league['league_id'], 2018)




matchup = league.boxscore()



print(matchup)

''' end points
leagueSettings
playerInfo
scoreboard
player/news
recentActivity
leagueSchedules
teams
rosterInfo
schedule
polls
messageboard
boxscore
status
teams/pendingMoveBatches
tweets
stories
livescoring'''
