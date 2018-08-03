'''
http://api.fantasy.nfl.com/v1/players/stats?statType=weekStats&season=2017&week=1&format=json
players/advanced
players/researchinfo
players/editorweekranks
players/editorweekranks
'''

import requests
import pandas as pd
import sqlite3

import sys
sys.path.insert(0,'..')

from security import sqlite_location

conn = sqlite3.connect(sqlite_location+"/ff_data.db")

c = conn.cursor()

c.execute('drop table if exists playerStats;')

c.execute('create table playerStats(season integer, week integer, '+
          'player text, position text, team text, stat text, '+
          'value float);')

conn.commit()

url = 'http://api.fantasy.nfl.com/v1/players/stats?statType=weekStats&season=%d&week=%d&format=json'

r = requests.get(url % (2017,9))

data = r.json()

players = data['players']

statDict = {1 : '',
            2 : 'Passing Attempts',
            3 : 'Completions',
            4 : 'Incompletions',
            5 : 'Passing Yards',
            6 : 'Passing TD',
            7 : 'Interceptions Thrown',
            8 : 'QB Sacks',
            9 : '300-399 Passing Yards Bonus',
            10 : '400+ Passing Yards Bonus',
            11 : '40+ Passing Yard TD Bonus',
            12 : '50+ Passing Yards TD Bonus',
            13 : 'Rushing Attempts',
            14 : 'Receiving Yards',
            15 : 'Rushing Touchdowns',
            16 : '40+ Rushing Yard TD Bonus',
            17 : '50+ Rushing Yard TD Bonus',
            18 : '100-199 Rushing Yards Bonus',
            19 : '200+ Rushing Yards Bonus',
            20 : 'Receptions',
            21 : 'Receiving Yards',
            22 : 'Receiving Touchdowns',
            23 : '40+ Receiving Yard TD Bonus',
            24 : '50+ Receiving Yard TD Bonus',
            25 : '100-199 Receiving Yards Bonus',
            26 : '200+ Receiving Yards Bonus',
            27 : 'Kickoff and Punt Return Yards',
            28 : 'Kickoff and Punt Return Touchdowns',
            29 : 'Fumble Recovered for TD',
            30 : 'Fumbles Lost',
            31 : 'Fumble',
            32 : '2-Point Conversions',
            33 : 'PAT Made',
            34 : 'PAT Missed',
            35 : 'FG Made 0-19',
            36 : 'FG Made 20-29',
            37 : 'FG Made 30-39',
            38 : 'FG Made 40-49',
            39 : 'FG Made 50+',
            40 : 'FG Missed 0-19',
            41 : 'FG Missed 20-29',
            42 : 'FG Missed 30-39',
            43 : 'FG Missed 40-49',
            44 : 'FG Missed 50+',
            45 : 'Sacks',
            46 : 'Interceptions',
            47 : 'Fumbles Recovered',
            48 : 'Fumbles Forced',
            49 : 'Safeties',
            50 : 'Defensive Touchdowns',
            51 : 'Blocked Kicks',
            52 : 'Kickoff and Punt Return Yards',
            53 : 'Kickoff and Punt Return Touchdowns',
            54 : 'Points Allowed',
            55 : 'Points Allowed 0',
            56 : 'Points Allowed 1-6',
            57 : 'Points Allowed 7-13',
            58 : 'Points Allowed 14-20',
            59 : 'Points Allowed 21-27',
            60 : 'Points Allowed 28-34',
            61 : 'Points Allowed 35+',
            62 : 'Yards Allowed',
            63 : 'Less than 100 Total Yards Allowed',
            64 : '100-199 Yards Allowed',
            65 : '200-299 Yards Allowed',
            66 : '300-399 Yards Allowed',
            67 : '400-449 yards Allowed',
            68 : '450-499 Yards Allowed',
            69 : '500+Yards Allowed',
            70 : 'Tackle',
            71 : 'Assisted Tackles',
            72 : 'Sacks',
            73 : 'Defensive Interception',
            74 : 'Forced Fumble',
            75 : 'Fumbles Recovery',
            76 : 'INT Touchdown',
            77 : 'Fumble Touchdown',
            78 : 'Blocked Kick Touchdown',
            79 : 'Safety',
            80 : 'Pass Defended',
            81 : 'INT Return Yards',
            82 : 'Fumble Return Yards',
            83 : 'Tackles for Loss',
            84 : 'QB Hit',
            85 : 'Sack yards',
            86 : '10+ Tackle Bonus',
            87 : '2+ Sack Bonus',
            88 : '3+ Passes Defended Bonus',
            89 : '50+ Yard INT Return TD Bonus',
            90 : '50+ Yard Fumble Return TD Bonus',
            91 : 'Def 2-Point Return',
            92 : '',
            93 : '',
            94 : '',
            95 : '',
            96 : '',
            97 : '',
            98 : '',
            99 : '',
            100 : '',
            101 : '',
            102 : '',
            103 : '',
            104 : '',
            105 : '',
            106 : '',
            107 : '',
            108 : '',
            109 : '',
            110 : ''
            }

stats = {}

for player in players:
    for key in player['stats']:
        sqlData = {'season' : int(data['season']),
                   'week' : int(data['week']),
                   'Player' : player['name'],
                   'Position' : player['position'],
                   'Team' : player['teamAbbr'],
                   'stat' : key,
                   'value' : player['stats'][key]
                   }
        if statDict[int(key)] != '':
            sqlData['stat'] = statDict[int(key)]

        c.execute("insert into playerStats values (%d, %d, '%s', "
                  "'%s', '%s', '%s', '%s')" %
                  (sqlData['season'],
                   sqlData['week'],
                   sqlData['Player'].replace("'","_"),
                   sqlData['Position'],
                   sqlData['Team'],
                   sqlData['stat'],
                   sqlData['value'])
                  )

        conn.commit()



conn.close()
