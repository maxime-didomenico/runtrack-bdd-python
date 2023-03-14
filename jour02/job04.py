import mysql.connector
from config import pwd

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = pwd,
    database = "LaPlateforme"
)

cursor = db.cursor()

cursor.execute("SELECT nom,capacite FROM salles")

result = cursor.fetchall()

for x in result:
    print(x)

db.close()