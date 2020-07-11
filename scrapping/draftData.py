import requests
from bs4 import BeautifulSoup as bs

import sys
sys.path.insert(0,'..')

from DOConn import connection
from DOsshTunnel import DOConnect


'''
create table scrapped_data.draft (draftYear integer, 
    draftRound integer, draftPick integer, 
    draftTeam varchar(25), draftPlayer varchar(50),
    pos varchar(25), age integer,
    dataCreate datetime,
    primary key (draftYear, draftRound, draftPick))
'''

with DOConnect() as tunnel:
    c, conn = connection(tunnel)

         
    url = 'https://www.pro-football-reference.com/years/%d/draft.htm'

    for i in range(1999,2019):
        url2 = url % i

        req = requests.get(url2)


        xml = bs(req.text, 'lxml')

        def nullValue(string):
            if not string:
                return 'null'
            else:
                return string


        table = xml.find_all('table')[0]
        for row in table.find_all('tr'):
            tds = row.find_all('td')
            if len(tds) > 0:
                draftValues = (i, row.find_all('th')[0].get_text(), tds[0].get_text(),
                               tds[1].get_text(), tds[2].get_text().replace("'","_"),
                               tds[3].get_text(), nullValue(tds[4].get_text()))
                try:
                    c.execute("insert into scrapped_data.draft values (%s, %s, %s, '%s', '%s', '%s', %s, current_timestamp());" % draftValues)
                except:
                    print('error')
        conn.commit()

        print("Draft Year",str(i),"Finished")

    conn.close()
