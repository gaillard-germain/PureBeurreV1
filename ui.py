#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ui.py
# Author: Germain GAILLARD <gaillard.germain@gmail.com>
# Version: 0.1
# License: GNU GPL


from dbtools import groups_menu, products_menu

def menu_input(**menu):
    """ Display menu with user's entry """

    for key, value in menu.items():
        print("{} - {}".format(key, value))

    com = input("\nEntrez le n° de votre choix : ")

    if com in menu and com.isdigit():
        return com
    else:
        print("\n!!! Choix invalide !!!\n")
        return menu_input(**menu)

menu = {'1' : "Quels aliment souhaitez vous remplacer ?",
        '2' : "Retrouver mes aliments substitués."}

com = menu_input(**menu)

if com == '1':
    menu = groups_menu()
    print("\nChoisissez une catégorie.")
    com = menu_input(**menu)
    
    menu = products_menu(com)
    print("\nChoisissez un produit.")
    com = menu_input(**menu)
