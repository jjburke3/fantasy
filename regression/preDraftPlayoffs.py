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



sql = """select a.*, if(count(winWin)>0,1,0) as playoffs
from (
select draftYear, selectingTeam,
sum(greatest(actualPickValue,0)) as draftCapital

from (select a.draftYear,
a.draftRound, 
a.draftPick,
a.selectingTeam,
a.player,
a.playerPosition,
a.playerTeam,
if(b.draftYear is null,'N','Y') as keeper,
preRank,
least(ifnull(preRank,999),a.draftPick +
(select count(*)
from (
select draftYear, draftPick, player,
keeperPick, preRank,
@row := if(@label = concat(draftYear,'-',draftPick),
@row + 1,draftPick) as addPick,
@label := concat(draftYear,'-',draftPick)
from (
select d.draftYear, d.draftPick, d.player,
e.draftPick as keeperPick, preRank
from la_liga_data.draftData d
join 
(select e.*, preRank from la_liga_data.keepers e
join scrapped_data.preRanks f on preYear = e.draftYear and prePlayer = e.player and prePosition = position) e
on e.draftYear = d.draftyear and e.draftPick > d.draftPick
order by d.draftYear, d.draftPick, preRank) d
join (select @row := 0, @label := cast('' as char)) t) d
where addPick >= preRank and d.draftYear = a.draftYear and d.draftPick = a.draftPick
)) as actualPick


from la_liga_data.draftData a

left join la_liga_data.keepers b on a.draftYear = b.draftYear and a.player = b.player and a.playerPosition = b.position
left join scrapped_data.preRanks c on preYear = b.draftYear and prePlayer = b.player and prePosition = position
where a.draftYear between 2011 and 2017
) b
left join 
refData.pickValue on actualPick = pickNumber
group by 1,2 ) a
left join la_liga_data.wins on winSeason = draftYear and selectingTeam = winTeam and playoffs is not null
group by 1,2,3

"""


with DOConnect() as tunnel:
    c, conn = connection(tunnel)

         
    data = pd.read_sql(sql, con=conn)


    dataPlot = data

    X = dataPlot['draftCapital']
    xMin = int(round(min(X),0))
    xMax = int(round(max(X),0))
    X = sm.add_constant(X)
    Y = dataPlot['playoffs']

    glm_binom = sm.Logit(Y,X)


    xx = range(xMin,xMax)

    x2018 = [815.702261328697,
773.722952842712,
718.61446237564,
715.221795082092,
698.794709384441,
605.876345872879,
579.210064172744,
561.754466056823,
530.88414978981,
510.965470314025,
506.061405420303,
456.482367753982,
443.097253322601,
441.711277008056
             ]

    xx2 = sm.add_constant(xx)
    
    x20182 = sm.add_constant(x2018)
    results = glm_binom.fit()

    print(results.summary())

    yy = results.predict(xx2)

    y2018 = results.predict(x20182)
    print(y2018)
    fig, ax = plt.subplots()
    ax.plot(xx,yy)
    ax.plot(x2018,y2018,marker="o")
    #ax.fill_between(xx,bound_lower,bound_upper,color = 'blue', alpha = .15)
    plt.show()

    '''
    
    for name, group in groups:
        fig, ax = plt.subplots()
        ax.margins(0.05)
        X = group['actualPick']
        Y = group['pointsOverReplace']
        popt2, pcov2 = scipy.optimize.curve_fit(func,X,Y)
        yy2 = func(xx, *popt2)
        ax.plot(xx,yy)
        ax.fill_between(xx,bound_lower,bound_upper,color = 'blue', alpha = .15)
    
        ax.plot(xx,yy2,label=name)
        ax.plot(group['actualPick'],group['pointsOverReplace'],
                marker='o',linestyle='',ms=5,label=name)

        ax.legend()
        pylab.title(name)
        plt.show()


    
    ## sns.countplot(y="adPosition", data=data)
    ## plt.show()
    positions = ['QB','RB','WR','TE','K','D/ST']
    #plt.show()
    
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
