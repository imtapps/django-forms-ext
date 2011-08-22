from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=100)
    eye_color = models.ForeignKey('EyeColor')

class EyeColor(models.Model):
    name = models.CharField(max_length=30)
