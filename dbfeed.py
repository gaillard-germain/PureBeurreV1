#!/usr/bin/env python3
#  *  coding: utf 8  *

# dbfeed.py
# Author: Germain GAILLARD <gaillard.germain@gmail.com>
# Version: 0.1
# License: GNU GPL


import requests, json
from dbtools import insert_products


def format_value(dict, key):
    """ Checks if the field exist in the json from openfoodfacts API
        and return a formated value"""

    groups = {'Milk and dairy products' : 1,
            'Fish Meat Eggs' : 2,
            'Cereals and potatoes' : 3,
            'Fruits and vegetables' : 4,
            'Fat and sauces' : 5,
            'Sugary snacks' : 6,
            'Beverages' : 7,
            'Salty snacks' : 8,
            'Composite foods' : 9,
            'unknown' : 10,}
    entry = None

    try:
        entry = dict[key]
        if not entry:
            entry = None
        elif key == 'pnns_groups_1':
            if entry in groups:
                entry = groups[entry]
            else:
                entry = None
        elif isinstance(entry, list):
            entry = ', '.join(entry).replace('en:','')

    except KeyError as error:
        print("product {} doesn't have {} field".format(dict['code'], error))

    return entry

def feed_db():
    """ Insert datas from openfoodfacts API into database """

    print('Querying datas...')
    search = 'https://fr.openfoodfacts.org/cgi/search.pl?search_terms=&\
    tagtype_0=states&tag_contains_0=contains&tag_0=checked&\
    sort_by=unique_scans_n&page_size=1000&json=1'

    all = requests.get(search)
    all = all.json()['products']

    products = []

    for product in all:
        raw = (format_value(product, 'product_name'),
               format_value(product, 'brands'),
               format_value(product, 'categories'),
               format_value(product, 'pnns_groups_1'),
               format_value(product, 'ingredients_text_fr'),
               format_value(product, 'additives_tags'),
               format_value(product, 'allergens_tags'),
               format_value(product, 'labels'),
               format_value(product, 'stores'),
               format_value(product, 'url'))

        products.append(raw)

    insert_products(products)
