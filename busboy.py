#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# dbtools.py
# Author: Germain GAILLARD <gaillard.germain@gmail.com>
# Version: 0.1
# License: GNU GPL


from mysql.connector import MySQLConnection, Error
from dbconfig import read_db_config


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
        self.cursor.close()
        self.conx.close()
        print('Connection closed.')

    def insert_products(self, products):
        """ Insert multiple rows into a table """

        query = 'INSERT IGNORE INTO Products(name, brand, tags, \
                 pnns_group_id, ingredients, additives, allergens, labels, \
                 stores, link, compared_to) \
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        try:
            print('Inserting datas...')
            self.cursor.executemany(query, products)
            self.conx.commit()

        except Error as error:
            print(error)

    def groups_menu(self):
        query = 'SELECT * FROM PnnsGroups ORDER BY id'
        menu = {}

        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            for row in rows:
                menu[str(row[0])] = row[1]

        except Error as error:
            print(error)

        return menu

    def products_menu(self, id):
        query = "SELECT id, name, brand FROM Products WHERE pnns_group_id = {} \
                 AND (additives IS NOT NULL AND labels IS NULL) ORDER BY RAND() \
                 LIMIT 10".format(id)
        menu = {}

        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            for row in rows:
                menu[str(row[0])] = '{} / {}'.format(row[1], row[2])

        except Error as error:
            print(error)

        return menu

    def keyword(self, id):
        query = "SELECT compared_to FROM Products WHERE id = {}".format(id)
        keyword = None

        try:
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            keyword = row[0]

        except Error as error:
            print(error)

        return keyword

    def product_details(self, keyword):
        query = "SELECT * FROM Products WHERE tags LIKE ('%{}%') \
                 AND (additives IS NULL AND labels IS NOT NULL) ORDER BY RAND() \
                 LIMIT 1".format(keyword)
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
                product['Labels'] = row[8]
                product['Distribué par'] = row[9]
                product['Lien OpenFoodFacts'] = row[10]
            else:
                product['résultat'] = 'Aucun substitut trouvé'

        except Error as error:
            print(error)

        return product
