import mysql.connector
import csv
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from config import pwd


class GestionStockGUI:
    
    def __init__(self, master):

        self.gestion_stock = GestionStock()
        self.master = master
        master.title("Gestion de stock")
        
        # Create the frame for the categories section
        self.categories_frame = ttk.LabelFrame(master, text="Catégories")
        self.categories_frame.grid(row=0, column=0, padx=10, pady=10)
        
        # Add category button and entry
        self.add_category_entry = ttk.Entry(self.categories_frame)
        self.add_category_entry.grid(row=0, column=0, padx=5, pady=5)
        self.add_category_button = ttk.Button(self.categories_frame, text="Ajouter", command=lambda: self.add_category(self.add_category_entry.get()))
        self.add_category_button.grid(row=0, column=1, padx=5, pady=5)
        
        # Update category button and entry
        self.update_category_entry = ttk.Entry(self.categories_frame)
        self.update_category_entry.grid(row=1, column=0, padx=5, pady=5)
        self.update_category_button = ttk.Button(self.categories_frame, text="Mettre à jour", command=lambda: self.update_category(self.update_category_entry.get()))
        self.update_category_button.grid(row=1, column=1, padx=5, pady=5)
        
        # Delete category button and entry
        self.delete_category_entry = ttk.Entry(self.categories_frame)
        self.delete_category_entry.grid(row=2, column=0, padx=5, pady=5)
        self.delete_category_button = ttk.Button(self.categories_frame, text="Supprimer", command=lambda: self.delete_category(self.delete_category_entry.get()))
        self.delete_category_button.grid(row=2, column=1, padx=5, pady=5)
        
        # Csv button
        self.add_csv_button = ttk.Button(self.categories_frame, text="Ajouter CSV", command=lambda: self.export_csv())
        self.add_csv_button.grid(row=3, column=1, padx=5, pady=5)

        # Liste des catégories
        self.categories_listbox = tk.Listbox(self.categories_frame)
        self.categories_listbox.grid(row=3, column=0, columnspan=1, padx=5, pady=5)

        # Remplir la liste des catégories
        self.categorie_fill()
        
        # Create the frame for the products section
        self.products_frame = ttk.LabelFrame(master, text="Produits")
        self.products_frame.grid(row=1, column=0, padx=10, pady=10)
        
        # Add product entry fields
        ttk.Label(self.products_frame, text="Nom").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(self.products_frame, text="Prix").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(self.products_frame, text="Quantité").grid(row=2, column=0, padx=5, pady=5)
        ttk.Label(self.products_frame, text="Catégorie").grid(row=3, column=0, padx=5, pady=5)
        ttk.Label(self.products_frame, text="Description").grid(row=4, column=0, padx=5, pady=5)
        
        self.product_name_entry = ttk.Entry(self.products_frame)
        self.product_name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.product_price_entry = ttk.Entry(self.products_frame)
        self.product_price_entry.grid(row=1, column=1, padx=5, pady=5)
        self.product_quantity_entry = ttk.Entry(self.products_frame)
        self.product_quantity_entry.grid(row=2, column=1, padx=5, pady=5)
        self.product_category_combobox = ttk.Combobox(self.products_frame, values=self.gestion_stock.get_categories(), state='readonly')
        self.product_category_combobox.grid(row=3, column=1, padx=5, pady=5)
        self.product_description_entry = ttk.Entry(self.products_frame)
        self.product_description_entry.grid(row=4, column=1, padx=5, pady=5)

        # Add product button
        self.add_product_button = ttk.Button(self.products_frame, text="Ajouter", command=self.add_product)
        self.add_product_button.grid(row=5, column=1, padx=5, pady=5)
        
        # Update product button and combobox
        self.update_product_combobox = ttk.Combobox(self.products_frame, values=self.gestion_stock.get_produits_name(), state='readonly')
        self.update_product_combobox.grid(row=6, column=1, padx=5, pady=5)
        self.update_product_button = ttk.Button(self.products_frame, text="Mettre à jour", command=self.update_product)
        self.update_product_button.grid(row=7, column=1, padx=5, pady=5)
        
        # Delete product button and combobox
        self.delete_product_combobox = ttk.Combobox(self.products_frame, values=self.gestion_stock.get_produits_name(), state='readonly')
        self.delete_product_combobox.grid(row=8, column=1, padx=5, pady=5)
        self.delete_product_button = ttk.Button(self.products_frame, text="Supprimer", command=self.delete_product)
        self.delete_product_button.grid(row=9, column=1, padx=5, pady=5)
        
        # Products treeview
        self.products_treeview = ttk.Treeview(self.products_frame, columns=("id","name", "price", "quantity", "category"), show='headings')
        self.products_treeview.heading("id", text="ID")
        self.products_treeview.heading("name", text="Nom")
        self.products_treeview.heading("price", text="Prix")
        self.products_treeview.heading("quantity", text="Quantité")
        self.products_treeview.heading("category", text="Categorie")
        #self.products_treeview.heading("desc", text="Description")
        self.products_treeview.grid(row=2, column=2, rowspan=10, padx=10, pady=10)

        self.update_produits_list()
    
    def categorie_fill(self):
        self.categories_listbox.delete(0, tk.END)
        categories = self.gestion_stock.get_categories()
        for category in categories:
            self.categories_listbox.insert(tk.END, category[0])

    def add_category(self, str):
        self.gestion_stock.add_categorie(str)
        self.add_category_entry.delete(0, 'end')
        self.categorie_fill()

    def update_category(self, str):
        self.gestion_stock.upd_categorie(str)
        self.update_category_entry.delete(0, 'end')
        self.categorie_fill()

    def delete_category(self, str):
        self.gestion_stock.del_categorie(str)
        self.delete_category_entry.delete(0, 'end')
        self.categorie_fill()

    def add_product(self):
        id = self.gestion_stock.get_categorie_id(self.product_category_combobox.get())
        self.gestion_stock.add_produit(self.product_name_entry.get(), self.product_price_entry.get(), self.product_quantity_entry.get(), id, self.product_description_entry.get())
        self.product_name_entry.delete(0, 'end')
        self.update_produits_list()

    def update_product(self):
        category = self.gestion_stock.get_categorie_id(self.product_category_combobox.get())
        id = self.gestion_stock.get_categorie_id(self.update_product_combobox.get())
        name = self.product_name_entry.get()
        if name[0] == '{':
            name = name.strip('{}')

        self.gestion_stock.upd_produit(id, name, self.product_price_entry.get(), self.product_quantity_entry.get(), category, self.product_description_entry.get())
        self.product_name_entry.delete(0, 'end')
        self.update_produits_list()

    def delete_product(self):
        name = self.delete_product_combobox.get()
        if name[0] == '{':
            name = name.strip('{}')
        id = self.gestion_stock.get_produit_id(name)
        self.gestion_stock.del_produit(id)
        self.delete_product_combobox.delete(0, 'end')
        self.update_produits_list()

    def update_produits_list(self):
        self.products_treeview.delete(*self.products_treeview.get_children())
        all_products = self.gestion_stock.get_produits()
        for produit in all_products:
            self.products_treeview.insert("", "end", values=produit)

    def export_csv(self):
        selected_category = self.categories_listbox.curselection()
        if selected_category:
            category_name = self.categories_listbox.get(selected_category[0])
            self.gestion_stock.csv(category_name)



