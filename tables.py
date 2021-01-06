#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# dbcreate.py
# Author: Germain GAILLARD <gaillard.germain@gmail.com>
# Version: 0.1
# License: GNU GPL

tables = {}
tables['Categories'] = (
    "CREATE TABLE Categories("
    "  id smallint(5) unsigned NOT NULL AUTO_INCREMENT,"
    "  name varchar(50) NOT NULL UNIQUE,"
    "  PRIMARY KEY (id)"
    ") ENGINE = InnoDB")

tables['Products'] = (
    "CREATE TABLE Products ("
    "  id smallint(5) unsigned NOT NULL AUTO_INCREMENT,"
    "  name varchar(100) NOT NULL UNIQUE,"
    "  brand varchar(100) DEFAULT NULL,"
    "  tags varchar(200) NOT NULL,"
    "  categories_id smallint(5) unsigned NOT NULL,"
    "  ingredients text DEFAULT NULL,"
    "  additives text DEFAULT NULL,"
    "  allergens text DEFAULT NULL,"
    "  nutriscore varchar(1) DEFAULT NULL,"
    "  labels text DEFAULT NULL,"
    "  stores text DEFAULT NULL,"
    "  link varchar(100) DEFAULT NULL UNIQUE,"
    "  compared_to varchar(50) DEFAULT NULL,"
    "  PRIMARY KEY (id),"
    "  INDEX (tags),"
    "  CONSTRAINT fk_categories_id FOREIGN KEY (categories_id)"
    "    REFERENCES Categories (id)"
    ") ENGINE = InnoDB")

tables['Favorites'] = (
    "CREATE TABLE Favorites ("
    "  id smallint(5) unsigned NOT NULL AUTO_INCREMENT,"
    "  unliked_id smallint(5) unsigned NOT NULL,"
    "  liked_id smallint(5) unsigned NOT NULL,"
    "  PRIMARY KEY (id),"
    "  CONSTRAINT fk_unliked_id FOREIGN KEY (unliked_id)"
    "    REFERENCES Products (id),"
    "  CONSTRAINT fk_liked_id FOREIGN KEY (liked_id)"
    "    REFERENCES Products (id)"
    ") ENGINE = InnoDB")

query = (
    "INSERT INTO Categories VALUES (1, 'Lait et produits laitiers'),"
    "(2, 'Viandes Poissons Oeufs'), (3, 'Féculents'),"
    "(4, 'Fruits et légumes'), (5, 'Corps gras'),"
    "(6, 'Produits sucrés'), (7, 'Boissons'),"
    "(8, 'Produits salés'), (9, 'Plats préparés'), (10, 'Autre')")
