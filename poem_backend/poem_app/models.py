from __future__ import unicode_literals
from django.db import models
from datetime import *

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20,default='')
    password = models.CharField(max_length=20,default='123456')
    phone = models.CharField( max_length=11,default=''),

    def __str__(self):
        return self.username



#创建Log表
class Log(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=11,default='')
    poem = models.TextField(max_length=255,null=True,blank=True)
    time = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return self.username



