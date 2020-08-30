import pandas as pd
import numpy as np

import statistics as s

from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing as pp

from sklearn.model_selection import train_test_split


from sklearn.neural_network import MLPRegressor

import math

import sys
sys.path.insert(0,'..')
from DOConn import connection
from DOsshTunnel import DOConnect


class fantasyModel:
    def __init__(self, position, season, week):
        self.season = season
        self.week = week
        self.position = position
        table = self._pullData(position)
        if position == 'QB':
            trailYears = 3
            nodeCount = 40
            dummy_columns = ['chartRank','chartPosition','chartRole','injuryStatus','sameTeam']
            main_columns = ['playerRating','age','experience'
                            ,'speed','acceleration','agility','carrying','throw_power','injury','throw_accuracy','awareness'
                            ,'qb1_Rating','qb1_inj'
                            ,'rb1_rating'
                            #,'rb2_Rating'
                            ,'lt_Rating'
                            ,'lg_Rating'
                            ,'c_Rating'
                            ,'rg_Rating'
                            ,'rt_Rating'
                            ,'wr1_Rating'
                            ,'wr2_Rating'
                            ,'wr3_Rating'
                            ,'te1_Rating'
                            #,'fb1_Rating'
                            ,'dl_rating','lb_Rating','db_Rating']
        elif position == 'RB':
            trailYears = 2
            nodeCount = 22
            dummy_columns = ['chartRank','chartPosition','chartRole','injuryStatus']
            main_columns = ['playerRating','age','experience','sameTeam'
                            ,'thirdDownBack','goalLineBack','pr','kr'
                            ,'speed','acceleration','agility','catch','carrying','bc_vision','injury','route_running'
                            ,'qb1_rating'
                            ,'rb1_rating','rb1_Inj'
                            #,'rb2_Rating','rb2_Inj'
                            #,'rb3_Rating','rb3_Inj'
                            ,'lt_Rating'
                            ,'lg_Rating'
                            ,'c_Rating'
                            ,'rg_Rating'
                            ,'rt_Rating'
                            ,'wr1_Rating','wr2_Rating','wr3_Rating'
                            ,'te1_Rating'
                            ,'fb1_Rating'
                            ,'dl_rating','lb_Rating','db_Rating'
                            ]

        elif position == 'WR':
            trailYears = 2
            nodeCount = 25
            dummy_columns = ['chartRank','chartPosition','chartRole','injuryStatus']
            main_columns = ['sameTeam'
                            ,'pr','kr'
                            ,'playerRating','age','experience'
                            ,'speed','acceleration','agility','catch','carrying','bc_vision','injury','route_running'
                            ,'qb1_rating'#,'qb1_throw_power','qb1_throw_accuracy','qb1_awareness'
                            ,'rb1_rating'
                            #,'rb2_Rating'
                            ,'lt_Rating'
                            ,'lg_Rating'
                            ,'c_Rating'
                            ,'rg_Rating'
                            ,'rt_Rating'
                            ,'wr1_Rating','wr1_Inj'
                            ,'wr2_Rating','wr2_Inj'
                            ,'wr3_Rating','wr3_Inj'
                            ,'wr4_Rating','wr4_Inj'
                            ,'te1_Rating'
                            ,'te2_Rating'
                            #,'fb1_Rating'
                            ,'dl_rating','lb_Rating','db_Rating']

        elif position == 'TE':
            trailYears = 2
            nodeCount = 25
            dummy_columns = ['chartRank','chartPosition','chartRole','injuryStatus']
            main_columns = ['sameTeam'
                            ,'pr','kr'
                            ,'playerRating','age','experience'
                            ,'speed','acceleration','agility','catch','carrying','bc_vision','injury','route_running'
                            ,'qb1_rating','qb1_throw_power','qb1_throw_accuracy','qb1_awareness'
                            ,'rb1_rating'
                            #,'rb2_Rating'
                            ,'lt_Rating'
                            ,'lg_Rating'
                            ,'c_Rating'
                            ,'rg_Rating'
                            ,'rt_Rating'
                            ,'wr1_Rating'
                            ,'wr2_Rating'
                            ,'wr3_Rating'
                            ,'wr4_Rating'
                            ,'te1_Rating','te1_Inj'
                            ,'te2_Rating','te2_Inj'
                            #,'fb1_Rating'
                            ,'dl_rating','lb_Rating','db_Rating']

        elif position == 'DST':
            trailYears = 3
            nodeCount = 15
            dummy_columns = []
            main_columns = ['qb1_rating','qb1_inj'
                            ,'rb1_rating'
                            ,'lt_Rating'
                            ,'lg_Rating'
                            ,'c_Rating'
                            ,'rg_Rating'
                            ,'rt_Rating'
                            ,'wr1_Rating','wr2_Rating','wr3_Rating'
                            ,'te1_Rating'
                            ,'fb1_Rating'
                            ,'de1_rating','de2_rating','dt1_rating','dt2_rating'
                            ,'mlb_rating','olb1_rating','olb2_rating'
                            ,'cb1_rating','cb2_rating','s1_rating','s2_rating'
                            ]
        
        
        

        mainData = table.loc[:,main_columns]

        trainSeries = ((table['playerSeason'] < season) &
                       (table['playerSeason'] >= (season - trailYears)))

        testSeries = table['playerSeason'] == season

        if position != 'DST':
            dummies = pd.get_dummies(table.loc[:,dummy_columns])
            trainData_X = pd.concat([mainData.loc[trainSeries],
                                     dummies.loc[trainSeries]],
                                    axis = 1)
            testData_X = pd.concat([mainData.loc[testSeries],
                                     dummies.loc[testSeries]],
                                    axis = 1)
        else:
            trainData_X = mainData.loc[trainSeries]
            testData_X = mainData.loc[testSeries]
                           

        trainData_Y = table.loc[trainSeries,['fantasyPoints']]

        testData_Y = table.loc[testSeries,['fantasyPoints']]
        testDataSummary = table.loc[testSeries,['playerName','playerId']]

        clf = MLPRegressor(random_state=1,max_iter=10000,hidden_layer_sizes=(nodeCount,nodeCount))

        clf2 = MLPRegressor(random_state=1,max_iter=10000,hidden_layer_sizes=(nodeCount,nodeCount))

        try:
            clf.fit(trainData_X,trainData_Y)
            clf2.fit(trainData_X,(trainData_Y.fantasyPoints-clf.predict(trainData_X))**2)

            prediction = clf.predict(testData_X)

            prediction2 = clf2.predict(testData_X)

            results = pd.DataFrame({'prediction' : prediction,
                                    'predVar' : prediction2,
                                    'Name' : testDataSummary['playerName'].tolist(),
                                    'playerId' : testDataSummary['playerId'].tolist()
                                    
                                    })
                                                
            print(results)
            self._pushData(results)
        except Exception as e:
            print(str(e))

    def _pullData(self, position):
        with DOConnect() as tunnel:
            c, conn = connection(tunnel)
            if position == 'DST':
                query = '''select * from modelData.%sData
                where playerSeason >= 2014''' % position.lower()
            else:
                query = '''select * from modelData.%sData
                where chartPosition is not null and playerRating is not null and age is not null and experience is not null
                and playerSeason >= 2014''' % position.lower()

            table = pd.read_sql(query,con=conn)

            conn.close()

            return table

    def _pushData(self, prediction):
        with DOConnect() as tunnel:
            c, conn = connection(tunnel)
            try:
                c.execute('''delete from modelData.modelResults
                            where modelYear = %d and modelWeek = %d
                            and modelPlayerPosition = '%s' ''' %
                          (self.season,self.week,self.position))
            except Exception as e:
                print(str(e))
            try:
                query = '''insert into modelData.modelResults values '''
                for i, row in prediction.iterrows():
                    query += ("(%d, %d, %d, '%s', '%s', %s, %s, current_timestamp()),"
                              % (self.season, self.week,
                                 row.playerId, row.Name,
                                 self.position,
                                 str(row.prediction), str(row.predVar)))

                query = query[:-1]
            except Exception as e:
                print(str(e))
            try:
                c.execute(query)
            except Exception as e:
                print(str(e))
            conn.commit()

            conn.close()


    
