#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ui.py
# Author: Germain GAILLARD <gaillard.germain@gmail.com>
# Version: 0.1
# License: GNU GPL

import sys
from busboy import Busboy

class Ui:
    def __init__(self):
        self.title = None
        self.menu = None

    def show_saved(self, **substituts):
        for key, value in substituts.items():
            print("\t- '{}' Peu être remplacé par '{}'".format(key, value))

    def show_product(self, **product):
        print('\n---Substitut---\n|')
        for key, value in product.items():
            if value and ', ' in value:
                new = value.replace(', ', '\n|\t  -')
                print("|\t{} :\n|\t  -{}".format(key, new))
            else:
                print("|\t{} : {}".format(key, value))
        print('|\n------------\n')

    def menu_input(self):
        """ Display menu with user's entry """

        print('\n{}'.format(self.title))
        if not self.menu:
            print("\nAucun aliments dans cette catégorie.\n")

        for key, value in self.menu.items():
            print("{} - {}".format(key, value))

        com = input("\nEntrez le n° de votre choix : ")

        if com in self.menu and com.isdigit():
            return int(com)
        else:
            print("\n!!! Choix invalide !!!\n")
            return self.menu_input()

    def main(self):
        """ Main function """

        busboy = Busboy()

        while True:
            self.title = "Bienvenu sur l'application Pure Beurre"
            self.menu = {'1' : "Quels aliment souhaitez vous remplacer ?",
                         '2' : "Retrouver mes aliments substitués.",
                         '0' : "Quitter."}
            com = self.menu_input()

            if not com:
                break

            if com == 1:
                self.title = "---Choisissez une catégorie.---"
                self.menu = busboy.groups_menu()
                com = self.menu_input()

                self.title ="---Choisissez un produit.---"
                self.menu = busboy.products_menu(com)
                com = self.menu_input()

                product_id = com
                substitut_id = busboy.substitut_id(product_id)
                substitut = busboy.product_detail(substitut_id)
                self.show_product(**substitut)

                self.title = "Souhaitez-vous sauvegarder le résultat ?"
                self.menu = {'1' : "Oui", '2' : "Non"}
                com = self.menu_input()

                if com == 1:
                    busboy.save((product_id, substitut_id))
                    com = None
                elif com == 2:
                    com = None

            elif com == 2:
                substituts = busboy.substituts_saved()
                self.show_saved(**substituts)

        busboy.dismiss()

if __name__ == '__main__':
    Ui().main()
