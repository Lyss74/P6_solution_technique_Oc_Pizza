# -*- coding: Utf-8 -*-


import random
from datetime import date as date
from random import randint, sample
from passlib.hash import pbkdf2_sha256
from faker import Faker
fake = Faker("fr_FR")


class FakeCollectingData:
    """
        This class has the responsibility
        generating the data to feed the database
    """

    def __init__(self):
        """ The constructor is not used here """
        pass

    # Address attribute section:
    def address(self):
        numb = self.fake_number_random(1, 9999)
        street = fake.street_name()
        return f"{numb} {street}"

    def postal_zip(self):
        postal_zip = self.fake_number_random(1, 9999)
        return postal_zip

    def city(self):
        city = fake.city()
        return city

    def complement_address(self):
        random_num = str(self.fake_number_random(1, 99))
        complement_list = (
                            '',
                            'apartment ' + random_num,
                            'Floor ' + random_num,
                            'Bell ' + random_num,
                            ''
                          )
        complement = sample(complement_list, 1)
        return complement[0]

    def fake_address(self):
        address = self.address()
        postal_zip = self.postal_zip()
        city = self.city()
        complement = self.complement_address()
        return address, postal_zip, city, complement

    # Civility attribute section:
    def fake_first_name(self):
        first_name = fake.first_name()
        return first_name

    def fake_last_name(self):
        last_name = fake.last_name()
        return last_name

    # Password attribute section:
    def fake_password(self):
        return pbkdf2_sha256.hash("Oc_pizza")

    # Mail attribute section:
    def fake_mail(self):
        mail = fake.email()
        return mail

    # Phone attribute section:
    def fake_phone(self):
        prefix = "3356",  "0176", "0450", "0629"
        form = sample(prefix, 1)
        number = self.fake_number_random(1, 999999)
        form.append(number)
        phone = "".join(form)
        return phone

    # # Restaurant attribute section:
    # def fake_restaurant(self, number=1):
    #     name_list = ('Oc Pizza Paris Xem',
    #                  'Oc Pizza Paris XIIem')
    #     restaurant_name = \
    #         sample(name_list, number if number else len(name_list))
    #     return \
    #         [{'restaurant_name': data} for data in restaurant_name]

    # Status attribute section:
    def fake_status(self, number=1):
        status_list = (
                       'En court de préparation',
                       'Commande terminé',
                       'Commande en cours de livraison',
                       'Commande livré',
                      )
        status = \
            sample(status_list, number if number else len(status_list))
        return [{'status': data} for data in status]

    # Employee attribute section:
    def fake_quality(self, number=1):
        quality_list = (
                        'Gerant',
                        'Pizzaïolos',
                        'Hotesse',
                        'Livreur'
                       )
        quality = \
            sample(quality_list, number if number else len(quality_list))
        return [{'quality': data} for data in quality]

    # Product type attribute section:
    def fake_product_type(self, number=1):
        product_type = (
                        'Salade',
                        'Entrée',
                        'Pizza',
                        'Dessert',
                        'Boisson',
                        'soda',
                        'Supplément'
                       )
        type = \
            sample(product_type, number if number else len(product_type))
        return [{'product_type': data} for data in type]

    # Administrative attribute section:
    def fake_price(self):
        price = (
                    str(self.fake_number_random(1, 99))
                    + '.' +
                    str(self.fake_number_random(1, 99))
                )
        return price

    def fake_payment(self, number=1):
        payment_list = (
                        'Espece',
                        'Carte bancaire',
                        'Cheque bancaire',
                        'Tiket restaurant'
                        )
        mode = \
            sample(payment_list, number if number else len(payment_list))
        return [{'payment_mode': data} for data in mode]

    def fake_number_random(self, count, count1):
        fake_number = randint(count, count1)
        return str(fake_number)

    def fake_date(self):
        day = fake.day_of_month()
        month = fake.month_name()
        year = fake.year()
        # return f"{year}-{random.randint(1, 12)}-{day}"""
        return date(int(year), random.randint(1, 12), int(28))
