import psycopg

TOKEN = '7070307732:AAHECqiy1xYCtWtdf1nRXq_Vu0Zsz6148JM'

GROUP_ID: int = -4198612438
ADMIN: list = []

HOST = "localhost"
DBNAME = "testdb"
USER = "postgres"
PASSWORD = "root"
PORT = 5432

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
