import json
from pprint import pprint

import sys
sys.path.insert(0,'../..')

from DOConn import connection
from DOsshTunnel import DOConnect

with DOConnect() as tunnel:
    c, conn = connection(tunnel)

    with open('eligiblePlayers.json', encoding='utf-8') as data_file:
        data = json.loads(data_file.read())

        sqlCode = 'insert into scrapped_data.currentAvailable values '

        for row in data:
            playerData = {}
            playerData['player'] = (row['fn'].replace("'",'_') + ' ' +
                                    row['ln'].replace("'",'_'))
            playerData['pos'] = row['tph'][row['tph'].index(' ')+1:]
            playerData['team'] = row['tph'][:row['tph'].index(' ')]
            playerData['projPoints'] = row['ps']
            playerData['passYard'] = row['st'][0]
            playerData['passTD'] = row['st'][1]
            playerData['passINT'] = row['st'][2]
            playerData['rushYard'] = row['st'][3]
            playerData['rushTD'] = row['st'][4]
            playerData['recept'] = row['st'][5]
            playerData['receivYard'] = row['st'][6]
            playerData['receivTD'] = row['st'][7]
            playerData['defInt'] = row['st'][8]
            playerData['defFR'] = row['st'][9]
            playerData['defPA'] = row['st'][10]
            playerData['defYA'] = row['st'][11]

            sqlCode += "(2018, '" + playerData['player'] + "',"
            sqlCode += "'" + playerData['pos'] + "',"
            sqlCode += "'" + playerData['team'] + "',"
            sqlCode += "'" + playerData['passYard'] + "',"
            sqlCode += "'" + playerData['passTD'] + "',"
            sqlCode += "'" + playerData['passINT'] + "',"
            sqlCode += "'" + playerData['rushYard'] + "',"
            sqlCode += "'" + playerData['rushTD'] + "',"
            sqlCode += "'" + playerData['recept'] + "',"
            sqlCode += "'" + playerData['receivYard'] + "',"
            sqlCode += "'" + playerData['receivTD'] + "',"
            sqlCode += "'" + playerData['defInt'] + "',"
            sqlCode += "'" + playerData['defFR'] + "',"
            sqlCode += "'" + playerData['defPA'] + "',"
            sqlCode += "'" + playerData['defYA'] + "',"
            sqlCode += "'" + str(playerData['projPoints']) + "'),"
            
        sqlCode = sqlCode[:-1]

        c.execute(sqlCode)
        conn.commit()


    conn.close()
