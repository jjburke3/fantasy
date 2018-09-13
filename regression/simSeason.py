import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import time

plt.rc("font", size=14)
sns.set(style="white")
sns.set(style="whitegrid", color_codes=True)

import sys
sys.path.insert(0,'..')

from DOConn import connection
from DOsshTunnel import DOConnect



with DOConnect() as tunnel:
    c, conn = connection(tunnel)
    weekRun = 13
         
    data = pd.read_sql("""select avg(a.winPoints)
 as donePoints, 
 avg(ifnull(preDraftCapital,(select avg(preDraftCapital) from analysis.preDraftCapital))) as preDraftCapital,
 avg(b.winPoints) as predictPoints, lcase(ifnull(a.winTeam,preDraftTeam)) as winTeam, 
 ifnull(a.winSeason,preDraftYear) as winSeason,
 max(a.winWeek) as maxWeek
 from analysis.preDraftCapital

left join (select winSeason, winTeam, avg(winPoints) as winPoints, max(winWeek) as winWeek
from la_liga_data.wins

where winWeek <= (select max(winWeek) from la_liga_data.wins where winSeason = 2018 and winWeek <= %d)
group by 1,2) a on a.winSeason = preDraftYear and a.winTeam = preDraftTeam
left join la_liga_data.wins b on  ifnull(a.winSeason,preDraftYear) = b.winSeason and b.winWeek > ifnull(a.winWeek,0) and ifnull(a.winTeam,preDraftTeam) = b.winTeam
	and b.winWeek <= 13
group by winTeam, winSeason""" % weekRun, con=conn)

    matchups = pd.read_sql("""select matchYear, lcase(matchTeam) as matchTeam,
    group_concat(lcase(matchOpp) order by matchWeek asc) as matchOpp from la_liga_data.matchups
    group by 1,2;""", con=conn)

    standings = pd.read_sql("""select lcase(winTeam) as winTeam, ifnull(count(distinct(winWeek)),0) as weekNumber,
            sum(winWin) as win,
            sum(winLoss) as loss,
            sum(winTie) as ties,
            sum(winPoints) as points
            from la_liga_data.wins
            where winSeason = 2018 and winWeek <= %d
            group by 1""" % weekRun, con=conn)

    pointTotals = pd.read_sql("""select winPoints from la_liga_data.wins where winWeek < 13""",
                              con=conn)

    
    pointAverages = pd.read_sql("""select winSeason, winTeam, avg(winPoints) as avgPoints
            from la_liga_data.wins where winWeek < 13 group by 1,2""",
                              con=conn)
    data2 = data.loc[data['winSeason'] <= 2017]

    pointsMean = np.mean(pointTotals['winPoints'])
    pointsSd = np.std(pointTotals['winPoints'])

    randseasonMean = np.mean(pointAverages['avgPoints'])
    randseasonSd = np.std(pointAverages['avgPoints'])
    if weekRun == 0:
        weekStart = weekRun
    else:
        weekStart = standings.iloc[0]['weekNumber'].item()
    models = ['coin','draft','points','all']

    def randModel(preDraftCap,pointsAvg):
        result = (np.random.normal(randseasonMean,
                                           randseasonSd,
                                           1))

        return result
    
    def draftModel(preDraftCap,pointsAvg):
        result = (
                    np.random.normal(coefs['const'],
                                      se['const'],
                                      1)+
                    (np.random.normal(coefs['preDraftCapital'],
                                            se['preDraftCapital'],
                                            1))*preDraftCap
                )
        return result
    
    def pointsModel(preDraftCap,pointsAvg):
        result = (
                    np.random.normal(coefs['const'],
                                      se['const'],
                                      1)+
                    (np.random.normal(coefs['donePoints'],
                                            se['donePoints'],
                                            1))*pointsAvg
                )
        return result
    
    def allModel(preDraftCap,pointsAvg):
        result = (
                    np.random.normal(coefs['const'],
                                      se['const'],
                                      1)+
                    (np.random.normal(coefs['preDraftCapital'],
                                            se['preDraftCapital'],
                                            1))*preDraftCap+
                    (np.random.normal(coefs['donePoints'],
                                            se['donePoints'],
                                            1))*pointsAvg
                )
        return result

    def weeklyResults(seasonMean2,n):
        result = (np.random.normal(seasonMean2,
                                           pointsSd,
                                           n))
        return result

    X2 = data2[['preDraftCapital','donePoints']]
    Y2 = data2['predictPoints']
    X2 = sm.add_constant(X2)


    predictData = data.loc[data['winSeason'] == 2018]



    for model in models:
        if model == 'coin' or (model == 'points' and weekRun == 0):
            usedModel = randModel
            reg = sm.OLS(Y2,X2[['preDraftCapital','const']]).fit()
        elif model == 'draft' or (model == 'all' and weekRun == 0):
            usedModel = draftModel
            reg = sm.OLS(Y2,X2[['preDraftCapital','const']]).fit()
        elif model == 'points':
            usedModel = pointsModel
            reg = sm.OLS(Y2,X2[['donePoints','const']]).fit()
        elif model == 'all':
            usedModel = allModel
            reg = sm.OLS(Y2,X2).fit()

        #print(reg.summary())
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

        
        coefs = reg.params
        se = reg.bse

        print('start sim:', model)
        #for j in range(1,1001):
        
        start = time.time()
        for j in range(0,10000):
            teamDict = {}
            
            for index, row in predictData.iterrows():
                teamDict[row['winTeam']] = {}

                teamDict[row['winTeam']]['pointTotals'] = []

                teamDict[row['winTeam']]['matchup'] = []

                teamDict[row['winTeam']]['oppPoints'] = []

                teamDict[row['winTeam']]['wins'] = []

                teamDict[row['winTeam']]['losses'] = []

                teamDict[row['winTeam']]['ties'] = []
                
                teamDict[row['winTeam']]['seasonMean'] = usedModel(row['preDraftCapital'],row['donePoints'])
            
            for key, value in teamDict.items():
                value['pointTotals'] = weeklyResults(value['seasonMean'],13-weekStart).tolist()
                value['matchup'] = matchups.loc[matchups['matchTeam']==key]['matchOpp'].item().split(',')[weekStart:]
                
            for key,value in teamDict.items():
                for i, matchup in enumerate(value['matchup']):
                    value['oppPoints'].append(teamDict[matchup]['pointTotals'][i])
                    value['wins'].append(value['pointTotals'][i] > value['oppPoints'][i])
                    value['losses'].append(value['pointTotals'][i] < value['oppPoints'][i])
                    value['ties'].append(value['pointTotals'][i] == value['oppPoints'][i])
            if weekRun > 0:
                for key,value in teamDict.items():
                    value['pointTotals'].append(standings.loc[standings['winTeam'] == key]['points'].item())
                    value['wins'].append(standings.loc[standings['winTeam'] == key]['win'].item())
                    value['losses'].append(standings.loc[standings['winTeam'] == key]['loss'].item())
                    value['ties'].append(standings.loc[standings['winTeam'] == key]['ties'].item())


                
            
            teams = []
            winArray = []
            lossArray = []
            tieArray = []
            pointArray = []
            for key, value in teamDict.items():
                wins = sum(value['wins'])
                losses = sum(value['losses'])
                ties = sum(value['ties'])
                points = sum(value['pointTotals'])

                teams.append(key)
                winArray.append(wins)
                lossArray.append(losses)
                tieArray.append(ties)
                pointArray.append(points)
                summaryData[key]['wins'].append(wins)
                summaryData[key]['losses'].append(losses)
                summaryData[key]['ties'].append(ties)
                summaryData[key]['points'].append(points)



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
                seasonMean = teamDict[row['team']]['seasonMean']
                scores.append(weeklyResults(seasonMean,1))
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
                seasonMean = teamDict[row['team']]['seasonMean']
                scores.append(weeklyResults(seasonMean,1))
            for index, row in df[advanceTeams[0]:advanceTeams[0]+1].iterrows():
                teams.append(index)
                seasonMean = teamDict[row['team']]['seasonMean']
                scores.append(weeklyResults(seasonMean,1))
            for index, row in df[advanceTeams[1]:advanceTeams[1]+1].iterrows():
                teams.append(index)
                seasonMean = teamDict[row['team']]['seasonMean']
                scores.append(weeklyResults(seasonMean,1))

            
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
                seasonMean = teamDict[row['team']]['seasonMean']
                scores.append(weeklyResults(seasonMean,1))
            for index, row in df[advanceTeams[1]:advanceTeams[1]+1].iterrows():
                teams.append(index)
                seasonMean = teamDict[row['team']]['seasonMean']
                scores.append(weeklyResults(seasonMean,1))

            if scores[0] > scores[1]:
                champ = teams[0]
            else:
                champ = teams[1]

            for index, row in df.iterrows():
                if index == champ:
                    summaryData[row['team']]['champ'].append(1)
                else:
                    summaryData[row['team']]['champ'].append(0)
                

            
        print(j, time.time()-start)
            

            
                

        for index, row in predictData.iterrows():
            if weekStart > 0:
                standTeam = standings.loc[standings['winTeam'] == row['winTeam']]
                currentWins = standTeam['win'].item()
                currentLosses = standTeam['loss'].item()
                currentTies = standTeam['ties'].item()
                currentPoints = standTeam['points'].item()
            else:
                currentWins = 0
                currentLosses = 0
                currentTies = 0
                currentPoints = 0
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
                (standWeek, standType, standTeam, wins, losses, tie, pointsScored, exPointAverage,
                exWins, playoffsOdds, champOdds, highpoints, lowpoints)
                values (%s)

                on duplicate key update
                wins = values(wins),
                losses = values(losses),
                tie = values(tie),
                pointsScored = values(pointsScored),
                exPointAverage = values(exPointAverage),
                exWins = values(exWins),
                playoffsOdds = values(playoffsOdds),
                champOdds = values(champOdds),
                highpoints = values(highpoints),
                lowpoints = values(lowpoints);"""

            sqlString = (str(weekStart) + "," +
                         "'" + model + "'," +
                         "'" + row['winTeam'] + "'," +
                         str(currentWins) + "," +
                         str(currentLosses) + "," +
                         str(currentTies) + "," +
                         str(currentPoints) + "," +
                         str(points) + "," +
                         str(wins) + "," +
                         str(playoffs) + "," +
                         str(champ) + "," +
                         str(highpoints) + "," +
                         str(lowpoints))

            c.execute(sql % sqlString)

            conn.commit()
                         

        



        




    
    conn.close()
