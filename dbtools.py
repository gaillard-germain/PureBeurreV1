#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# dbtools.py
# Author: Germain GAILLARD <gaillard.germain@gmail.com>
# Version: 0.1
# License: GNU GPL


from mysql.connector import MySQLConnection, Error
from configparser import ConfigParser


def create_database(cursor, db_name):
    """ Create database """

    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
    except Error as error:
        print("Failed creating database: {}".format(error))
        exit(1)

def read_db_config(filename='config.ini', section='mysql'):
    """ Read database configuration file and return a dictionary object"""

    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{} not found in {} file'.format(section, filename))
    return db

def connect():
    """ Connect to MySQL database """

    db_config = read_db_config()
    conx = None
    try:
        print('Connecting to {} database...'.format(db_config['database']))
        conx = MySQLConnection(**db_config)

        if conx.is_connected():
            print('Connection established.')
        else:
            print('Connection failed.')

    except Error as error:
        print(error)

    finally:
        if conx is not None and conx.is_connected():
            return conx

def insert_products(products):
    """ Insert multiple rows into a table """

    query = 'INSERT IGNORE INTO Products(name, brand, tags, \
             pnns_group_id, ingredients, additives, allergens, labels, \
             stores, link, compared_to) \
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    try:
        conx = connect()

        cursor = conx.cursor()
        print('Inserting datas...')
        cursor.executemany(query, products)

        conx.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conx.close()
        print('Connection closed.')

def groups_menu():
    query = 'SELECT * FROM PnnsGroups ORDER BY id'
    menu = {}

    try:
        conx = connect()
        cursor = conx.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            menu[str(row[0])] = row[1]

    except Error as error:
        print(error)

    finally:
        cursor.close()
        conx.close()
        print('Connection closed.')
    return menu

def iter_row(cursor, size=10):
    while True:
        rows = cursor.fetchmany(size)
        if not rows:
            break
        for row in rows:
            yield row

def products_menu(id):
    query = "SELECT id, name, brand FROM Products WHERE pnns_group_id = {} \
             AND (additives IS NOT NULL AND labels IS NULL) ORDER BY RAND() \
             LIMIT 10".format(id)
    menu = {}

    try:
        conx = connect()
        cursor = conx.cursor()

        cursor.execute(query)

        for row in iter_row(cursor, 10):
            menu[str(row[0])] = '{} / {}'.format(row[1], row[2])

    except Error as error:
        print(error)

    finally:
        cursor.close()
        conx.close()
        print('Connection closed.')
    return menu

def keyword(id):
    query = "SELECT compared_to FROM Products WHERE id = {}".format(id)
    word = None

    try:
        conx = connect()
        cursor = conx.cursor()
        cursor.execute(query)
        row = cursor.fetchone()

        word = row[0]
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conx.close()
        print('Connection closed.')
    return word

def product_details(keyword):
    query = "SELECT * FROM Products WHERE tags LIKE ('%{}%') \
             AND (additives IS NULL AND labels IS NOT NULL) ORDER BY RAND() \
             LIMIT 1".format(keyword)
    product = {}

    try:
        conx = connect()
        cursor = conx.cursor()
        cursor.execute(query)
        row = cursor.fetchone()

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

    finally:
        cursor.close()
        conx.close()
        print('Connection closed.')

    return product
