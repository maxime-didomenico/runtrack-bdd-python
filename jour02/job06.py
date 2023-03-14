import mysql.connector
from config import pwd

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = pwd,
    database = "LaPlateforme"
)

cursor = db.cursor()

cursor.execute("SELECT capacite FROM salles")

result = cursor.fetchall()


a = 0
for x in result:
    a += x[0]
print("La superficie totale des salles de LaPlateforme est de", a, "m².")

db.close()