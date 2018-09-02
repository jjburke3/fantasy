import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import pylab
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import statsmodels.api as sm
import scipy
#import plotly.plotly as py
#import plotly.graph_objs as go

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

         
    data = pd.read_sql("select draftYear, draftRound, draftPick, " +
                       "selectingTeam, player, playerPosition, ifnull(round(points,1),0) as points, " +
                       "ifnull(round(points,1),0) - replacePoints as pointsOverReplace, " +
                       "yearsPro " +
                       " from la_liga_data.draftData " +
                       "left join (select statYear, statPlayer, statPosition, " +
                       "sum(totalPoints) as points " +
                       "from scrapped_data.playerStats " +
                       "group by 1,2,3) b on draftYear = statYear and player = statPlayer  " +
                       "	and playerPosition = statPosition " +
                       "join analysis.replacementValue on " +
                       "replaceYear = draftYear and replacePosition = " +
                       "playerPosition " +
                       "left join analysis.expectedAdvanced on "+
                       "adYear = draftYear and adPLayer = player and adPosition = playerPosition " +
                       "    where draftYear > 2010 ", con=conn)

    #selectingTeam = 'JJ Burke'
    #data = data.loc[data['selectingTeam']==selectingTeam]

    dataPlot = data

    X = dataPlot['draftPick']
    Y = dataPlot['pointsOverReplace']
    def func(x, a, b, c):
        return a *np.exp(-b*x) + c

    popt, pcov = scipy.optimize.curve_fit(func,X,Y)
    xx = range(1,225)
    yy = func(xx, *popt)
    sigma_yy = np.sqrt(np.diagonal(pcov))
    bound_upper = func(xx, *(popt + sigma_yy))
    bound_lower = func(xx, *(popt - sigma_yy))
    #fig, ax = plt.subplots()
    #ax.plot(xx,yy)
    #ax.fill_between(xx,bound_lower,bound_upper,color = 'blue', alpha = .15)
    
    groups = data.groupby('playerPosition')

    
    for name, group in groups:
        fig, ax = plt.subplots()
        ax.margins(0.05)
        X = group['draftPick']
        Y = group['pointsOverReplace']
        popt2, pcov2 = scipy.optimize.curve_fit(func,X,Y)
        yy2 = func(xx, *popt2)
        ax.plot(xx,yy)
        ax.fill_between(xx,bound_lower,bound_upper,color = 'blue', alpha = .15)
    
        ax.plot(xx,yy2,label=name)
        ax.plot(group['draftPick'],group['pointsOverReplace'],
                marker='o',linestyle='',ms=5,label=name)

        ax.legend()
        pylab.title(name)
        plt.show()


    
    ## sns.countplot(y="adPosition", data=data)
    ## plt.show()
    positions = ['QB','RB','WR','TE','K','D/ST']
    #plt.show()
    '''
    for i, pos in enumerate(positions):
        plt.figure()
        dataPlot = data.loc[data['playerPosition']==pos]
        dataPlot2 = dataPlot.loc[data['yearsPro']==0]
        dataPlot = dataPlot.loc[data['yearsPro']!=0]
        #sns.scatterplot(dataPlot['draftPick'],dataPlot['points'],hue=i).set_title(pos)
        #plt.show()
        
        X = dataPlot['draftPick']
        Y = dataPlot['pointsOverReplace']
        X2 = dataPlot2['draftPick']
        Y2 = dataPlot2['pointsOverReplace']
        
        plt.plot(X,Y,'b.')
        plt.plot(X2,Y2,'r.')
        plt.plot(xx,yy)
        pylab.title(pos)'''
        

        

        

        #model = np.powfit(X,Y,2)

        #np.linspace(-2,6,100)
        #p = np.poly1d(model)
        #_ = plt.plot(X,Y, '.',xp,p(xp),'-')
    
        #plt.show()
        

    '''X = dataPlot[['priorYearPoints']]
    X = sm.add_constant(X)
    Y = dataPlot['yearPoints']
    
    reg = LinearRegression()

    model = reg.fit(X,Y)


    print(model.intercept_)
    print(model.coef_)

    model = sm.OLS(Y,X).fit()

    print(model.summary())'''

    
    conn.close()
