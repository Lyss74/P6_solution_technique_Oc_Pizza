# -*- coding: Utf-8 -*-


from Python import dataclass_data as table
from dataclasses import asdict


class Repository:
    """
        The class insert the data in database Oc Pizza
    """

    def __init__(self, db):
        """
            Connect to Mysql database from
            the class DataBaseUser()
        """
        self.db = db
        self.table = table

    def save(self, instance):
        """
            Save just one instance
        """
        pass

    def save_all(self, collection):
        """
            Save several instance
        """
        for instance in collection:
            self.save(instance)

    def last_id(self):
        """
            Seek the last id insert
        """
        rows = self.db.query(
            """
                SELECT LAST_INSERT_ID() 
                AS id;
            """)
        for row in rows:
            return row['id']


# Information SQL code


class EmailRepository(Repository):

    def save(self, instance):
        data = asdict(instance)
        self.db.query(
            """
                INSERT IGNORE INTO `Email`(
                id, mail
                )
                VALUES(
                :id, :mail
                );
            """, **data)

        instance.id = self.last_id()

    def get(self, id):
        """
            Just get all id in table
        """
        rows = self.db.query(
            """
                SELECT * FROM `Email` 
                WHERE id = :id;
            """, id=id).as_dict()
        for row in rows:
            return self.table.Email(**row)

    def get_all(self):
        """
            Get all instance in table
        """
        rows = self.db.query(
            """
                SELECT * FROM `Email`;
            """).all(as_dict=True)
        return [self.table.Email(**data) for data in rows]


class PhoneRepository(Repository):

    def save(self, instance):
        data = asdict(instance)
        self.db.query(
            """
                INSERT IGNORE INTO `Phone`(
                id, phone
                )
                VALUES(
                :id, :phone
                );
            """, **data)

        instance.id = self.db.query(
            """
                SELECT id FROM `Phone` 
                ORDER BY id DESC LIMIT 1;
            """).all(as_dict=True)[0]['id']

        instance.id = self.last_id()

    def get(self, id):
        rows = self.db.query(
            """
                SELECT * FROM `Phone` 
                WHERE id = :id;
            """, id=id).as_dict()
        for row in rows:
            return self.table.Phone(**row)

    def get_all(self):
        """

        """
        rows = self.db.query(
            """
                SELECT * FROM `Phone`;
            """).all(as_dict=True)
        return [self.table.Phone(**data) for data in rows]

    def get_by_name(self, phone):
        """
            Get per name in table
        """
        rows = self.db.query(
            """
                SELECT * FROM `Phone`
                WHERE phone = :phone;
            """, phone=phone).all(as_dict=True)
        return [self.table.Phone(**data) for data in rows][0]


class AddressRepository(Repository):

    def save(self, instance):
        data = asdict(instance)
        self.db.query(
            """
                INSERT IGNORE INTO `Address`(
                id, address, zip_code, city, 
                additional_address
                )
                VALUES(
                :id, :address, :zip_code, :city, 
                :additional_address
                );
            """, **data)

        instance.id = self.last_id()

    def get(self, id):
        rows = self.db.query(
            """
                SELECT * FROM `Address` 
                WHERE id = :id;
            """, id=id).as_dict()
        for row in rows:
            return self.table.Address(**row)

    def get_all(self):
        rows = self.db.query(
            """
                SELECT * FROM `Address`;
            """).all(as_dict=True)
        return [self.table.Address(**data) for data in rows]

    def get_by_name(self, address):
        rows = self.db.query(
            """
                SELECT * FROM `Address` 
                WHERE address = :address;
            """, address=address).all(as_dict=True)
        return [self.table.Address(**data) for data in rows][0]


# Restaurants SQL code


