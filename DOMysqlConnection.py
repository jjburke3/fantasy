

from security import server_creds
from security import mysqlConn

import pymysql
from sshtunnel import SSHTunnelForwarder

sql_host = mysqlConn['host']
sql_user = mysqlConn['user']
sql_pw = mysqlConn['passwd']
sql_db = mysqlConn['db']

ssh_host = server_creds['host']
ssh_user = server_creds['username']
ssh_pw = server_creds['password']

with SSHTunnelForwarder(
    ssh_host,
    ssh_username=ssh_user,
    ssh_password=ssh_pw,
    remote_bind_address=(sql_host, 3306)) as tunnel:
    conn = pymysql.connect(host=sql_host,
                           user=sql_user,
                           passwd=sql_pw,
                           db=sql_db,
                           port=tunnel.local_bind_port)

    c = conn.cursor()

    c.execute("select * from links")

    for row in c:
        print(row)

    conn.close()
