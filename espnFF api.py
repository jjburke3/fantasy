from espnff import League

from espnff import ESPNFF

from security import fantasy_league

client = ESPNFF(fantasy_league['username'], fantasy_league['password'])
try:
    client.authorize()
except AuthorizationError:
    print('failed to authorize')


season = 2018
week = 1

league = client.get_league(fantasy_league['league_id'], 2018)




matchup = league.boxscore(week=1,team=11)

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



print(season, week, teamId[matchup['teamId']], teamId[matchup['opponentId']])

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
