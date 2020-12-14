#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ui.py
# Author: Germain GAILLARD <gaillard.germain@gmail.com>
# Version: 0.1
# License: GNU GPL

from busboy import Busboy
import os
from collections import OrderedDict


class Ui:
    def __init__(self):
        """ User interface """

        self.title = None
        self.menu = None

    def clear_console(self):
        """ Clear the console """

        if os.name == 'nt':
            _ = os.system('cls')
        else:
            _ = os.system('clear')

    def show_saved(self, unliked, liked):
        """ Display saved substituts in a simple way """

        print("\n---Mes aliments substitués.---\n")
        if unliked and liked:
            for i, k1 in enumerate(unliked.keys()):
                v1 = unliked[k1]
                k2 = list(liked)[i]
                v2 = liked[k2]
                print("({}) {} --substitut-> ({}) {}".format(k1.ljust(4),
                                                             v1.ljust(30),
                                                             k2, v2))

        else:
            print("Aucun aliments sauvegardés\n")

    def show_product(self, **product):
        """ Display the details of the product """

        print('\n---Detail---\n')
        for key, value in product.items():
            print("|  {} : {}".format(key.ljust(20), value))

    def menu_input(self):
        """ Display menu with user's entry """

        print('\n{}\n'.format(self.title.center(30, '-')))

        for key, value in self.menu.items():
            print("{} - {}".format(key.ljust(4), value))

        com = input("\nEntrez le n° de votre choix : ")

        if com in self.menu and com.isdigit():
            self.clear_console()
            return int(com)
        else:
            self.clear_console()
            print("\n!!! Choix invalide !!!\n")
            return self.menu_input()

    def main(self):
        """ Main function """

        self.clear_console()

        busboy = Busboy()
        print("\nBIENVENUE SUR L'APPLICATION PURE BEURRE")

        while True:
            self.title = "Menu Principal"
            self.menu = {'1' : "Quels aliment souhaitez vous remplacer ?",
                         '2' : "Retrouver mes aliments substitués.",
                         '0' : "Quitter."}
            com = self.menu_input()

            if not com:
                break

            if com == 1:
                self.title = "Choisissez une catégorie"
                self.menu = busboy.groups_menu()
                self.menu['0'] = "Retourner au menu principal."
                com = self.menu_input()

                if com:
                    self.title ="Choisissez un produit"
                    self.menu = busboy.products_menu(com)
                    self.menu['0'] = "Retourner au menu principal."
                    com = self.menu_input()

                if com:
                    product_id = com
                    substitut_id = busboy.substitut_id(product_id)
                    substitut = busboy.product_detail(substitut_id)
                    self.show_product(**substitut)
                    if product_id and substitut_id:
                        self.title = "Sauvegarder le résultat ? "
                        self.menu = {'1' : "Oui",
                                     '0' : "Non. Retourner au menu principal."}
                    else:
                        self.title = "Aucun résultat"
                        self.menu = {'0' : "Retourner au menu principal."}
                    com = self.menu_input()

                if com == 1:
                    busboy.save((product_id, substitut_id))
                    com = None


            elif com == 2:
                unliked, liked = busboy.substituts_saved()
                sub = dict(unliked)
                sub.update(liked)
                self.title = "Entrez le n° du produit pour voir le detail."
                self.menu = sub
                self.menu['0'] = "Retourner au menu principal."

                while com:
                    self.show_saved(unliked, liked)
                    com = self.menu_input()
                    if com:
                        choosen = busboy.product_detail(com)
                        self.show_product(**choosen)

        print("A BIENTOT...")
        busboy.dismiss()


if __name__ == '__main__':
    Ui().main()
