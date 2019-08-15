# -*- coding: Utf-8 -*-

"""
    This file has the responsibility of stored,
    - references products,
    - recipes and configurations of
    - connections to the database
"""

import records as rec


# Records settings
db = rec.Database("mysql+mysqlconnector://OCP6:OC_STUDENT@localhost/Oc_Pizza?charset=utf8mb4")

# Categories of products
CATEGORIES = [
              'Entrée',
              'Pizza',
              'Dessert',
              'Boisson',
              'soda',
              'Salade',
              ]

# Recipe for pizzas
ROYALE_PIZZA = [
                 '7610100514654',
                 '3038352876506',
                 '7613034232465',
                 '3333160002025',
                 '3560070246571',
                 '3076820002064',
                ]

ROYALE_PIZZA_BLANCHE = [
                         '7610100514654',
                         '3451790439506',
                         '7613034232465',
                         '3333160002025',
                         '3560070246571',
                         '3076820002064',
                       ]

MARGARITA_PIZZA = [
                     '7610100514654',
                     '3038352876506',
                     '3178050000725',
                     '3560070246571',
                     '3076820002064',
                  ]

CANADIENNE_PIZZA = [
                     '7610100514654',
                     '3038352876506',
                     '7613034232465',
                     '3166290200081',
                     '3560070150908',
                     '3178050000725',
                     '3333160002025',
                     '3560070246571',
                     '3076820002064',
                   ]

LIST_PIZZA = [
                ROYALE_PIZZA,
                ROYALE_PIZZA_BLANCHE,
                MARGARITA_PIZZA,
                CANADIENNE_PIZZA
             ]

RECIPE = {
            'ROYALE_PIZZA': ROYALE_PIZZA,
            'MARGARITA_PIZZA': MARGARITA_PIZZA,
            'CANADIENNE_PIZZA': CANADIENNE_PIZZA,
            'ROYALE_PIZZA_BLANCHE': ROYALE_PIZZA_BLANCHE,
         }

# The printing the index or values error
INDEX_ERROR = "IndexError - |*** /!\ Tapez le chiffre associé à votre choix dans la liste /!\ ***|"
VALUE_ERROR = "ValueError - |*** /!\ Tapez la valeur associé à votre choix dans la liste /!\ ***|"
