
import requests
import pandas as pd
import sqlite3

import sys
sys.path.insert(0,'..')

from security import sqlite_location

conn = sqlite3.connect(sqlite_location+"/ff_data.db")

c = conn.cursor()

'''
c.execute("create table depthCharts (name text, team text, position text, " +
          "chartPos int, season int, " +
          "week int, period text);")
'''
c.execute("delete from depthCharts;")
conn.commit()

season = 2018
week = 0
period = ''

from bs4 import BeautifulSoup

r = requests.get('https://www.ourlads.com/nfldepthcharts/depthcharts.aspx')
soup = BeautifulSoup(r.content, 'html.parser')
table = soup.find_all('table', 0)

tdf = pd.read_html(str(table), flavor='bs4')[0]

tdf = tdf.iloc[1:20,0:]
priorPos = ''
for index, row in tdf.iterrows():
    if row[1] == row[1]:
        team = row[0]
        pos = row[1]
        playerCells = [3,5,7,9,11]
        if pos != priorPos:
            chartPos = 0
        for player in playerCells:
            if row[player] == row[player]:
                playerName = row[player]
                lastName = playerName.split(',')[0]
                firstName = playerName.split(', ',1)[1]
                firstName = firstName[:firstName.rindex(' ')]
                chartPos += 1
                priorPos = pos
                info = {'team' : team,
                        'position' : pos,
                        'player' : firstName + " " + lastName,
                        'chartPos' : chartPos}
                c.execute("insert into depthCharts values ("+
                          "'" + info['player'] + "'," +
                          "'" + info['team'] + "'," +
                          "'" + info['position'] + "'," +
                          str(info['chartPos']) + "," +
                          str(season) + "," +
                          str(week) + "," +
                          "'" + period + "'" +
                          ");")
                conn.commit()

conn.close()
