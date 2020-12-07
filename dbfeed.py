#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# dbfeed.py
# Author: Germain GAILLARD <gaillard.germain@gmail.com>
# Version: 0.1
# License: GNU GPL

import requests, json
from dbtools import insert_products


def check_entry(dict, key):
    """ Checks if the field exist in the json from openfoodfacts API """

    try:
        if not dict[key]:
            return 'NULL'
        else:
            return dict[key]
    except KeyError as error:
        print("product {} doesn't have {} field".format(dict['code'], error))
        return 'NULL'

def join_tags(tags):
    if tags != 'NULL':
        return ', '.join(tags)

def feed_db():
    """ Insert datas from openfoodfacts API into database """

    print('Querying datas...')
    search = 'https://fr.openfoodfacts.org/cgi/search.pl?search_terms=&\
    tagtype_0=states&tag_contains_0=contains&tag_0=checked&\
    sort_by=unique_scans_n&page_size=1000&json=1'

    all = requests.get(search)
    all = all.json()['products']

    products = []

    pnns = {'milk-and-dairy-products' : 1,
            'fish-meat-eggs' : 2,
            'cereals-and-potatoes' : 3,
            'fruits-and-vegetables' : 4,
            'fat-and-sauces' : 5,
            'sugary-snacks' : 6,
            'beverages' : 7,
            'salty-snacks' : 8,
            'composite-foods' : 9,
            'unknown' : 10,
            'null' : 10}

    for product in all:
        raw = (check_entry(product, 'product_name'),
                check_entry(product, 'brands'),
                check_entry(product, 'generic_name_fr'),
                pnns[check_entry(product, 'pnns_groups_1').replace(' ', '-').lower()],
                check_entry(product, 'ingredients_text_fr'),
                join_tags(check_entry(product, 'additives_tags')),
                join_tags(check_entry(product, 'allergens_tags')),
                check_entry(product, 'labels'),
                check_entry(product, 'stores'),
                check_entry(product, 'url'))

        products.append(raw)

    insert_products(products)
