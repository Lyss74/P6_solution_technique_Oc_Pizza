# -*- coding: Utf-8 -*-


"""
    This file has responsibility build
    the model of the tables in the database.
    It will also serve as a link between the instances and the generations of the data
"""


from dataclasses import dataclass
from decimal import Decimal


# Information entity


@dataclass
class Email:
    mail: str
    # Id is AUTO_INCREMENT
    id: int = None


@dataclass
class Phone:
    phone: str
    # Id is AUTO_INCREMENT
    id: int = None


@dataclass
class Address:
    address: str
    zip_code: str
    city: str
    additional_address: str
    # Id is AUTO_INCREMENT
    id: int = None


# Actors entity


@dataclass
class Actor:
    first_name: str
    last_name: str
    authentication_password: str
    # Foreign key attribute
    mail: Email
    phone: Phone
    address: Address
    # Id is AUTO_INCREMENT
    id: int = None


# Restaurants entity


@dataclass
class Status:
    status: str
    # Id is AUTO_INCREMENT
    id: int = None


@dataclass
class Restaurant:
    restaurant_name: str
    # Foreign key attribute
    address: Address
    phone: Phone
    email: Email
    # Id is AUTO_INCREMENT
    id: int = None


@dataclass
class Employee:
    social_security_numb: str
    quality: str
    date_entry: str
    # Foreign key attribute
    status: Status
    restaurant: Restaurant
    actor: Actor
    id: int = None


# Billing entity


@dataclass
class Payment:
    payment_mode: str
    # Id is AUTO_INCREMENT
    id: int = None


@dataclass
class Order:
    order_date: str
    # Foreign key attribute
    status: Status
    actor: Actor
    restaurant: Restaurant
    address: Address
    # Id is AUTO_INCREMENT
    id: int = None


@dataclass
class Invoice:
    invoice_date: str
    product_tax: float
    # Foreign key attribute
    order: Order
    payment: Payment
    phone: Phone
    id: int = None


# Stock entity


@dataclass
class ProductType:
    product_type: str
    # Id is AUTO_INCREMENT
    id: int = None


@dataclass
class Product:
    id: int
    product_name: str
    product_price: Decimal

    # Foreign key attribute
    productType: ProductType
    ProductType_id: int = None
    # Id is not AUTO_INCREMENT


@dataclass
class Ingredient:
    product_name: str
    # Id is AUTO_INCREMENT
    id: int


# Associate stock entity


@dataclass
class Composition:
    # Foreign key attribute
    product: Product
    ingredient: Ingredient
    # Attribute
    weight: Decimal


@dataclass
class ProductStock:
    # Foreign key attribute
    restaurant: Restaurant
    ingredient: Ingredient
    # Attribute
    quantity: int


@dataclass
class ShoppingCart:
    # Foreign key attribute
    order: Order
    product: Product
    # Attribute
    quantity: int
    price: Decimal
