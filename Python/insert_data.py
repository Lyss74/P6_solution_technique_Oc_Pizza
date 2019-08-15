# -*- coding: Utf-8 -*-


from Python.config import db
from Python.faker_data import FakeCollectingData
from Python.generator_data import GeneratorData
from Python import instance_data as repos
from Python import dataclass_data as models


class InsertData:
    """
        This class is responsible for inserting all data
        in the order of relationships
    """

    def __init__(self):
        """
            Just link the db connexion
        """
        self.db = db

    # Insert the static data

    def insert_status_list(self, generate):
        status_repo = repos.StatusRepository(db)
        status = [
            models.Status(**data)
            for data in generate.gen_status_list()
        ]
        status_repo.save_all(status)

    def insert_product_type(self, generate):
        repo = repos.ProductTypeRepository(db)
        product_type = [
            models.ProductType(**data)
            for data in generate.gen_product_type()
        ]
        repo.save_all(product_type)

    def insert_barcode_type(self, generate):
        repo = repos.ProductTypeRepository(db)
        product_type = [
            models.ProductType(data)
            for data in generate.gen_barcode_type()
        ]
        repo.save_all(product_type)

    def insert_payment_list(self, generate):
        payment_repo = repos.PaymentRepository(db)
        payment = [
            models.Payment(**data)
            for data in generate.gen_payment_list()
        ]
        payment_repo.save_all(payment)

    # Insert data

    def insert_restaurant_list(self, generate):
        restaurants = repos.RestaurantRepository(db)
        restaurants.save_all(generate.gen_restaurants_list())

    def insert_employee_list(self, generate):
        employee = repos.EmployeeRepository(db)
        employee.save_all(generate.gen_employee_list())

    def insert_actor_list(self, generate):
        actors = repos.ActorRepository(db)
        actors.save_all(generate.gen_actors(number=50))

    def insert_product(self, generate):
        product = repos.ProductRepository(db)
        ingredient = repos.IngredientRepository(db)
        products, ingredients = generate.gen_product()
        product.save_all(products)
        ingredient.save_all(ingredients)

    def insert_product_stock(self, generate):
        product = repos.ProductStockRepository(db)
        product.save_all(generate.gen_product_stock())

    def insert_product_barcode(self, generate):
        product = repos.ProductRepository(db)
        product.save_all(generate.gen_product_barcode())

    def insert_ingredient(self, generate):
        ingredient = repos.IngredientRepository(db)
        ingredient.save_all(generate.gen_ingredient())

    def insert_stock_product(self, generate):
        product_stock = repos.ProductStockRepository(db)
        product_stock.save_all(generate.generate_stock_product())

    def insert_composition(self, generate):
        composition = repos.CompositionRepository(db)
        composition.save_all(generate.generate_composition())

    def insert_order(self, generate):
        order = repos.OrderRepository(db)
        order.save_all(generate.generate_order())

    def insert_shopping(self, generate):
        shop = repos.ShoppingCartRepository(db)
        shop.save_all(generate.generate_shopping())

    def insert_payment(self, generate):
        invoice = repos.PaymentRepository(db)
        invoice.save_all(generate.generate_payment())

    def insert_invoice(self, generate):
        invoice = repos.InvoiceRepository(db)
        invoice.save_all(generate.generate_invoice())

    def pizza_product(self, generate):
        invoice = repos.ProductRepository(db)
        invoice.save_all(generate.gen_pizza())

    def pizza_ingredient(self, generate):
        invoice = repos.IngredientRepository(db)
        invoice.save_all(generate.gen_pizza_ingredient())

    def pizza_composition(self, generate):
        invoice = repos.CompositionRepository(db)
        invoice.save_all(generate.pizza_composition())

    # Launch the insert data per section

    def launch_insert_static(self):
        """
            Group the data for insert
        """
        generate = GeneratorData()
        self.insert_status_list(generate)
        print("Status list insert ok !")
        self.insert_payment_list(generate)
        print("Payment list insert ok !")
        self.insert_restaurant_list(generate)
        print("Restaurant list insert ok !")
        self.insert_product_type(generate)
        print("Product_type list insert ok !")

    # Insert organization

    def launch_insert_actor(self):
        """
            Group the data for insert Actor
        """
        generate = GeneratorData()
        self.insert_actor_list(generate)
        print("Actor list insert ok !")
        self.insert_employee_list(generate)
        print("Employee list insert ok !")

    def launch_insert_product(self):
        """
            Group the data for insert product
        """
        generate = GeneratorData()
        self.insert_product(generate)
        print("Product list insert ok !")

    def launch_insert_pizzas(self):
        """
            Group the data for insert pizza product
        """
        generate = GeneratorData()
        self.pizza_product(generate)
        print("Pizza product list insert ok !")
        self.insert_ingredient(generate)
        print("Ingredient list insert ok !")
        self.pizza_composition(generate)
        print("Pizza composition list insert ok !")
        self.insert_stock_product(generate)
        print("Stock product list insert ok !")

    def launch_insert_order(self):
        """
            Group the data for order
        """
        generate = GeneratorData()
        self.insert_order(generate)
        print("Order list insert ok !")
        self.insert_shopping(generate)
        print("Shopping list insert ok !")
        self.insert_invoice(generate)
        print("Invoice list insert ok !")


def main():
    """
        Initialize the data collect
    """
    init = InsertData()

    # Insert the static data
    init.launch_insert_static()

    # Insert actor data
    init.launch_insert_actor()

    # Insert the product data
    init.launch_insert_product()
    init.launch_insert_pizzas()

    # Insert the order data
    init.launch_insert_order()
