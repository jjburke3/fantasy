
import requests
from bs4 import BeautifulSoup as bs, Comment
import sys
from requests.structures import CaseInsensitiveDict
sys.path.insert(0,'..')
sys.path.insert(0,'..\..')

from references import fullName, pfrAbbrName, fullToMascot, abbrToMascot, teamLocation

fullName = CaseInsensitiveDict(fullName)


def pullInjuries(season, week, day, time):
    deleteSql = '''delete from scrapped_data.injuries
            where injSeason = %d and injWeek = %d
            and injDay = '%s' and injTime = '%s' ''' % (season, week, day, time)
    sql = 'insert into scrapped_data.injuries values '

    teamsUrl = "https://www.rotoworld.com/api/team/football?sort=locale&filter%5Bactive%5D=1&filter%5Bleague.meta.drupal_internal__id%5D=21&include=secondary_logo"
    

    teamsR = requests.get(teamsUrl).json()['data']
    
    url2 = 'https://www.rotoworld.com/api/injury?sort=-start_date&filter%5Bplayer.team.meta.drupal_internal__id%5D='
    url3 = '&filter%5Bplayer.status.active%5D=1&filter%5Bactive%5D=1&include=injury_type,player,player.status,player.position'
    url = 'https://www.rotoworld.com/api/injury'

    for teamLink in teamsR:
        r = requests.get(url2 + str(teamLink['attributes']['team_id']) + url3)
        data = r.json()
        for injury in data['data']:
            if injury['relationships']['player']['data']['type'] == "player--football":
                injId = injury['id']
                attributes = {
                    'status' : injury['attributes']['return_estimate'],
                    'startDate' : injury['attributes']['start_date'],
                    'endDate' : injury['attributes']['end_date'],
                    'outlook' : injury['attributes']['outlook'],
                    'active' : injury['attributes']['active']
                    }
                playerData = requests.get(url + "/" + injId + "/player").json()['data']
                playerName = playerData['attributes']['name']
                injuryData = requests.get(url + "/" + injId + "/injury_type").json()['data']
                injuryName = injuryData['attributes']['name']

                positionUrl = playerData['relationships']['position']['links']['related']['href']
                teamUrl = playerData['relationships']['team']['links']['related']['href']
                team = requests.get(teamUrl).json()['data']['attributes']['abbreviation']
                position = requests.get(positionUrl).json()['data']['attributes']['abbreviation']
                statusUrl = playerData['relationships']['status']['links']['related']['href']
                status = requests.get(statusUrl).json()['data']['attributes']['name']

                sql += ("(" +
                        str(season) + "," +
                        str(week) + "," +
                        "'" + day + "'," +
                        "'" + time + "'," +
                        "'" + injId + "'," +
                        "'" + team + "'," +
                        "'" + playerName.replace("'","_") + "'," +
                        "'" + position.replace("'","_") + "'," +
                        "'" + injuryName.replace("'","_") + "'," +
                        "'" + status.replace("'","_") + "'," +
                        ('null' if attributes['startDate'] == None else "'" +str(attributes['startDate']).replace("'","_") + "'") + "," +
                        ('null' if attributes['endDate'] == None else "'" +str(attributes['endDate']).replace("'","_") + "'") + "," +
                        ('null' if attributes['outlook'] == None else "'" + str(attributes['outlook']['value']).replace("'","_") + "'") + "," +
                        "current_timestamp()),"
                        )


    sql = sql[:-1]


    return [deleteSql,sql]