class StatusRepository(Repository):

    def save(self, instance):
        data = asdict(instance)
        self.db.query(
            """
                INSERT IGNORE INTO `Status`(
                status
                )
                VALUES(
                :status
                );
            """, **data)

        instance.id = self.db.query(
            """
                SELECT id FROM `Status` 
                ORDER BY id DESC LIMIT 1;
            """).all(as_dict=True)[0]['id']

    def get(self, id):
        rows = self.db.query(
            """
                SELECT * FROM `Status` 
                WHERE id = :id;
            """, id=id).as_dict()
        for row in rows:
            return self.table.Status(**row)

    def get_all(self):
        rows = self.db.query(
            """
                SELECT * FROM `Status`;
            """).all(as_dict=True)
        return [self.table.Status(**data) for data in rows]

    def get_by_name(self, status):
        rows = self.db.query(
            """
                SELECT * FROM Status
                WHERE status = :status;
            """, status=status).all(as_dict=True)
        return [self.table.Status(**data) for data in rows][0]


class RestaurantRepository(Repository):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addresses = AddressRepository(self.db)
        self.phones = PhoneRepository(self.db)
        self.emails = EmailRepository(self.db)

    def save(self, instance):
        self.addresses.save(instance.address)
        self.phones.save(instance.phone)
        self.emails.save(instance.email)
        data = asdict(instance)
        data['Addresses_id'] = instance.address.id
        data['Phones_id'] = instance.phone.id
        data['Emails_id'] = instance.email.id
        self.db.query(
            """
                INSERT IGNORE INTO `Restaurant`(
                restaurant_name, Addresses_id, 
                Phones_id, Emails_id
                )
                VALUES(
                :restaurant_name, :Addresses_id,
                :Phones_id, :Emails_id
                );
            """, **data)

        instance.id = self.last_id()

    def get(self, id):
        rows = self.db.query(
            """
                SELECT * FROM `Restaurant` 
                WHERE id = :id;
            """, id=id).as_dict()
        for restaurant in rows:
            self._get_foreign_objects(restaurant)
            return self.table.Restaurant(**restaurant)

    def get_all(self):
        rows = self.db.query(
            """
                SELECT * FROM `Restaurant`;
            """).all(as_dict=True)
        for restaurant in rows:
            self._get_foreign_objects(restaurant)
        return [self.table.Restaurant(**data) for data in rows]

    def get_by_name(self, restaurant_name):
        rows = self.db.query(
            """
                SELECT * FROM `Restaurant`
                WHERE restaurant_name = :restaurant_name;
            """, restaurant_name=restaurant_name).all(as_dict=True)
        return [self.table.Restaurant(**data) for data in rows][0]

    def _get_foreign_objects(self, restaurant):
        """
            Get the foreign key in other table
        """
        restaurant['address'] = self.addresses.get(restaurant['Addresses_id'])
        del restaurant['Addresses_id']
        restaurant['phone'] = self.phones.get(restaurant['Phones_id'])
        del restaurant['Phones_id']
        restaurant['email'] = self.emails.get(restaurant['Emails_id'])
        del restaurant['Emails_id']


# Actors SQL code


class ActorRepository(Repository):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.emails = EmailRepository(self.db)
        self.phones = PhoneRepository(self.db)
        self.address = AddressRepository(self.db)

    def save(self, instance):
        self.emails.save(instance.mail)
        self.phones.save(instance.phone)
        self.address.save(instance.address)
        data = asdict(instance)
        data['Emails_id'] = instance.mail.id
        data['Phones_id'] = instance.phone.id
        data['Addresses_id'] = instance.address.id
        self.db.query(
            """
                INSERT IGNORE INTO `Actor`(
                first_name, last_name, 
                authentication_password,
                Emails_id, Phones_id, Addresses_id
                )
                VALUES(
                :first_name, :last_name, 
                :authentication_password,
                :Emails_id, :Phones_id, :Addresses_id
                );
            """, **data)

        instance.id = self.last_id()

    def get(self, id):
        rows = self.db.query(
            """
                SELECT * FROM `Actor` 
                WHERE id = :id;
            """, id=id).as_dict()
        for actor in rows:
            self._get_foreign_objects(actor)
            return self.table.Actor(**actor)

    def get_all(self):
        rows = self.db.query(
            """
                SELECT * FROM `Actor`;
            """).all(as_dict=True)
        for actor in rows:
            self._get_foreign_objects(actor)
        return [self.table.Actor(**data) for data in rows]

    def _get_foreign_objects(self, actor):
        actor['mail'] = self.emails.get(actor['Emails_id'])
        del actor['Emails_id']
        actor['phone'] = self.phones.get(actor['Phones_id'])
        del actor['Phones_id']
        actor['address'] = self.address.get(actor['Addresses_id'])
        del actor['Addresses_id']


