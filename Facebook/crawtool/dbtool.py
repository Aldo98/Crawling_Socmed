from psycopg2 import pool
import json

with open("config/database.json", "r") as f:
    conf_db = json.load(f)
Hostname = conf_db["postgre"][0]["Hostname"]
Port = conf_db["postgre"][0]["Port"]
DBname = conf_db["postgre"][0]["DBname"]
Username = conf_db["postgre"][0]["Username"]
Password = conf_db["postgre"][0]["Password"]

# Connection Pool disesuaikan dengan target user & kemampuan server
pconnection = pool.ThreadedConnectionPool(
    1, 2, host=Hostname, database=DBname, user=Username, password=Password, port=Port
)

# Function untuk koneksi ke DB
def get_db_conn():
    connection = pconnection.getconn()
    if (connection):
        return connection
        # cursor = connection.cursor()
        # return cursor
    else:
        htg = 0
        while(htg<3):
            print("Error at DB connection... connecting again..")
            get_db_conn()
            htg += 1