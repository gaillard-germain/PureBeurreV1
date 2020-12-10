#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# dbconfig.py
# Author: Germain GAILLARD <gaillard.germain@gmail.com>
# Version: 0.1
# License: GNU GPL

from configparser import ConfigParser
from mysql.connector import MySQLConnection, Error


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

def insert_products(products):
    """ Insert products rows into Products table """

    query = 'INSERT IGNORE INTO Products(name, brand, tags, \
             pnns_group_id, ingredients, additives, allergens, labels, \
             stores, link, compared_to) \
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    db_config = read_db_config()

    try:
        print('Connecting to {} database...'.format(db_config['database']))
        conx = MySQLConnection(**db_config)
        cursor = conx.cursor()

        print('Inserting datas...')

        cursor.executemany(query, products)
        conx.commit()
        cursor.close()
        conx.close()

        print('Connection closed.')

    except Error as error:
        print(error)
