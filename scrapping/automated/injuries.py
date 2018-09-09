
import requests
from bs4 import BeautifulSoup as bs, Comment
import sys
from requests.structures import CaseInsensitiveDict
sys.path.insert(0,'..')
sys.path.insert(0,'..\..')

from references import fullName, pfrAbbrName, fullToMascot, abbrToMascot, teamLocation

fullName = CaseInsensitiveDict(fullName)


def pullInjuries(season, week, day, time):
    sql = "insert into scrapped_data.injuries values "
    if season < 2017 or season > 2017:
        urlTag = 'injury'
    else:
        urlTag = 'injury_report'

    url = ('http://fftoday.com/nfl/%d_%s_wk%d.html' %
        (int(str(season)[-2:]), urlTag, week))

    r = requests.get(url)

    soup = bs(r.content, 'html.parser')

    table = soup.find_all('table', {'class' : 'smallbody'})[0]

    team = ''

    i = 0
    for tr in table.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) > 1 and tds[0].get_text() not in ('Name',''):
            if tds[1].get_text() == '':
                team = tds[0].get_text()
                team = team.replace(' ',' ')
                try:
                    team = fullName[team]
                except:
                    True
                try:
                    team = teamLocation[team]
                except:
                    True
                try:
                    team = fullName[team.replace(' Injuries','')]
                except:
                    True

            else:
                player = tds[0].get_text()
                position = tds[1].get_text()
                injury = tds[2].get_text()
                if len(tds) == 5:
                    gameStatus = tds[4].get_text()
                else:
                    gameStatus = tds[3].get_text()


                sql += ("(" + str(season) + "," + str(week) + "," +
                        "'" + day + "','" + time + "'," + str(i) + "," +
                        "'" + team + "'," +
                        "'" + player.replace("'","_").replace("’","_") + "'," +
                        "'" + position + "'," +
                        "'" + injury.replace("'","_") + "'," +
                        "'" + gameStatus.replace("'","_") + "'),")

                i += 1



    sql = sql[:-1]


    return sql




