
import sys
sys.path.insert(0,'../..')
from datetime import date, datetime, timedelta
import calendar




from DOConn import connection
from DOsshTunnel import DOConnect
from leagueResults import pullLeagueData

now = datetime.utcnow() - timedelta(hours=4)


year = 2019
if now.date() <= date(year, 9, 10) and now.date() >= date(year,9,3):
    week = 1
elif now.date() <= date(year, 9, 17):
    week = 2
elif now.date() <= date(year, 9, 24):
    week = 3
elif now.date() <= date(year, 10, 1):
    week = 4
elif now.date() <= date(year, 10, 8):
    week = 5
elif now.date() <= date(year, 10, 15):
    week = 6
elif now.date() <= date(year, 10, 22):
    week = 7
elif now.date() <= date(year, 10, 29):
    week = 8
elif now.date() <= date(year, 11, 5):
    week = 9
elif now.date() <= date(year, 11, 12):
    week = 10
elif now.date() <= date(year, 11, 19):
    week = 11
elif now.date() <= date(year, 11, 26):
    week = 12
elif now.date() <= date(year, 12, 3):
    week = 13
elif now.date() <= date(year, 12, 10):
    week = 14
elif now.date() <= date(year, 12, 17):
    week = 15
elif now.date() <= date(year, 12, 24):
    week = 16
elif now.date() <= date(year, 12,31):
    week = 17
else:
    week = 0
    


with DOConnect() as tunnel:
    c, conn = connection(tunnel)
    try:
        sql = pullLeagueData(year,week)
        try:
            c.execute(sql[0])
        except Exception as e:
            print(str(e))
        conn.commit()
        try:
            c.execute(sql[1])
        except Exception as e:
            print(str(e))
        try:
            c.execute('''update la_liga_data.wins
                    join (
                        select winSeason as oppSeason, winWeek as oppWeek, winTeam as opp, winPoints as oppPoint from la_liga_data.wins
                        where winSeason = %d and winWeek = %d) a on winSeason = oppSeason and winWeek = oppWeek
                        and winOpp = opp
                        set winPointsAgs = oppPoint, 
                        winWin = case when winPoints > oppPoint then 1 else 0 end, 
                        winLoss = case when winPoints < oppPoint then 1 else 0 end, 
                        winTie = case when winPoints = oppPoint then 1 else 0 end''' % (year,week))
        except Exception as e:
            print(str(e))
        conn.commit()
    except Exception as e:
        print(str(e))




    conn.close()
