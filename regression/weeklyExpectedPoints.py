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



with DOConnect() as tunnel:
    c, conn = connection(tunnel)

         
    data = pd.read_sql("""select a.winPoints - (select avg(c.winPoints) from 
	la_liga_data.wins c where c.winWeek <= 13 and c.winSeason = a.winSeason)
 as donePoints, 
 ifnull(preDraftCapital,(select avg(preDraftCapital) from analysis.preDraftCapital)) as preDraftCapital,
 b.winPoints as predictPoints, ifnull(a.winTeam,preDraftTeam) as winTeam, 
 ifnull(a.winSeason,preDraftYear) as winSeason, b.winWeek from analysis.preDraftCapital 

left join la_liga_data.wins a on a.winSeason = preDraftYear and a.winTeam = preDraftTeam and a.winWeek = 1
left join la_liga_data.wins b on a.winSeason = b.winSeason and b.winWeek > a.winWeek and a.winTeam = b.winTeam
	and b.winWeek <= 13""", con=conn)

    data2 = data.loc[data['winSeason'] <= 2017]


    X = data[['preDraftCapital']]
    Y = data['predictPoints']
    X2 = data2[['preDraftCapital']]
    Y2 = data2['predictPoints']
    X2 = sm.add_constant(X2)
    X = sm.add_constant(X)

    reg = LinearRegression()

    model = sm.OLS(Y2,X2).fit()

    predictData = data.loc[data['winSeason'] == 2018]

    predicts = model.predict(X)

    '''for index, row in data.iterrows():
        print(row['winSeason'], row['winWeek'], row['winTeam'], row['predictPoints'], predicts[index])
    '''
    coefs = model.params
    se = model.bse

    rand = np.random.normal(0,.1,1)
    print('start sim')
    for j in range(1,1001):
        for index, row in predictData.iterrows():

            for i in range(1,13):
            
                result = (np.random.normal(coefs['const'],
                                           se['const'],
                                           1) +
                          (np.random.normal(coefs['preDraftCapital'],
                                            se['preDraftCapital'],
                                            1))*row['preDraftCapital'])

        
    print('end sim')




    
    conn.close()
