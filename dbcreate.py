#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# dbcreate.py
# Author: Germain GAILLARD <gaillard.germain@gmail.com>
# Version: 0.1
# License: GNU GPL

# from __future__ import print_function

import mysql.connector
from mysql.connector import MySQLConnection, Error, errorcode
from dbtools import read_db_config, create_database
from dbfeed import feed_db


tables = {}
tables['PnnsGroups'] = (
    "CREATE TABLE PnnsGroups("
    "  id smallint(5) unsigned NOT NULL AUTO_INCREMENT,"
    "  name varchar(50) NOT NULL UNIQUE,"
    "  PRIMARY KEY (id)"
    ") ENGINE = InnoDB")

tables['Products'] = (
    "CREATE TABLE Products ("
    "  id smallint(5) unsigned NOT NULL AUTO_INCREMENT,"
    "  name varchar(100) NOT NULL UNIQUE,"
    "  brand varchar(100) NOT NULL,"
    "  pnns_group_id smallint(5) unsigned NOT NULL,"
    "  ingredients text DEFAULT NULL,"
    "  additives text DEFAULT NULL,"
    "  allergens text DEFAULT NULL,"
    "  labels text DEFAULT NULL,"
    "  stores text DEFAULT NULL,"
    "  link varchar(100) DEFAULT NULL UNIQUE,"
    "  substitut_id smallint(5) unsigned DEFAULT NULL,"
    "  PRIMARY KEY (id),"
    "  CONSTRAINT fk_substitut_id FOREIGN KEY (substitut_id) "
    "    REFERENCES Products (id),"
    "  CONSTRAINT fk_pnns_group_id FOREIGN KEY (pnns_group_id) "
    "    REFERENCES PnnsGroups (id)"
    ") ENGINE = InnoDB")

query = (
    "INSERT INTO PnnsGroups VALUES (1, 'Lait et produits laitiers'),"
    "(2, 'Viandes Poissons Oeufs'), (3, 'Féculents'), (4, 'Fruits et légumes'),"
    "(5, 'Corps gras'), (6, 'Sucre et produits sucrés'), (7, 'Boissons'),"
    "(8, 'Produits salés'), (9, 'Plats préparés'), (10, 'Autre');")

db_config = read_db_config()
db_name = db_config['database']

conx = MySQLConnection(user=db_config['user'], password=db_config['password'])
print('Connecting to MySQL...')
cursor = conx.cursor()

try:
    cursor.execute("USE {}".format(db_name))
except Error as error:
    print("Database {} does not exists.".format(db_name))
    if error.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor, db_name)
        print("Database {} created successfully.".format(db_name))
        conx.database = db_name
    else:
        print(error)
        exit(1)

for table_name in tables:
    table_description = tables[table_name]
    try:
        print("Creating table {}: ".format(table_name))
        cursor.execute(table_description)
    except Error as error:
        if error.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(error.msg)
    else:
        print("OK")

try:
    print("Filling table PnnsGroups: ")
    cursor.execute(query)

    conx.commit()

except Error as error:
    print(error.msg)

finally:
    cursor.close()
    conx.close()
    print('Connection closed.')

feed_db()
