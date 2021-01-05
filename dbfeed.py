#!/usr/bin/env python3
#  *  coding: utf 8  *

# dbfeed.py
# Author: Germain GAILLARD <gaillard.germain@gmail.com>
# Version: 0.1
# License: GNU GPL

import requests


class Dbfeed:
    @staticmethod
    def format_value(dict, key):
        """ Checks if the field exist in the json from openfoodfacts API
            and return a formated value"""

        groups = {'Milk and dairy products': 1,
                  'Fish Meat Eggs': 2,
                  'Cereals and potatoes': 3,
                  'Fruits and vegetables': 4,
                  'Fat and sauces': 5,
                  'Sugary snacks': 6,
                  'Beverages': 7,
                  'Salty snacks': 8,
                  'Composite foods': 9,
                  'unknown': 10}
        value = None

        try:
            value = dict[key]
            if not value:
                value = None
            elif key == 'pnns_groups_1':
                if value in groups:
                    value = groups[value]
                else:
                    value = None
            elif isinstance(value, list):
                value = ', '.join(value)

        except KeyError as error:
            print("product {} doesn't have {} field".format(dict['code'],
                                                            error))

        return value

    @classmethod
    def feed(cls):
        """ Returns datas from openfoodfacts API """

        print('Querying datas...')
        search = 'https://fr.openfoodfacts.org/cgi/search.pl?search_terms=&\
        tagtype_0=states&tag_contains_0=contains&tag_0=checked&\
        sort_by=unique_scans_n&page_size=1000&json=1'

        all = requests.get(search)
        all = all.json()['products']

        products = []

        for product in all:
            row = (cls.format_value(product, 'product_name'),
                   cls.format_value(product, 'brands'),
                   cls.format_value(product, 'categories_tags'),
                   cls.format_value(product, 'pnns_groups_1'),
                   cls.format_value(product, 'ingredients_text_fr'),
                   cls.format_value(product, 'additives_tags'),
                   cls.format_value(product, 'allergens_tags'),
                   cls.format_value(product, 'nutrition_grade_fr'),
                   cls.format_value(product, 'labels'),
                   cls.format_value(product, 'stores'),
                   cls.format_value(product, 'url'),
                   cls.format_value(product, 'compared_to_category'))

            products.append(row)

        return products