class EmployeeRepository(Repository):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.statuts = StatusRepository(self.db)
        self.restaurants = RestaurantRepository(self.db)
        self.actors = ActorRepository(self.db)

    def save(self, instance):
        data = asdict(instance)
        self.actors.save(instance.actor)
        data['Status_id'] = instance.status.id
        data['Restaurants_id'] = instance.restaurant.id
        data['Actors_id'] = instance.actor.id
        self.db.query(
            """
                INSERT INTO `Employee`(
                social_security_numb, quality, 
                date_entry, Status_id,
                Restaurants_id, Actors_id
                )
                VALUES(
                :social_security_numb, :quality, 
                :date_entry, :Status_id,
                :Restaurants_id, :Actors_id
                );
            """, **data)

        instance.id = self.db.query(
            """
                SELECT id FROM `Employee`
                ORDER BY id DESC LIMIT 1;
            """).all(as_dict=True)[0]['id']

    def get_all(self):
        rows = self.db.query(
            """
                SELECT * FROM `Employee`;
            """).all(as_dict=True)
        for row in rows:
            self._get_foreign_objects(row)
        return [self.table.Employee(**data) for data in rows]

    def _get_foreign_objects(self, employee):
        employee['status'] = self.statuts.get(employee['Status_id'])
        del employee['Status_id']
        employee['restaurant'] = self.restaurants.get(employee['Restaurants_id'])
        del employee['Restaurants_id']
        employee['actor'] = self.actors.get(employee['Actors_id'])
        del employee['Actors_id']


# Stock SQL code


class ProductTypeRepository(Repository):

    def save(self, instance):
        data = asdict(instance)
        self.db.query(
            """
                INSERT IGNORE INTO `ProductType`(
                product_type
                )
                VALUES(
                :product_type
                );
            """, **data)

        instance.id = self.db.query(
            """
                SELECT id FROM `ProductType`
                WHERE product_type = :product_type;
            """, product_type=instance.product_type).all(as_dict=True)[0]['id']

    def get_all(self):
        rows = self.db.query(
            """
                SELECT * FROM `ProductType`;
            """).all(as_dict=True)
        return [self.table.ProductType(**data) for data in rows]

    def get(self, type_product_id):
        rows = self.db.query(
            """
                SELECT * FROM `ProductType` 
                WHERE id = :type_product;
            """, type_product=type_product_id).all(as_dict=True)
        return [self.table.ProductType(**data) for data in rows][0]

    def get_by_name(self, product_type):
        rows = self.db.query(
            """
                SELECT * FROM `ProductType` 
                WHERE product_type = :product_type;
            """, product_type=product_type).all(as_dict=True)
        return [self.table.ProductType(**data) for data in rows][0]


class ProductRepository(Repository):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product_types = ProductTypeRepository(self.db)

    def save(self, instance):
        self.product_types.save(instance.productType)
        instance.ProductType_id = instance.productType.id
        data = asdict(instance)
        self.db.query(
            """
                INSERT IGNORE INTO `Product`(
                id, product_name, 
                product_price, ProductType_id
                )
                VALUES(
                :id, :product_name, 
                :product_price, :ProductType_id
                );
            """, **data)

    def get(self, id):
        rows = self.db.query(
            """
                SELECT * FROM `ProductType` 
                WHERE id = :id;
            """, id=id).as_dict()
        for row in rows:
            self._get_foreign_objects(row)
            return self.table.Product(**row)

    def get_all(self):
        rows = self.db.query(
            """
                SELECT * FROM `Product`;
            """).all(as_dict=True)
        for row in rows:
            self._get_foreign_objects(row)
        return [self.table.Product(**data) for data in rows]

    def get_by_name(self, product_name):
        rows = self.db.query(
            """
                SELECT * FROM `Product` 
                WHERE product_name = :product_name;
            """, product_name=product_name).all(as_dict=True)
        for row in rows:
            self._get_foreign_objects(row)
        return [self.table.Product(**data) for data in rows]

    def _get_foreign_objects(self, product):
        product['productType'] = self.product_types.get(product['ProductType_id'])


