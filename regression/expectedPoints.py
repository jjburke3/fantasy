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

         
    data = pd.read_sql('SELECT ifnull(rushPoints,0) as yearPoints, ' +
                       ' ifnull(priorYearPoints,0) as priorYearPoints, ' +
                       ' ifnull(priorYearGamesPlayed,0) as priorYearGamesPlayed, ' +
                       " case when playerAge < 29 then 'Young' " +
                       " else 'Old' end as playerAge, " +
                       ' olineRun, ' +
                       " case when depthChart > 5 or depthChart is null "
                       ' then 5 else depthChart end as depthChart, ' +
                       ' playerPosition, ' +
                       " if(draftYear = calYear,'R','') as rookie, " +
                       " priorYearDYAR_rush as dyar, priorYearDVOA_rush as dvoa " +
                       ' FROM analysis.yearStats ' +
                       "where calYear between 2011 and 2017" +
                       ' and priorYearPoints is not null' +
                       " and priorYearDYAR_rush is not null " +
                       " and olineRun is not null ", con=conn)


    ## sns.countplot(y="adPosition", data=data)
    ## plt.show()
    dataPlot = data.loc[data['playerPosition'] == 'RB']

    dataPlot = dataPlot.loc[:,['yearPoints','priorYearPoints','gamesPlayed',
                                  'priorYearGamesPlayed','playerAge','olineRun',
                                  'depthChart','rookie','dyar','dvoa']]
    ##dataPlot.drop(dataPlot.columns[[0,1, 2]],
    ##          axis=1, inplace=True)
    #sns.heatmap(dataPlot.corr())
    
    #plt.show()
    
    X = pd.concat([
        dataPlot[['dyar','olineRun']],
        pd.get_dummies(dataPlot['depthChart'],drop_first=True),
        pd.get_dummies(dataPlot['playerAge'],drop_first=True)],axis=1)
    X = sm.add_constant(X)
    Y = dataPlot['yearPoints']
    print(X.shape)
    print(Y.shape)
    
    #reg = LinearRegression()

    #model = reg.fit(X,Y)


    #print(model.intercept_)
    #print(model.coef_)

    model = sm.OLS(Y,X).fit()

    print(model.summary())
    
    
    conn.close()
