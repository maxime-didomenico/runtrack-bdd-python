import mysql.connector
from config import pwd

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = pwd,
    database = "LaPlateforme"
)

cursor = db.cursor()

cursor.execute("SELECT * FROM etudiants")

result = cursor.fetchall()

for x in result:
    print(x)

db.close()