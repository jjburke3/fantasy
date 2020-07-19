
import requests
import re
from bs4 import BeautifulSoup as bs, Comment
import sys
from requests.structures import CaseInsensitiveDict
sys.path.insert(0,'..')
sys.path.insert(0,'..\..')

from references import fullName, pfrAbbrName, fullToMascot, abbrToMascot, teamLocation

fullName = CaseInsensitiveDict(fullName)


def pullDepthCharts(season, week, day, time, url = 'https://subscribers.footballguys.com/apps/depthchart.php', timestamp = 'NULL'):
    deleteSql = ''' delete from scrapped_data.depthCharts where
                chartSeason = %s and chartWeek = %s and
                chartDay = '%s' and chartTime = '%s' ''' % (season, week,day,time)
    sql = "insert into scrapped_data.depthCharts values "
    
    params = {'type': 'noidp', 'lite':'no','exclude_coaches':'yes'}
    #url = 'https://subscribers.footballguys.com/apps/depthchart.php'
    
    r = requests.get(url)
    roles = {'red' : 'Injury Replacement', 'blue' : 'Starter', 'green': 'Situational', 'black' : 'Practice'}

    soup = bs(r.content, 'html.parser')
    tables = soup.find_all('td', {"class":"la","width" : "50%"})

    paren = re.compile(" \((.+)\)")
    
    for column in tables:
        teamRows = column.find_all("tr")
        teamName = ''
        for i, team in enumerate(teamRows):
            if i % 2 == 0:
                teamName = team.find("b").text
            else:
                children = team.find("td").findChildren()
                position = ''
                posRank = 0
                
                for child in children:
                    if child.name == "b":
                        position = child.text[:-1]
                        posRank = 0
                    elif child.name == "font" or (position=="Coaches" and child.name=="a"):
                        player = child.text
                        injuryStatus = ''
                        tdb = 0
                        gl = 0
                        kr = 0
                        pr = 0
                        if position =="Coaches":
                            role = re.sub(': ','',re.sub(', ','',child.previousSibling))
                        elif child.name == "font":
                            extra = paren.search(player)
                            if extra:
                                extra = extra.group(1)
                                player = paren.sub('',player)
                            else:
                                extra = ''
                            try:
                                role = roles[child['color']]
                            except:
                                role = "None"
                            if re.match("IR",extra):
                                injuryStatus = 'IR'
                            elif re.match('inj',extra):
                                injuryStatus = 'Injured'
                            elif re.match('susp',extra):
                                injuryStatus = 'Suspended'
                            elif re.match('res',extra):
                                injuryStatus = 'Reserve'
                            elif re.match('PUP',extra):
                                injuryStatus = 'PUP'
                            if re.match("3RB",extra):
                                tdb = 1
                            if re.match("SD",extra):
                                gl = 1
                            if re.match("KR",extra):
                                kr = 1
                            if re.match("PR",extra):
                                pr = 1
                        sql += ("(" +
                                "null" + "," +
                                "null" + "," +
                                "" + str(season) + "," +
                                "" + str(week) + "," +
                                "'" + str(day) + "'," +
                                "'" + str(time) + "'," +
                                "'" + teamName + "'," +
                                "'" + position + "'," +
                                str(posRank) + "," +
                                "'" + player.replace("'","_").replace("′","_") + "'," +
                                "'" + role + "'," +
                                "'" + injuryStatus + "'," +
                                "'" + str(tdb) + "'," +
                                "'" + str(gl) + "'," +
                                "'" + str(kr) + "'," +
                                "'" + str(pr) + "'," +
                                
                                "" + str(timestamp) + "),")
                        posRank += 1

                        
    
    sql = sql[:-1]

    
    return [sql]


