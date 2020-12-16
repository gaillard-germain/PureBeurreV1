#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# dbtools.py
# Author: Germain GAILLARD <gaillard.germain@gmail.com>
# Version: 0.1
# License: GNU GPL


from mysql.connector import MySQLConnection, Error, errorcode
from dbtools import read_db_config
from collections import OrderedDict


class Busboy:
    def __init__(self):
        self.conx = None
        self.cursor = None
        self.connect()

    def connect(self):
        """ Connect to MySQL database """

        db_config = read_db_config()

        try:
            print('Connecting to {} database...'.format(db_config['database']))
            self.conx = MySQLConnection(**db_config)

            if self.conx.is_connected():
                print('Connection established.')
            else:
                print('Connection failed.')

        except Error as error:
            print(error)

        finally:
            if self.conx is not None and self.conx.is_connected():
                self.cursor = self.conx.cursor()

    def dismiss(self):
        """ Close connexion to MySQL database """

        self.cursor.close()
        self.conx.close()
        print('Connection closed.')

    def groups_menu(self):
        """ Returns a dict of alimentary groups with their id """

        query = 'SELECT * FROM PnnsGroups ORDER BY id'
        menu = OrderedDict()

        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            for row in rows:
                menu[str(row[0])] = row[1]

        except Error as error:
            print(error)

        return menu

    def products_menu(self, id):
        """ Returns a dict of a random top ten 'bads' products with their id """

        query = "SELECT id, name, brand \
                 FROM Products WHERE pnns_group_id = {} \
                 AND (nutriscore IN ('d', 'e') \
                 OR nutriscore IS NULL) \
                 ORDER BY RAND() LIMIT 10".format(id)
        menu = {}

        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            for row in rows:
                menu[str(row[0])] = '{} de {}'.format(row[1], row[2])

        except Error as error:
            print(error)

        return menu

    def keyword(self, id):
        """ Returns the keyword of the product """

        query = "SELECT compared_to FROM Products WHERE id = {}".format(id)
        keyword = None

        try:
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            keyword = row[0]

        except Error as error:
            print(error)

        return keyword

    def substitut_id(self, id):
        """ Returns a random 'good' product's id which tags matched keyword """

        keyword = self.keyword(id)
        query = "SELECT id FROM Products WHERE tags LIKE ('%{}%') \
                 AND (nutriscore IN ('a', 'b', 'c') OR additives IS NULL) \
                 AND id <> {} \
                 ORDER BY RAND() LIMIT 1".format(keyword, id)
        id = None

        try:
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            if row:
                id = row[0]

        except Error as error:
            print(error)

        return id

    def product_detail(self, id):
        """ Returns a dict {field : value} of the product """

        query = "SELECT * FROM Products WHERE id = {}".format(id)
        product = {}

        try:
            self.cursor.execute(query)
            row = self.cursor.fetchone()

            if row:
                product['Nom'] = row[1]
                product['Marque'] = row[2]
                product['Ingrédients'] = row[5]
                product['Additifs'] = row[6]
                product['Allergènes'] = row[7]
                product['Nutriscore'] = row[8]
                product['Labels'] = row[9]
                product['Distribué par'] = row[10]
                product['Lien OpenFoodFacts'] = row[11]

        except Error as error:
            if error.errno == errorcode.ER_BAD_FIELD_ERROR:
                print("\nAucun produits correspondant\n")
            else:
                print(error)

        return product

    def save(self, ids):
        """ Saves comparison in database (product's id) """

        query = "INSERT INTO Substituts(unliked_id, liked_id) \
                 VALUES(%s, %s)"

        try:
            self.cursor.execute(query, ids)
            self.conx.commit()

        except Error as error:
            print(error)

    def substituts_saved(self):
        """ Returns a dict of unliked products and a dict of liked products """

        query = "SELECT unliked_id, Prod1.name, Prod1.brand,\
                 liked_id, Prod2.name, Prod2.brand \
                 FROM Substituts INNER JOIN Products AS Prod1 \
                 ON Substituts.unliked_id = Prod1.id \
                 INNER JOIN Products AS Prod2 \
                 ON Substituts.liked_id = Prod2.id"
        unliked = OrderedDict()
        liked = OrderedDict()

        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            for row in rows:
                unliked[str(row[0])] = "{} de {}".format(row[1], row[2])
                liked[str(row[3])] = "{} de {}".format(row[4], row[5])

        except Error as error:
            print(error)

        return unliked, liked
