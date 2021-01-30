from operator import index
from playhouse.postgres_ext import ArrayField
from .database import db
from peewee import *
from datetime import datetime, date, timedelta

class TypeUser(Model):
    libelle = CharField(null=True)
    isactive = BooleanField(default=False)

    class Meta:
        database = db
        table_name = "typeusers"

class User(Model):
    class Meta:
        database = db
        table_name = "users"

    first_name = CharField(null=True)
    last_name = CharField(null=True)
    username = CharField(null=True)
    email = CharField(unique=True, null=True)
    hashed_password = CharField()
    isactive = BooleanField(default=False)
    address = CharField(null=True)
    column = CharField(null=True)
    typeuser = ForeignKeyField(TypeUser, backref="users", null=True)


class Produit(Model):
    class Meta:
        database = db
        table_name = "produits"


class Order(Model):
    class Meta:
        database = db
        table_name = "orders"
    
    product = ForeignKeyField(Produit, backref="orders")
    client = ForeignKeyField(User, backref="my_orders")
    confirmed = BooleanField(default=False, null=True)
    delivered = BooleanField(default=False, null=True)
    total = FloatField(null=True)
    discount = FloatField(null=True)

class Country(Model):
    class Meta:
        database = db
        table_name ="contries"
    
    code = IntegerField(null=True)
    iso = IntegerField(null=True)
    fullname = CharField(null=True)
    shortcode = CharField(null=True)

class Category(Model):
    class Meta:
        database = db
        table_name = "categories"
    
    title = IntegerField(null=True)
    description = CharField(null=True)
    parent = ForeignKeyField("self", backref="children", null=True)

class Boutique(Model):
    class Meta:
        database = db
        table_name = "boutiques"
    
    name = IntegerField(null=True)
    slogan = CharField(null=True)
    location = CharField(null=True)
    owner = ForeignKeyField(User, backref="boutiques", null=True)
    category = ForeignKeyField(Category, backref="boutiques")    
    registration_date = DateField(default=datetime.now(), null=True)
    logo = CharField(null=True)
