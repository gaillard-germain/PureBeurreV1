#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# dbcreate.py
# Author: Germain GAILLARD <gaillard.germain@gmail.com>
# Version: 0.1
# License: GNU GPL

from mysql.connector import MySQLConnection, Error, errorcode
from dbconfig import read_db_config
from dbfeed import feed_database
from tables import tables, query


def create_database(tables, query):
    """ Create database """

    db_config = read_db_config()
    db_name = db_config['database']

    conx = MySQLConnection(user=db_config['user'],
                           password=db_config['password'])

    print('Connecting to MySQL...')

    cursor = conx.cursor()

    try:
        cursor.execute("DROP DATABASE {}".format(db_name))

        try:
            cursor.execute("CREATE DATABASE {} \
                            DEFAULT CHARACTER SET 'utf8'".format(db_name))

        except Error as error:
            print("Failed creating database: {}".format(error))
            exit(1)

        conx.database = db_name

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
                print("{} already exists.".format(table_name))
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

    else:
        print("OK")

    finally:
        cursor.close()
        conx.close()
        print('Connection closed.')


if __name__ == "__main__":
    create_database(tables, query)
    feed_database()
