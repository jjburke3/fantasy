import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from tabulate import tabulate
import sqlite3

import sys
sys.path.insert(0,'..')

from security import sqlite_location

conn = sqlite3.connect(sqlite_location+"/ff_data.db")

c = conn.cursor()

c.execute('drop table if exists draftData;')

c.execute('create table draftData(draftYear integer, round integer, pick integer, team text, ' +
          'player text, pos text, age integer)')
          

conn.commit()

url = 'https://www.pro-football-reference.com/years/%d/draft.htm'

for i in range(1998,2018):
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
            draftValues = (i, row.find_all('th')[0].get_text(), tds[0].get_text(), tds[1].get_text(), tds[2].get_text().replace("'","_"), tds[3].get_text(), nullValue(tds[4].get_text()))
            c.execute("insert into draftData values (%s, %s, %s, '%s', '%s', '%s', %s);" % draftValues)

    conn.commit()

conn.close()
