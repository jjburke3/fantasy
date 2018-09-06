
import sys
sys.path.insert(0,'..')
sys.path.insert(0,'..\..')




from DOConn import connection
from DOsshTunnel import DOConnect
from references import errorSQL


week = 1
year = 2018


with DOConnect() as tunnel:
    c, conn = connection(tunnel)





    conn.close()
