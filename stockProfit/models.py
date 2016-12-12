from __future__ import unicode_literals

from django.db import models
from mongoengine import *

# Create your models here.

class Employees(Document):
	email = StringField(required=True)
	first_name = StringField(max_length=50)
	last_name = StringField(max_length=50)


class Post(Document):
	title = StringField(max_length=120, required=True)
	content = StringField(max_length=500, required=True)
	last_update = DateTimeField(required=True)

class StockValues(Document):
	date = DateTimeField()
	name = StringField(max_length=300)
	ticker = StringField(max_length=10)
	price = FloatField()
	valuechange = IntField()

class MonthlyWeather(models.Model):
	month = StringField(max_length=10)
	temp = IntField()

class LiveDataValue(Document):
	time = DateTimeField()
	symbol = StringField(max_length=10)
	price = FloatField()
	meta = {'strict': False}