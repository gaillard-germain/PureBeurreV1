#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# dbconfig.py
# Author: Germain GAILLARD <gaillard.germain@gmail.com>
# Version: 0.1
# License: GNU GPL

from configparser import ConfigParser
from mysql.connector import MySQLConnection, Error

class Dbtools:
    @staticmethod
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

    @classmethod
    def connect(cls):
        """ Connect to MySQL database """

        db_config = cls.read_db_config()

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
