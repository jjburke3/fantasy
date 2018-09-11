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
 as donePoints, b.winPoints as weekPoints,
 ifnull(preDraftCapital,(select avg(preDraftCapital) from analysis.preDraftCapital)) as preDraftCapital,
 b.winPoints as predictPoints, lcase(ifnull(a.winTeam,preDraftTeam)) as winTeam, 
 ifnull(a.winSeason,preDraftYear) as winSeason, b.winWeek from analysis.preDraftCapital 

left join la_liga_data.wins a on a.winSeason = preDraftYear and a.winTeam = preDraftTeam and a.winWeek = 0
left join la_liga_data.wins b on preDraftYear = b.winSeason and b.winWeek > ifnull(a.winWeek,0) and preDraftTeam = b.winTeam
	and b.winWeek <= 13""", con=conn)

    matchups = pd.read_sql("""select matchYear, matchWeek, lcase(matchTeam) as matchTeam,
    lcase(matchOpp) as matchOpp from la_liga_data.matchups;""", con=conn)

    data2 = data.loc[data['winSeason'] <= 2017]

    pointsMean = np.mean(data2['weekPoints'])
    pointsSd = np.std(data2['weekPoints'])
    
    def normDist(preDraftCap):
        result = (np.random.normal(pointsMean,
                                           pointsSd,
                                           1)*(1-model.rsquared) +
                          (coefs['const']+
                          (np.random.normal(coefs['preDraftCapital'],
                                            se['preDraftCapital'],
                                            1))*preDraftCap)*model.rsquared)
        return result


    X = data[['preDraftCapital']]
    Y = data['predictPoints']
    X2 = data2[['preDraftCapital']]
    Y2 = data2['predictPoints']
    X2 = sm.add_constant(X2)
    X = sm.add_constant(X)

    reg = LinearRegression()

    model = sm.OLS(Y2,X2).fit()
    print(model.summary())

    predictData = data.loc[data['winSeason'] == 2018]
    summaryData = {}
    for index, row in predictData.iterrows():
        summaryData[row['winTeam']] = {}
        summaryData[row['winTeam']]['wins'] = []
        summaryData[row['winTeam']]['losses'] = []
        summaryData[row['winTeam']]['ties'] = []
        summaryData[row['winTeam']]['points'] = []
        summaryData[row['winTeam']]['playoffs'] = []
        summaryData[row['winTeam']]['champ'] = []
        summaryData[row['winTeam']]['highpoints'] = []
        summaryData[row['winTeam']]['lowpoints'] = []

    predicts = model.predict(X)

    '''for index, row in data.iterrows():
        print(row['winSeason'], row['winWeek'], row['winTeam'], row['predictPoints'], predicts[index])
    '''
    coefs = model.params
    se = model.bse

    rand = np.random.normal(0,.1,1)
    print('start sim')
    #for j in range(1,1001):


    for j in range(0,10000):
        print(j)
        teamDict = {}
        
        for index, row in predictData.iterrows():
            teamDict[row['winTeam']] = {}

            teamDict[row['winTeam']]['pointTotals'] = []

            teamDict[row['winTeam']]['matchup'] = []

            teamDict[row['winTeam']]['wins'] = []

            teamDict[row['winTeam']]['losses'] = []

            teamDict[row['winTeam']]['ties'] = []
        for i in range(1,14):
            for index, row in predictData.iterrows():

                result = normDist(row['preDraftCapital'])
                teamDict[row['winTeam']]['pointTotals'].append(result[0])
                matchup = matchups.loc[(matchups['matchWeek'] == i) &
                                       (matchups['matchTeam'] == row['winTeam'])]
                matchup = matchup.iloc[0][3]
                
                teamDict[row['winTeam']]['matchup'].append(matchup)
            
            for index, row in predictData.iterrows():
                pointsScored = teamDict[row['winTeam']]['pointTotals'][i - 1]
                oppPoints = teamDict[teamDict[row['winTeam']]['matchup'][i-1]]['pointTotals'][i - 1]
                teamDict[row['winTeam']]['wins'].append(pointsScored > oppPoints)
                teamDict[row['winTeam']]['losses'].append(pointsScored < oppPoints)
                teamDict[row['winTeam']]['ties'].append(pointsScored == oppPoints)
        teams = []
        winArray = []
        lossArray = []
        tieArray = []
        pointArray = []
        for index, row in predictData.iterrows():
            wins = sum(teamDict[row['winTeam']]['wins'])
            losses = sum(teamDict[row['winTeam']]['losses'])
            ties = sum(teamDict[row['winTeam']]['ties'])
            points = sum(teamDict[row['winTeam']]['pointTotals'])

            teams.append(row['winTeam'])
            winArray.append(wins)
            lossArray.append(losses)
            tieArray.append(ties)
            pointArray.append(points)
            summaryData[row['winTeam']]['wins'].append(wins)
            summaryData[row['winTeam']]['losses'].append(losses)
            summaryData[row['winTeam']]['ties'].append(ties)
            summaryData[row['winTeam']]['points'].append(points)

        d = {'team' : teams, 'wins' : winArray,
             'losses' : lossArray, 'ties' : tieArray,
             'points' : pointArray}

        df = pd.DataFrame(data=d)

        #high and low points
        df = df.sort_values(['points'], ascending=[0])
        df = df.reset_index(drop=True)
        for index, row in df.iterrows():
            if index < 1:
                highpoints = 1
            else:
                highpoints = 0
            if index == 13:
                lowpoints = 1
            else:
                lowpoints = 0
            summaryData[row['team']]['highpoints'].append(highpoints)
            summaryData[row['team']]['lowpoints'].append(lowpoints)

        #playoffs
        df = df.sort_values(['wins','losses','points'], ascending=[0,1,0])
        df = df.reset_index(drop=True)
        for index, row in df.iterrows():
            if index < 6:
                playoff = 1
            else:
                playoff = 0
            summaryData[row['team']]['playoffs'].append(playoff)
        
        #round 1
        scores = []
        teams = []
        for index, row in df[2:6].iterrows():
            teams.append(index)
            preDraftCap = predictData.loc[predictData['winTeam'] == row['team']]['preDraftCapital']
            preDraftCap = preDraftCap.item()
            scores.append(normDist(preDraftCap))
        advanceTeams = []

        if scores[3] > scores[0]:
            advanceTeams.append(teams[3])
        else:
            advanceTeams.append(teams[0])
            
        if scores[2] > scores[1]:
            advanceTeams.append(teams[2])
        else:
            advanceTeams.append(teams[1])

        #round 2

        scores = []
        teams = []
        for index, row in df[0:2].iterrows():
            teams.append(index)
            preDraftCap = predictData.loc[predictData['winTeam'] == row['team']]['preDraftCapital']
            preDraftCap = preDraftCap.item()
            scores.append(normDist(preDraftCap))
        for index, row in df[advanceTeams[0]:advanceTeams[0]+1].iterrows():
            teams.append(index)
            preDraftCap = predictData.loc[predictData['winTeam'] == row['team']]['preDraftCapital']
            preDraftCap = preDraftCap.item()
            scores.append(normDist(preDraftCap))
        for index, row in df[advanceTeams[1]:advanceTeams[1]+1].iterrows():
            teams.append(index)
            preDraftCap = predictData.loc[predictData['winTeam'] == row['team']]['preDraftCapital']
            preDraftCap = preDraftCap.item()
            scores.append(normDist(preDraftCap))

        
        if scores[3] > scores[0]:
            advanceTeams.append(teams[3])
        else:
            advanceTeams.append(teams[0])
            
        if scores[2] > scores[1]:
            advanceTeams.append(teams[2])
        else:
            advanceTeams.append(teams[1])

        #champ
        scores = []
        teams = []
        for index, row in df[advanceTeams[0]:advanceTeams[0]+1].iterrows():
            teams.append(index)
            preDraftCap = predictData.loc[predictData['winTeam'] == row['team']]['preDraftCapital']
            preDraftCap = preDraftCap.item()
            scores.append(normDist(preDraftCap))
        for index, row in df[advanceTeams[1]:advanceTeams[1]+1].iterrows():
            teams.append(index)
            preDraftCap = predictData.loc[predictData['winTeam'] == row['team']]['preDraftCapital']
            preDraftCap = preDraftCap.item()
            scores.append(normDist(preDraftCap))

        if scores[0] > scores[1]:
            champ = teams[0]
        else:
            champ = teams[1]

        for index, row in df.iterrows():
            if index == champ:
                summaryData[row['team']]['champ'].append(1)
            else:
                summaryData[row['team']]['champ'].append(0)
            

        

        
            

    for index, row in predictData.iterrows():
        wins = np.mean(summaryData[row['winTeam']]['wins'])
        losses = np.mean(summaryData[row['winTeam']]['losses'])
        ties = np.mean(summaryData[row['winTeam']]['ties'])
        points = np.mean(summaryData[row['winTeam']]['points'])
        playoffs = np.mean(summaryData[row['winTeam']]['playoffs'])
        highpoints = np.mean(summaryData[row['winTeam']]['highpoints'])
        lowpoints = np.mean(summaryData[row['winTeam']]['lowpoints'])
        champ = np.mean(summaryData[row['winTeam']]['champ'])

        print(row['winTeam'], wins, losses, ties, points,playoffs, highpoints, lowpoints,champ)


        sql = """insert into analysis.standings
            (standWeek, standTeam, exPointAverage, exWins, playoffsOdds, champOdds, highpoints, lowpoints)
            values (%s)

            on duplicate key update
            exPointAverage = values(exPointAverage),
            exWins = values(exWins),
            playoffsOdds = values(playoffsOdds),
            champOdds = values(champOdds),
            highpoints = values(highpoints),
            lowpoints = values(lowpoints);"""

        sqlString = (str(0) + "," +
                     "'" + row['winTeam'] + "'," +
                     str(points) + "," +
                     str(wins) + "," +
                     str(playoffs) + "," +
                     str(champ) + "," +
                     str(highpoints) + "," +
                     str(lowpoints))

        c.execute(sql % sqlString)

        conn.commit()
                     

        



        




    
    conn.close()
