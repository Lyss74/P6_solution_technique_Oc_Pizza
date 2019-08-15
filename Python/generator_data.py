# -*- coding: Utf-8 -*-


import Python.config as config
from decimal import Decimal
from random import randint, choice
from Python.faker_data import FakeCollectingData
from Python.api_data import ApiCollectingData
from Python import instance_data as repos
from Python import dataclass_data as models


class GeneratorData:
    """
        This class is responsibility for generating all data
        in the order of relationships
    """

    def __init__(self):
        """
            Sharing the class
        """
        self.fake = FakeCollectingData()
        self.api = ApiCollectingData()

    # Status_list

    def gen_status_list(self):
        """
            Generate the status for order information
        """
        status_list = self.fake.fake_status(number=None)
        return status_list

    # Product_type

    def gen_product_type(self):
        """
            Generate the product type for order information
        """
        product_type = self.fake.fake_product_type(number=None)
        return product_type

    # Payment list

    def gen_payment_list(self):
        """
            Generate the the various restaurant
        """
        payment_list = self.fake.fake_payment(number=None)
        return payment_list

    def gen_restaurants_list(self, number=None):
        """
            Generate the status for order information
        """
        restaurant_address = [
            models.Restaurant(
                restaurant_name="OC Pizza Paris X",
                address=models.Address(
                    address="10 rue Oc",
                    zip_code="75 000",
                    city="Paris X em",
                    additional_address="",
                ),
                phone=models.Phone(
                    phone="+0145486730",
                ),
                email=models.Email(
                    mail="Oc_Pizza_Paris_Xem@Oc_pizza.com",
                )),
            models.Restaurant(
                restaurant_name="OC Pizza Paris XII",
                address=models.Address(
                    address="12 rue Oc",
                    zip_code="75 001",
                    city="Paris XII em",
                    additional_address="",
                ),
                phone=models.Phone(
                    phone="+0145486731",
                ),
                email=models.Email(
                    mail="Oc_Pizza_Paris_XIIem@Oc_pizza.com"
                ))]
        if number is None or number >= len(restaurant_address):
            return restaurant_address
        return restaurant_address[number]

    # Actor's list

    def gen_actors(self, number=None):
        """
            Generate the actor
        """
        return [models.Actor(
            first_name=self.fake.fake_first_name(),
            last_name=self.fake.fake_last_name(),
            authentication_password=self.fake.fake_password(),
            address=models.Address(
                *self.fake.fake_address()),
            phone=models.Phone(
                phone=self.fake.fake_phone()),
            mail=models.Email(
                mail=self.fake.fake_mail()
            ))
            for _ in range(number)]

    def gen_employee_list(self):
        """
            Generate the employee
        """
        employee = []
        restaurant_repo = repos.RestaurantRepository(config.db)
        status_repo = repos.StatusRepository(config.db)
        for i in range(50):
            employee.append(
                models.Employee(
                    social_security_numb=self.fake.fake_number_random(
                        1, 99999999999999),
                    quality=self.fake.fake_quality()[0]['quality'],
                    date_entry=self.fake.fake_date(),
                    status=choice(status_repo.get_all()),
                    restaurant=choice(restaurant_repo.get_all()),
                    actor=models.Actor(
                        first_name=self.fake.fake_first_name(),
                        last_name=self.fake.fake_last_name(),
                        authentication_password=self.fake.fake_password(),
                        address=models.Address(
                            *self.fake.fake_address()),
                        phone=models.Phone(
                            phone=self.fake.fake_phone()),
                        mail=models.Email(
                            mail=self.fake.fake_mail())
                    )))
        return employee

    # Product list

    def gen_product(self):
        """
            Generate the product
        """
        ingredients = []
        products = []
        product_types = repos.ProductTypeRepository(config.db)
        for product in self.api.all_product:
            product_obj = models.Product(
                    id=product['code'],
                    product_name=product['product_name_fr'],
                    product_price=self.fake.fake_price(),
                    productType=product_types.get_by_name(
                        product_type=product['main_category']))
            ingredient_obj = models.Ingredient(
                    id=product['code'],
                    product_name=product['product_name_fr'],
                )
            products.append(product_obj)
            ingredients.append(ingredient_obj)
        return products ,ingredients

    def gen_product_stock(self):
        """
            Adding the product in stock
        """
        product_stock = []
        restaurant_repo = repos.RestaurantRepository(config.db)
        product_repo = repos.ProductRepository(config.db)
        for restaurant in restaurant_repo.get_all():
            for product in product_repo.get_all():
                product_stock.append(
                    models.ProductStock(
                        restaurant=restaurant,
                        ingredient=product,
                        quantity=randint(10, 100)
                    ))
        return product_stock

    def gen_pizza(self):
        """
            Generate the pizza products
        """
        products = []
        product_types = repos.ProductTypeRepository(config.db)
        for product_name in config.RECIPE:
            products.append(
                models.Product(
                    id=randint(100, 90000),
                    product_name=product_name,
                    product_price=self.fake.fake_price(),
                    productType=product_types.get_by_name(product_type='Pizza')
                ))
        return products

    def gen_ingredient(self):
        """
            Generate the ingredient
        """
        ingredients = []
        for ingredient, weight in zip(self.api.barcode, self.api.key_weight()):
            ingredients.append(
                models.Ingredient(
                    id=ingredient['code'],
                    product_name=ingredient['generic_name_fr'],
                ))
        return ingredients

    def pizza_composition(self):
        """
            Generate the pizza ingredient
        """
        compositions = []
        product_repo = repos.ProductRepository(config.db)
        ingredient_repo = repos.IngredientRepository(config.db)
        for product_name, ingredients in config.RECIPE.items():
            product = product_repo.get_by_name(product_name)
            for iid in ingredients:
                ingredient = ingredient_repo.get(iid)
            # for ingredient in ingredient_repo.get_all():
                compositions.append(
                    models.Composition(
                        product=product[0],
                        ingredient=ingredient,
                        weight=Decimal(randint(1, 50))
                    ))
        return compositions

    def generate_stock_product(self):
        """
            Adding all product in stock
        """
        stocks = []
        restaurant_repo = repos.RestaurantRepository(config.db)
        ingredient_repo = repos.IngredientRepository(config.db)
        for restaurant in restaurant_repo.get_all():
            for ingredient in ingredient_repo.get_all():
                stocks.append(
                    models.ProductStock(
                        restaurant=restaurant,
                        ingredient=ingredient,
                        quantity=randint(1, 50)
                    ))
        return stocks

    # Order Product list

    def generate_order(self):
        """
            Generate the order
        """
        results = []
        status_repo = repos.StatusRepository(config.db)
        actor_repo = repos.ActorRepository(config.db)
        restaurant_repo = repos.RestaurantRepository(config.db)
        for i in range(15):
            actor = choice(actor_repo.get_all())
            results.append(
                models.Order(
                        order_date=self.fake.fake_date(),
                        status=choice(status_repo.get_all()),
                        actor=actor,
                        restaurant=choice(restaurant_repo.get_all()),
                        address=actor.address
                ))
        return results

    def generate_shopping(self):
        """
            Generate the shopping market
        """
        shoppings = []
        order_repository = repos.OrderRepository(config.db)
        product_repository = repos.ProductRepository(config.db)
        for i in range(30):
            shoppings.append(
                models.ShoppingCart(
                        order=choice(order_repository.get_all()),
                        product=choice(product_repository.get_all()),
                        quantity=1,
                        price=self.fake.fake_price()
                ))
        return shoppings

    def generate_invoice(self):
        """
            Generate the invoice of the order
        """
        invoices = []
        order_repository = repos.OrderRepository(config.db)
        payment_repo = repos.PaymentRepository(config.db)
        phone_repository = repos.PhoneRepository(config.db)
        for order in order_repository.get_all():
            for payment in payment_repo.get_all():
                for phone in phone_repository.get_all():
                    invoices.append(
                        models.Invoice(
                           invoice_date=self.fake.fake_date(),
                           product_tax=5.5,
                           order=order,
                           payment=payment,
                           phone=phone,
                        ))
        return invoices
