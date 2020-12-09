#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ui.py
# Author: Germain GAILLARD <gaillard.germain@gmail.com>
# Version: 0.1
# License: GNU GPL

import sys
from busboy import Busboy


def show_product(**product):
    print('\n---Substitut---\n|')
    for key, value in product.items():
        if value and ', ' in value:
            new = value.replace(', ', '\n|\t  -')
            print("|\t{} :\n|\t  -{}".format(key, new))
        else:
            print("|\t{} : {}".format(key, value))
    print('|\n------------\n')

def menu_input(menu, title):
    """ Display menu with user's entry """

    menu['0'] = 'Quitter'
    print('\n{}'.format(title))
    for key, value in menu.items():
        print("{} - {}".format(key, value))

    com = input("\nEntrez le n° de votre choix : ")

    if com in menu and com.isdigit():
        if not int(com):
            sys.exit()
        else:
            return com
    else:
        print("\n!!! Choix invalide !!!\n")
        return menu_input(menu, title)

def main():
    """ Main function """

    busboy = Busboy()
    title = ''
    menu = {'1' : "Quels aliment souhaitez vous remplacer ?",
            '2' : "Retrouver mes aliments substitués."}
    com = menu_input(menu, title)

    if com == '1':
        title = "---Choisissez une catégorie.---"
        menu = busboy.groups_menu()
        com = menu_input(menu, title)

        title ="---Choisissez un produit.---"
        menu = busboy.products_menu(com)
        com = menu_input(menu, title)

        product = busboy.product_details(busboy.keyword(com))
        show_product(**product)

        busboy.dismiss()

    elif com == '2':
        pass

if __name__ == '__main__':
    main()
