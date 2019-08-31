import pymysql
from espnff import League, ESPNFF, playerPos, nflTeamsAbbrev

import sys
sys.path.insert(0,'../..')
sys.path.insert(0,'..')
from security import fantasy_league
from references import fullName

sqlScript = ('''insert into draft.availplayers
    (id, player, position, team)
    values''')

client = ESPNFF(fantasy_league['username'], fantasy_league['password'])
try:
    client.authorize()
except AuthorizationError:
    print('failed to authorize')


league = client.get_league(fantasy_league['league_id'], 2019)

for playerId, player in league.players.items():
    if player['position'] in playerPos:

        sql = ("(" +
               str(playerId) + "," +
               "'" + player['player'].replace("'","''") + "'," +
               "'" + playerPos[player['position']] + "'," +
               "'" + nflTeamsAbbrev[player['team']] + "'" +
               "),")

        sqlScript += sql

conn = pymysql.connect(host="localhost",
                       user="root",
                       passwd="",
                       db="draft")



c = conn.cursor()
c.execute("truncate draft.availplayers")
sqlScript = sqlScript[:-1]
c.execute(sqlScript)

conn.commit()

conn.close()
