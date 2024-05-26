import psycopg

TOKEN = ''

GROUP_ID = -1002128903514
ADMIN = [6324087931]

HOST = ""
DBNAME = ""
USER = "postgres"
PASSWORD = "root"
PORT = 

db = psycopg.connect(host=HOST, dbname=DBNAME, user=USER, password=PASSWORD, port=PORT)
db.autocommit = True


def get_workers():
    workers = []
    with db.cursor() as cursor:
        cursor.execute("SELECT id FROM workers")
        for worker in cursor.fetchall():
            workers.append(worker[0])
        return workers


WORKERS = get_workers()
