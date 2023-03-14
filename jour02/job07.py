import mysql.connector
from config import pwd

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = pwd,
    database = "LaPlateforme"
)

cursor = db.cursor()

cursor.execute("SELECT nom FROM employes WHERE salaire > 3000.0;")

result = cursor.fetchall()

for x in result:
    print(x[0])
print()

db.close()


class Employe:
    def __init__(self):
        self.log = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = pwd,
            database = "LaPlateforme"
        )
        self.cursor = self.log.cursor()
    
    def del_employe(self, nom_employe):
        query = "DELETE FROM employes WHERE nom = %s"
        values = (nom_employe,)
        self.cursor.execute(query, values)
        self.log.commit()
        print("Employé supprimé avec succès !\n")
    
    def add_employe(self, nom, prenom, salaire, poste):
        self.cursor.execute("INSERT INTO employes (nom, prenom, salaire, id_service) VALUES (%s, %s, %s, %s);", (nom, prenom, salaire, poste))
        print(self.cursor.rowcount, "employé ajouté.\n")

    def upd_employe(self, nom, nouveau_salaire):
        request = "UPDATE employes SET salaire = %s WHERE nom = %s"
        values = (nouveau_salaire, nom)
        self.cursor.execute(request, values)
        self.log.commit()

    def ls_employe(self):
        self.cursor.execute("SELECT * FROM employes;")
        result = self.cursor.fetchall()
        print("Liste des employés : ")
        for x in result:
            print(x)
        print("\n")

    def exit(self):
        self.cursor.close()
        self.log.close()
        print("Connexion à la base de données fermée.")

employe = Employe()

employe.add_employe("Zidane", "Zinedine", 4000.00, 2)
employe.ls_employe()

employe.upd_employe("Zidane", 4500.00)
employe.ls_employe()

print('It was all a dream...')
employe.del_employe("Zidane")
employe.ls_employe()

employe.exit()