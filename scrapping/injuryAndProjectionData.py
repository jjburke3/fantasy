'''
pull before draft
pull data every week - Thursday afternoon, Saturday night, sunday morning, sunday afternoon, sunday night, monday afternoon,
tuesday morning
'''

import requests
import pandas as pd
import sqlite3

import sys
sys.path.insert(0,'..')

from security import sqlite_location
from security import swid
from security import espn_cookie
from security import fantasy_league

conn = sqlite3.connect(sqlite_location+"/ff_data.db")

c = conn.cursor()
'''
c.execute("create table injuryData (name text, team text, position text, season int, " +
          "week int, period text, injuryStatus text);")


c.execute("create table projections (name text, team text, position text, season int, " +
          "week int, period text, opponet text, gameTime text, projPoints float, " +
          "oppRank text, startPerc float, ownPerc float);")


c.execute("create table preSeasonProjections (name text, team text, position text, season int, " +
          "preSeasonProjection float);")
'''        

c.execute("delete from injuryData;")
c.execute("delete from projections;")
c.execute("delete from preSeasonProjections;")
conn.commit()
from bs4 import BeautifulSoup

scorePer = 0
season = 2018
continueVar = True
startIndex = 0
if scorePer == 0:
    view = 'projections'
else:
    view = 'overview'

while startIndex == 0:
    #injury data
    r = requests.get('http://games.espn.com/ffl/freeagency',
                         params={'leagueId': fantasy_league['league_id'],
                                 'seasonId': season, 
                                 'scoringPeriodId': scorePer,
                                 'view' : view,
                                 #'slotCategoryId' : 16,
                                 'startIndex' : startIndex},
                         cookies={'SWID': swid, 'espn_s2': espn_cookie})
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('table', class_='playerTableTable')
    tdf = pd.read_html(str(table), flavor='bs4')[0]  # returns a list of df's, grab first
    if tdf.shape[0] == 1:
        continueVar = False
    players = tdf.iloc[2:,0]
    for row in players:
        if 'D/ST' in row:
            info = {'name' : row.split()[0] + ' D/ST',
                    'team' : row.split()[0],
                    'position' : 'D/ST',
                    'injury' : ''}
        else:
            info = {'name' : row.split(',')[0].replace("'","_"),
                    'team' : row.split(',')[1].split('\xa0')[0],
                    'position' : row.split(',')[1].split('\xa0')[1].split()[0],
                    'injury' : ''}
            if len(row.split(',')[1].split('\xa0')[1].split()) > 1:
                info['injury'] = row.split(',')[1].split('\xa0')[1].split()[1]
        if info['injury'] != '':
            c.execute("insert into injuryData values('" + info['name'] + "','" +
                      info['team'] + "','" + info['position'] + "'," + str(season) +
                      "," + str(scorePer) + ",'','" + info['injury'] + "');")
            conn.commit()

    #projections
    # 0 - name, 5 - opp, 6 - game time, 8 - actual ranking, 9 - actual points, 10 - actual average,
    # 11 - last actual points, 13 - proj points, 14 - opp ranking,
    # 15 - % st, 16 - %OWN, 17 - change in own
    if view == 'overview':
        proj = tdf.iloc[2:,[0,5,6,13,14,15,16]]
        for index, row in proj.iterrows():
            if 'D/ST' in row[0]:
                info = {'name' : row[0].split()[0] + ' D/ST',
                        'team' : row[0].split()[0],
                        'position' : 'D/ST'}
            else:
                info = {'name' : row[0].split(',')[0].replace("'","_"),
                        'team' : row[0].split(',')[1].split('\xa0')[0],
                        'position' : row[0].split(',')[1].split('\xa0')[1].split()[0]}
            c.execute("insert into projections values('" + info['name'] + "','" +
                      info['team'] + "','" + info['position'] + "'," + str(season) +
                      "," + str(scorePer) + ",'','" + row[5] + "','" + row[6] + "'," +
                      str(row[13]) + ",'" + row[14] + "'," + str(row[15]) + "," +
                      str(row[16]) + ");")
            conn.commit()
    else:
        proj = tdf.iloc[2:,[0,9]]
        for index, row in proj.iterrows():
            if 'D/ST' in row[0]:
                info = {'name' : row[0].split()[0] + ' D/ST',
                        'team' : row[0].split()[0],
                        'position' : 'D/ST'}
            else:
                info = {'name' : row[0].split(',')[0].replace("'","_"),
                        'team' : row[0].split(',')[1].split('\xa0')[0],
                        'position' : row[0].split(',')[1].split('\xa0')[1].split()[0]}
            c.execute("insert into preSeasonProjections values('" + info['name'] + "','" +
                      info['team'] + "','" + info['position'] + "'," + str(season) +
                      "," + str(row[9]) + ");")
            conn.commit()
        
    startIndex += 50

conn.close()
