import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

plt.rc("font", size=14)
sns.set(style="white")
sns.set(style="whitegrid", color_codes=True)

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

         
    data = pd.read_sql('SELECT * FROM analysis.expectedAdvanced', con=conn)


    ## sns.countplot(y="adPosition", data=data)
    ## plt.show()
    qbs = data.loc[data['adPosition'] == 'QB']
    rbs = data.loc[data['adPosition'] == 'RB']
    wrs = data.loc[data['adPosition'] == 'WR']
    tes = data.loc[data['adPosition'] == 'TE']
    ks = data.loc[data['adPosition'] == 'K']
    defs = data.loc[data['adPosition'] == 'D/ST']
    defsPlot = data.loc[data['adPosition'] == 'D/ST']
    defsPlot = defsPlot.loc[defsPlot['adYear'] < 2018]
    defsPlot.drop(defsPlot.columns[[0,1,2,3,4,
                                    5,6,7,8,9,10,11,12,13,
                                    14,15,16,17,18,19,20,21,22,
                                    24,25,28,29,30,31]],
              axis=1, inplace=True)


    defX = defsPlot['priorDefDVOA']
    defY = defsPlot['actualDefDVOA']

    reg = LinearRegression()

    model = sm.OLS(defY,defX).fit()

    defs['exDefDVOA'] = model.predict(defs['priorDefDVOA'])

    #defs['exDefDVOA'] = model.predict(defX)
    updateSQL = ('update analysis.yearStats ' +
                 'join (')
    for index, row in defs.iterrows():
        updateSQL += "select convert(" + str(row['adYear']) + " using utf8) as adYear,"
        updateSQL += "convert('" +row['adPlayer'] + "' using utf8) as adPlayer,"
        updateSQL += "convert(" + str(row['exDefDVOA']) + " using utf8) as exDVOA UNION ALL "

    updateSQL = updateSQL[:-11]
    updateSQL += (") b on adYear = calYear and adPlayer = player " +
                  "set exDefDVOA = exDVOA;")


    c.execute(updateSQL)
    conn.commit()

    
    conn.close()
