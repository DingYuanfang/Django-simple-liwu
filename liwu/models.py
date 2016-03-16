#coding:utf-8
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    pw = models.CharField(max_length=21)
    sign = models.CharField(max_length=150,default="一片空白...")
    #collect = models.CommaSeparatedIntegerField(max_length=500)
    #order = models.CommaSeparatedIntegerField(max_length=500)
    #signature = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name

class Accommodation(models.Model):
    user_publish = models.ForeignKey(User)
    publish_username = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    week_price = models.IntegerField(default=0)
    address = models.CharField(max_length=100)
    SOURCE_TYPE_CHOICES=(
        ('AP','apartment'),
        ('SH','single-house'),
        ('TP','student-apartment')
    )

    source_type = models.CharField(max_length=2,choices=SOURCE_TYPE_CHOICES,default='TP')
    def __unicode__(self):
        return  self.name

class Room(models.Model):
    accommodation = models.ForeignKey(Accommodation)
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name
    week_price = models.IntegerField(default=0)
    order_price = models.IntegerField(default=0)
    start_data = models.DateField('data start rent')
    end_data = models.DateField('data end rent')
    def rent_long(self):
        return self.end_data - self.start_data
    SOURCE_TYPE_CHOICES = (
        ('whole','whole room'),
        ('single','single room'),
        ('share','share room')
    )
    source_type = models.CharField(max_length=7,choices=SOURCE_TYPE_CHOICES,default='all')
    deposit = models.IntegerField(default=0)
    bathroom = models.BooleanField(default=True)




