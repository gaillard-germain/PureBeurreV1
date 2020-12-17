#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ui.py
# Author: Germain GAILLARD <gaillard.germain@gmail.com>
# Version: 0.1
# License: GNU GPL

from busboy import Busboy
import os


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

    def show_product(self, product):
        """ Display the details of the product """

        print('\n{}\n'.format('Detail'.center(30, '-')))
        for key, value in product.items():
            print("|  {} : {}".format(key.upper().ljust(20), value))

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
            self.menu = {'1': "Choisir une catégorie d'aliments.",
                         '2': "Retrouver mes aliments substitués.",
                         '0': "Quitter."}
            com = self.menu_input()

            if not com:
                break

            if com == 1:
                self.title = "Choisissez une catégorie"
                self.menu = busboy.groups_menu()
                self.menu['0'] = "Retourner au menu principal."
                com = self.menu_input()

                if com:
                    self.title = "Choisissez un produit"
                    self.menu = busboy.products_menu(com)
                    self.menu['0'] = "Retourner au menu principal."
                    com = self.menu_input()

                if com:
                    product_id = com
                    substitut_id = busboy.substitut_id(product_id)
                    substitut = busboy.product_detail(substitut_id)
                    print("Une alternative à {} :"
                          .format(self.menu[str(product_id)]))
                    self.show_product(substitut)
                    if product_id and substitut_id:
                        self.title = "Sauvegarder le résultat ? "
                        self.menu = {'1': "Oui",
                                     '0': "Non. Retourner au menu principal."}
                    else:
                        self.title = "Aucun résultat"
                        self.menu = {'0': "Retourner au menu principal."}
                    com = self.menu_input()

                if com == 1:
                    busboy.save((product_id, substitut_id))
                    com = None

            elif com == 2:
                sub = busboy.substituts_saved()
                menu_sub = {}
                for key, value in sub.items():
                    menu_sub[key] = "{} de {}   --substitut->   {} de {}" \
                                    .format(value[1], value[2],
                                            value[4], value[5])
                self.title = "Mes aliments substitués"
                self.menu = menu_sub
                self.menu['0'] = "Retourner au menu principal."

                com = self.menu_input()

                while com:
                    self.show_product(busboy.product_detail(sub[str(com)][0]))
                    print("\n\nPeu être substitué par:\n")
                    self.show_product(busboy.product_detail(sub[str(com)][3]))
                    com = input("\nAppuyer sur Entrée pour continuer...")
                    self.clear_console()
                    com = self.menu_input()

        print("A BIENTOT...")
        busboy.dismiss()


if __name__ == '__main__':
    Ui().main()