class IngredientRepository(Repository):

    def save(self, instance):
        data = asdict(instance)
        self.db.query(
            """
                INSERT IGNORE INTO `Ingredient`(
                id,
                product_name
                )
                VALUES(
                :id,
                :product_name
                );
            """, **data)

        instance.id = self.db.query(
            """
                SELECT id FROM `Ingredient`
                ORDER BY id DESC LIMIT 1
            """).all(as_dict=True)[0]['id']

    def get(self, id):
        rows = self.db.query(
            """
                SELECT * FROM `Ingredient` 
                WHERE id = :id
            """, id=id).as_dict()
        for row in rows:
            return self.table.Ingredient(**row)

    def get_all(self):
        rows = self.db.query(
            """
                SELECT * FROM `Ingredient`
            """).all(as_dict=True)
        return [self.table.Ingredient(**data) for data in rows]

    def get_by_name(self, product_name):
        rows = self.db.query(
            """
                SELECT * FROM product_name
                WHERE product_name = :product_name
            """, product_name=product_name).all(as_dict=True)
        return [self.table.Ingredient(**data) for data in rows][0]


# Associate table SQL code


class CompositionRepository(Repository):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ingredients = IngredientRepository(self.db)
        self.products = ProductRepository(self.db)

    def save(self, instance):
        data = asdict(instance)
        product = instance.product
        data['Product_id'] = product.id
        data['Ingredient_id'] = instance.ingredient.id
        self.db.query(
            """
                INSERT INTO `Composition`(
                Product_id, Ingredient_id,
                weight
                )
                VALUES(
                :Product_id, :Ingredient_id,
                :weight
                );
            """, **data)

    def get(self, id):
        rows = self.db.query(
            """
                SELECT * FROM `Composition` 
                WHERE id = :id;
            """, id=id).as_dict()
        for row in rows:
            return self.table.Composition(**row)

    def get_all(self):
        rows = self.db.query(
            """
                SELECT * FROM `Composition`; 
            """).all(as_dict=True)
        for row in rows:
            self._get_foreign_objects(row)
        return [self.table.Composition(**data) for data in rows]

    def _get_foreign_objects(self, composition):
        composition['Ingredients'] = self.ingredients.get(composition['Ingredient_id'])
        del composition['Ingredient_id']
        composition['Products'] = self.products.get(composition['Products_id'])
        del composition['Products_id']


class ProductStockRepository(Repository):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.restaurants = RestaurantRepository(self.db)
        self.ingredients = IngredientRepository(self.db)

    def save(self, instance):
        data = asdict(instance)
        data['Restaurant_id'] = instance.restaurant.id
        data['Ingredient_id'] = instance.ingredient.id
        self.db.query(
            """
                INSERT IGNORE INTO `ProductStock`(
                Restaurant_id, Ingredient_id,
                quantity
                )
                VALUES(
                :Restaurant_id, :Ingredient_id,
                :quantity
                );
            """, **data)

    def get_all(self):
        rows = self.db.query(
            """
                SELECT * FROM `ProductStock`
            """).all(as_dict=True)
        return [self.table.ProductStock(**data) for data in rows]


class OrderRepository(Repository):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.statuts = StatusRepository(self.db)
        self.actors = ActorRepository(self.db)
        self.restaurants = RestaurantRepository(self.db)
        self.addresses = AddressRepository(self.db)

    def save(self, instance):
        data = asdict(instance)
        data['Status_id'] = instance.status.id
        data['Actors_id'] = instance.actor.id
        data['Restaurants_id'] = instance.restaurant.id
        data['Addresses_id'] = instance.address.id
        self.db.query(
            """
                INSERT INTO `Order`(
                order_date, Status_id,
                Actors_id, Restaurants_id,
                Addresses_id
                )
                VALUES(
                :order_date, :Status_id,
                :Actors_id, :Restaurants_id,
                :Addresses_id
                );
            """, **data)

        instance.id = self.db.query(
            """
                SELECT id FROM `Order`
                ORDER BY id DESC LIMIT 1;
            """).all(as_dict=True)[0]['id']

    def get(self, id):
        rows = self.db.query(
            """
                SELECT * FROM `Order` 
                WHERE id = :id;
            """, id=id).as_dict()
        for row in rows:
            return self.table.Order(**row)

    def get_all(self):
        rows = self.db.query(
            """
                SELECT * FROM `Order`;
            """).all(as_dict=True)
        for row in rows:
            self._get_foreign_objects(row)
        return [self.table.Order(**data) for data in rows]

    def _get_foreign_objects(self, order):
        order['status'] = self.statuts.get(order['Status_id'])
        del order['Status_id']
        order['actor'] = self.actors.get(order['Actors_id'])
        del order['Actors_id']
        order['restaurant'] = self.restaurants.get(order['Restaurants_id'])
        del order['Restaurants_id']
        order['address'] = self.addresses.get(order['Addresses_id'])
        del order['Addresses_id']


