
import requests
from bs4 import BeautifulSoup as bs, Comment
import sys
from requests.structures import CaseInsensitiveDict
sys.path.insert(0,'..')
sys.path.insert(0,'..\..')

from references import fullName, pfrAbbrName, fullToMascot, abbrToMascot, teamLocation

fullName = CaseInsensitiveDict(fullName)


def pullDepthCharts(season, week, day, time):
    sql = "insert into scrapped_data.depthChart values "

    url = 'http://fftoday.com/nfl/depth.php?o=one_page&order_by='
    
    r = requests.get(url)

    soup = bs(r.content, 'html.parser')
    tables = soup.find_all('table')[7]

    team = ''
    i = 0
    for tr in tables.find_all('tr',recursive=False):
        charts = tr.find_all('td',recursive=False)

        for chart in charts:
            chartTable = chart.find('table').find("table")
            teamRows = chartTable.find_all('tr',recursive=False)
            team = teamRows[0].find('td').get_text()

            try:
                team = fullName[team.replace(' ',' ')]
            except:
                True

            for row in teamRows[2:]:
                cells = row.find_all('td')
                fanPos = cells[0].get_text()
                teamPos = cells[1].get_text()
                player = cells[2].find('a')['href']
                player = player[player.rfind('/')+1:]
                player = player.replace("_"," ").replace("'","_")

                sql += ("(" + str(season) + "," +
                        str(week) + "," +
                        "'" + day + "'," +
                        "'" + time + "'," +
                        str(i) + "," +
                        "'" + team + "'," +
                        "'" + fanPos + "'," +
                        "'" + teamPos + "'," +
                        "'" + player + "'),")
                i += 1

    
    sql = sql[:-1]


    return sql





