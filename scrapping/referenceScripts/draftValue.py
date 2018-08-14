import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

import sys
sys.path.insert(0,'../..')

from DOConn import connection
from DOsshTunnel import DOConnect


'''
drop table if exists refData.draftValue;
create table refData.draftValue
(roundValue int, pickValue int, valueAmount float,
primary key(roundValue,pickValue))
'''

with DOConnect() as tunnel:
    c, conn = connection(tunnel)

         
    url = 'http://walterfootball.com/draftchart.php'


    r = requests.get(url)


    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find_all('table')[1]
    tdf = pd.read_html(str(table), flavor='bs4')[0]
    tdf = tdf.iloc[1:,]
    for index, row in tdf.iterrows():
        for round in range(1,8):
            col = (round - 1) * 2 + 1
            value = row[col]
            pick = row[col - 1]
            c.execute("insert into refData.draftValue " +
                      "values ( %d, %d, %s ) " %
                      (int(round), int(pick), value))
            conn.commit()
            
    conn.close()