class ShoppingCartRepository(Repository):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orders = OrderRepository(self.db)
        self.products = ProductRepository(self.db)

    def save(self, instance):
        data = asdict(instance)
        data['Orders_id'] = instance.order.id
        data['Products_id'] = instance.product.id
        self.db.query(
            """
                INSERT IGNORE INTO `ShoppingCart`(
                Orders_id, Products_id,
                quantity, price
                )
                VALUES(
                :Orders_id, :Products_id,
                :quantity, :price
                );
            """, **data)

    def get(self, id):
        rows = self.db.query(
            """
                SELECT * FROM `ShoppingCart` 
                WHERE id = :id;
            """, id=id).as_dict()
        for row in rows:
            return self.table.ShoppingCart(**row)

    def get_all(self):
        rows = self.db.query(
            """
                SELECT * FROM `ShoppingCart`;
            """).all(as_dict=True)
        return [self.table.ShoppingCart(**data) for data in rows]

    def _get_foreign_objects(self, shopping):
        shopping['Orders'] = self.orders.get(shopping['Orders_id'])
        del shopping['Orders_id']
        shopping['Products'] = self.products.get(shopping['Products_id'])
        del shopping['Products_id']


# Billing SQL code


class PaymentRepository(Repository):

    def save(self, instance):
        data = asdict(instance)
        self.db.query(
            """
                INSERT INTO `Payment`(
                payment_mode
                )
                VALUES(
                :payment_mode
                );
            """, **data)

        instance.id = self.db.query(
            """
                SELECT id FROM `Payment` 
                ORDER BY id DESC LIMIT 1;
            """).all(as_dict=True)[0]['id']

    def get(self, id):
        rows = self.db.query(
            """
                SELECT * FROM `Payment` 
                WHERE id = :id;
            """, id=id).as_dict()
        for row in rows:
            return self.table.Payment(**row)

    def get_all(self):
        rows = self.db.query(
            """
                SELECT * FROM `Payment`;
            """).all(as_dict=True)
        return [self.table.Payment(**data) for data in rows]


class InvoiceRepository(Repository):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orders = OrderRepository(self.db)
        self.payments = PaymentRepository(self.db)
        self.phones = PhoneRepository(self.db)

    def save(self, instance):
        data = asdict(instance)
        data['Orders_id'] = instance.order.id
        data['Payment_id'] = instance.payment.id
        data['Phones_id'] = instance.phone.id
        self.db.query(
            """
                INSERT IGNORE INTO `Invoice`(
                invoice_date, product_tax,
                Orders_id, Payment_id,
                Phones_id
                )
                VALUES(
                :invoice_date, :product_tax,
                :Orders_id, :Payment_id,
                :Phones_id
                );
            """, **data)

    def get_all(self):
        rows = self.db.query(
            """
                SELECT * FROM `Invoice`;
            """).all(as_dict=True)
        for row in rows:
            self._get_foreign_objects(row)
        return [self.table.Invoice(**data) for data in rows]

    def _get_foreign_objects(self, invoice):
        invoice['Orders'] = self.orders.get(invoice['Orders_id'])
        del invoice['Orders_id']
        invoice['Payments'] = self.payments.get(invoice['Payment_id'])
        del invoice['Payment_id']
        invoice['Phones'] = self.phones.get(invoice['Phones_id'])
        del invoice['Phones_id']