class GestionStock:

    def __init__(self):

        self.log = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = pwd,
            database = "boutique"
        )
        self.cursor = self.log.cursor()

    def get_categories(self):
        
        request = "SELECT * FROM categorie"
        self.cursor.execute(request)
        result = self.cursor.fetchall()
        categories = []
        for row in result:
            category = [row[1]]
            categories.append(category)
        return categories


    def add_categorie(self, nom):

        request = "INSERT INTO categorie (nom) VALUES (%s)"
        values = (nom,)
        self.cursor.execute(request, values)
        self.log.commit()
        print(f"Catégorie {nom} ajoutée.")


    def upd_categorie(self, nom):
        id_categorie = self.get_categorie_id(nom)
        request = "UPDATE categorie SET nom = %s WHERE id = %s"
        values = (nom, id_categorie)
        self.cursor.execute(request, values)
        self.log.commit()
        print(f"Catégorie {nom} mise à jour.")


    def get_categorie_id(self, nom):
        request = "SELECT id FROM categorie WHERE nom = %s"
        values = (nom,)
        self.cursor.execute(request, values)
        result = self.cursor.fetchone()
        return result[0]


    def del_categorie(self, categorie):
        id_categorie = self.get_categorie_id(categorie) 
        request = "DELETE FROM categorie WHERE id = %s"
        values = (id_categorie,)
        self.cursor.execute(request, values)
        self.log.commit()
        print(f"Catégorie {id_categorie} supprimée.")


    def add_produit(self, nom, prix, quantite, id_categorie, desc):

        request = "INSERT INTO produit (nom, prix, quantite, id_categorie, description) VALUES (%s, %s, %s, %s, %s)"
        values = (nom, prix, quantite, id_categorie, desc)
        self.cursor.execute(request, values)
        self.log.commit()
        print(f"Produit {nom} ajouté.")


    def upd_produit(self, id_produit, nom, prix, quantite, id_categorie, desc):

        request = "UPDATE produit SET nom = %s, prix = %s, quantite = %s, id_categorie = %s, description = %s WHERE id = %s"
        values = (nom, prix, quantite, id_categorie, id_produit, desc)
        self.cursor.execute(request, values)
        self.log.commit()
        print(f"Produit {nom} mis à jour.")


    def del_produit(self, id_produit):

        request = "DELETE FROM produit WHERE id = %s"
        values = (id_produit,)
        self.cursor.execute(request, values)
        self.log.commit()
        print(f"Produit {id_produit} supprimé.")


    def afficher_categories(self):

        request = "SELECT * FROM categorie"
        self.cursor.execute(request)
        result = self.cursor.fetchall()
        if result:
            return result
        
    
    def get_produit_id(self, name):
        request = "SELECT id FROM produit WHERE nom = %s"
        values = (name,)
        self.cursor.execute(request, values)
        result = self.cursor.fetchone()
        return result[0]


    def get_produits_name(self):

        request = "SELECT * FROM produit"
        self.cursor.execute(request)
        result = self.cursor.fetchall()
        list = []
        for row in result:
            produit = [row[1]]
            list.append(produit)
        return list
    
    def get_produits(self):
            
        request = "SELECT * FROM produit"
        self.cursor.execute(request)
        result = self.cursor.fetchall()
        return result


    def afficher_produits_par_categorie(self, id_categorie):

        request = "SELECT * FROM produit WHERE id_categorie = %s"
        values = (id_categorie,)
        self.cursor.execute(request, values)
        result = self.cursor.fetchall()
        if result:
            return result


    def recherche(self, nom):

        request = "SELECT * FROM produit WHERE nom LIKE %s"
        values = (f"%{nom}%",)
        self.cursor.execute(request, values)
        result = self.cursor.fetchall()
        if result:
            print("Résultat de la recherche :")
            return result
        else:
            print("Aucun résultat trouvé pour cette recherche.")


    def csv(self, nom_categorie):
        request = "SELECT id FROM categorie WHERE nom = %s"
        values = (nom_categorie,)
        self.cursor.execute(request, values)
        id_categorie = self.cursor.fetchone()
        if id_categorie is not None:
            id_categorie = id_categorie[0]
            request = "SELECT * FROM produit WHERE id_categorie = %s"
            values = (id_categorie,)
            self.cursor.execute(request, values)
            result = self.cursor.fetchall()
            with open(f"{nom_categorie}.csv", "w") as f:
                for produit in result:
                    f.write(",".join(str(val) for val in produit) + "\n")
            print(f"Fichier {nom_categorie}.csv créé.")
        else:
            print(f"La catégorie {nom_categorie} n'existe pas dans la base de données.")


    def exit(self):
        self.cursor.close()
        self.log.close()
        print("Connexion à la base de données fermée.")

root = tk.Tk()
app = GestionStockGUI(root)
root.mainloop()