#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# dbcreate.py
# Author: Germain GAILLARD <gaillard.germain@gmail.com>
# Version: 0.1
# License: GNU GPL

from mysql.connector import MySQLConnection, Error, errorcode
from dbtools import Dbtools
from dbfeed import Dbfeed
from tables import tables, query

class Dbcreate:
    def __init__(self):
        self.conx = None
        self.cursor = None
        self.tables = tables
        self.query = query

    def create_database(self):
        """ Create database """

        db_config = Dbtools.read_db_config()
        db_name = db_config['database']

        conx = MySQLConnection(user=db_config['user'],
                               password=db_config['password'])

        print('Connecting to MySQL...')

        cursor = conx.cursor()

        try:
            cursor.execute("DROP DATABASE IF EXISTS {}".format(db_name))
            cursor.execute("CREATE DATABASE {} \
                            DEFAULT CHARACTER SET 'utf8'".format(db_name))
            print('Creating database {}...'.format(db_name))

            conx.database = db_name

        except Error as error:
            print(error)
            exit(1)

        finally:
            self.cursor = cursor
            self.conx = conx

    def create_tables(self):
        for table_name in self.tables:
            table_description = self.tables[table_name]
            try:
                print("Creating table {}: ".format(table_name))
                self.cursor.execute(table_description)

            except Error as error:
                print(error)

            else:
                print("OK")

        try:
            print("Filling table PnnsGroups: ")
            self.cursor.execute(self.query)
            self.conx.commit()

        except Error as error:
            print(error)

        else:
            print("OK")

    def insert_products(self, products):
        """ Insert products rows into Products table """

        query = 'INSERT IGNORE INTO Products(name, brand, tags, \
                 pnns_group_id, ingredients, additives, allergens, nutriscore, \
                 labels, stores, link, compared_to) \
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

        try:
            self.cursor.executemany(query, products)
            self.conx.commit()
            print('Inserting datas...')

        except Error as error:
            print(error)

    def create(self):
        self.create_database()
        self.create_tables()
        products = Dbfeed.feed()
        self.insert_products(products)
        self.cursor.close()
        self.conx.close()
        print('Connexion closed.')


if __name__ == "__main__":
    Dbcreate().create()
