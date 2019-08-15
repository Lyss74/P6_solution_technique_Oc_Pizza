# -*- coding: Utf-8 -*-


from Python.config import db, INDEX_ERROR
from passlib.hash import pbkdf2_sha256
from Python import instance_data as repos
from Python import dataclass_data as models
from Python import insert_data as insert
from pprint import pprint


# cd C:\Users\Admin\GoogleDrive\DATA_OPEN_PROG\OPENCLASSROOMS\MyProjectOC\SYS\MySQL8\bin


class UserTest:
    """
        This class on a realised charge
    """

    def __init__(self):
        self.db = db

    def home(self):
        """
            You can register in the database of "OC Pizza"
        """
        print('\n','°*°*°*°*°*°*°*°*°*°*°*°*°*°*°', '\n',
              "***  Bonjour et bienvenue ***",
              '\n','°*°*°*°*°*°*°*°*°*°*°*°*°*°*°', '\n',
              )
        print("Tapez:", '\n',
                  " |-'A': Alimentez la base de donnèes" '\n',
                  " |-'1': Pour vous inscrire" '\n',
                  " |-'2': Consultez la liste des employées" '\n',
                  " |-'3': Consultez les recettes des pizzas" '\n',
                  " |-'4': Consultez le statut des commandes" '\n',
                  " |-'5': Affichez le tarif des produits" '\n',
                  " |-'6': Simulez une rupture de stock" '\n',
                  " |-'Q': Pour quitter", '\n'
              )
        user = input()
        key_list = ['A', '1', '2', '3', '4', '5', '6', 'Q']
        if user not in key_list:
            print('\n', INDEX_ERROR, '\n')
            self.home()
        else:
            if user == 'A':
                self.Feed_the_base()
            elif user == '1':
                self.subscribe_test()
            elif user == '2':
                self.employee_list()
            elif user == '3':
                self.recipe_pizza()
            elif user == '4':
                self.status_list()
            elif user == '5':
                self.product_price()
            elif user == '6':
                self.order_test()
            elif user == 'Q':
                self.exit()

    def Feed_the_base(self):
        """
            Feeding the database
        """
        insert.main()
        print("Filling the database successfully !")
        self.next_step()

    def subscribe_test(self):
        """
            You can register in the database of "OC Pizza"
        """
        print('\n',
                  "Lancement du test d'inscription",
              '\n')

        data = self.actor_instance()
        validate = input("Touche 'v' pour valider")
        if validate.lower().strip() == 'v':
            suscribe = repos.ActorRepository(db)
            suscribe.save_all(data)
            last_id = suscribe.last_id()
            print(suscribe.get(last_id))
        self.next_step()

    def employee_list(self):
        """
            Consult the list of actors
        """
        print('\n',
                  "Lancement de l'affichage des employè",
              '\n')
        pprint(self.db.query(
            """
                SELECT quality, first_name, 
                last_name, Restaurants_id 
                FROM `employee` 
                INNER JOIN actor 
                ON employee.id = actor.id;
            """).all(as_dict=True)
               )
        self.next_step()

    def recipe_pizza(self):
        """
            Consult the pizza recipes
        """
        print('\n',
                  "Lancement de la consultation des recettes",
              '\n')
        pprint(self.db.query(
            """
                SELECT product.product_name, ingredient.product_name 
                AS ingredient_name FROM product 
                INNER JOIN composition 
                ON composition.Product_id=product.id
                INNER JOIN ingredient 
                ON composition.Ingredient_id=ingredient.id;            
            """).all(as_dict=True)
               )
        self.next_step()

    def status_list(self):
        """
            Check the status of orders
        """
        print('\n',
                  "Consulter les status des commandes",
              '\n')
        pprint(self.db.query(
            """
                SELECT `status`, first_name, last_name, 
                restaurant_name, `order`.order_date 
                FROM oc_pizza.`order`
                INNER JOIN `status` 
                ON `status`.id=`order`.id
                INNER JOIN actor 
                ON actor.id=`order`.Actors_id
                INNER JOIN restaurant 
                ON restaurant.id=`order`.Restaurants_id 
                ORDER BY `order`.order_date;
                
            """).all(as_dict=True))
        self.next_step()

    def product_price(self):
        """
            Check the price per product
        """
        pprint(self.db.query(
            """
                SELECT product_name, product_price 
                FROM oc_pizza.product;
            """).all(as_dict=True))
        self.next_step()

    def order_test(self):
        """
            Simulate an order
        """
        print('\n',
                  "Consulter les produit en rupture de stock",
              '\n')
        stock = self.db.query(
            """
                SELECT product.product_name, 
                ingredient.product_name, 
                composition.weight 
                FROM composition
                INNER JOIN product 
                ON product.id=composition.Product_id
                INNER JOIN ingredient 
                ON ingredient.id=composition.Ingredient_id
                WHERE composition.weight < 5;
            """).all(as_dict=True)
        if len(stock) >= 1:
            print("Ingrédient en rupture")
            pprint(stock)
            self.next_step()

    def actor_instance(self):
        """
            You can register in the database of "OC Pizza"
        """
        first_name = input('\n' "|*** Prénom ***|"'\n')
        last_name = input('\n' "|*** Nom ***|"'\n')
        phone = input('\n' "|*** Téléphone ***|"'\n')
        mail = input('\n' "|*** Mail ***|"'\n')
        password = input('\n' "|*** Mot de passe ***|"'\n')
        address, postal_zip, city, complement = self.address()
        subscribe = [models.Actor(
                first_name=first_name,
                last_name=last_name,
                authentication_password=pbkdf2_sha256.hash(password),
                phone=models.Phone(phone=phone),
                mail=models.Email(mail=mail),
            address=models.Address(
                address=address,
                zip_code=postal_zip,
                city=city,
                additional_address=complement
                    ))]
        return subscribe

    def address(self):
        """
            Fill in an address
        """
        address = input('\n'"|*** Votre addresse ***|"'\n')
        postal_zip = input('\n'"|*** Code postal ***|"'\n')
        city = input('\n'"|*** Ville ***|"'\n')
        complement = input('\n'"|*** Complément ***|"'\n')
        return address, postal_zip, city, complement

    def next_step(self):
        """
            Propose the new choice in home menu
        """
        user = input('\n' 
                        'Que souhaitez-vous faire?' '\n'
                         " |-'H': Retour au menu" '\n'
                         " |-'R': Imprimé les requêtes" '\n'
                         " |-'Q': Quitter l'application" '\n'
                     )
        key_list = ['H', 'R', 'Q']
        if user not in key_list:
            print('\n', INDEX_ERROR, '\n')
            self.home()
        else:
             if user == 'H':
                 self.home()
             elif user == 'R':
                self.print_the_query()
             elif user == 'Q':
                 self.exit()

    def print_the_query(self):
        """
            print(query)
        """
        print('\n',
                [ "Commande connexion :",
                  "mysql --host=localhost --user=OCP6 --password=OC_STUDENT"
                ], '\n',
                [ "Reqêtes actor's list :",
                  "SELECT quality, first_name, last_name "
                  "Restaurants_id FROM `employee "
                  "INNER JOIN actor ON employee.id = actor.id;"
                ], '\n',
                [ "Reqêtes recipe Pizza :",
                  "SELECT product.product_name, ingredient.product_name AS ingredient_name FROM product "
                  "INNER JOIN composition ON composition.Product_id=product.id "
                  "INNER JOIN ingredient ON composition.Ingredient_id=ingredient.id;"
                ], '\n',
                [ "Reqêtes statut des commandes :",
                  "SELECT status.status, actor.first_name, actor.last_name, restaurant.restaurant_name, order.order_date FROM oc_pizza.order"
                  "INNER JOIN status ON status.id=order.id"
                  "INNER JOIN actor ON actor.id=order.Actors_Id"
                  "INNER JOIN restaurant ON restaurant.id=order.Restaurants_Id ORDER BY order.order_date;"
                ], '\n',
                [ "Product price :",
                  "SELECT product_name, product_price "
                  "FROM oc_pizza.product;"
                ], '\n',
                [ "Rupture de stock :",
                  "SELECT product.product_name, ingredient.product_name, composition.weight FROM composition"
                  "INNER JOIN product ON product.id=composition.Product_id"
                  "INNER JOIN ingredient ON ingredient.id=composition.Ingredient_id"
                  "WHERE composition.weight < 10;"
                ], '\n',
                [ "Database Dump :",
                  "mysqldump --user=OCP6 --password=OC_STUDENT Oc_Pizza > Oc_Pizza.backup.sql"
                ],
              '\n')
        self.next_step()

    def exit(self):
        """
            Exit the Program
        """
        print('\n',
              "*** ° Au revoir et à bientot ° ***",
              '\n')
        quit()


def main():
    """
        Initialize the unit test
    """

    gen = UserTest()
    gen.home()


if __name__ == "__main__":
    main()
