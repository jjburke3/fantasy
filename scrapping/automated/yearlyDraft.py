
import sys
sys.path.insert(0,'../..')
from datetime import date, datetime, timedelta
import calendar




from DOConn import connection
from DOsshTunnel import DOConnect
from leagueDraft import pullDraftData



year = 2019



with DOConnect() as tunnel:
    c, conn = connection(tunnel)
    try:
        sql = pullDraftData(year)
        c.execute(sql)

        conn.commit()
    except Exception as e:
        print(str(e))



    conn.close()
