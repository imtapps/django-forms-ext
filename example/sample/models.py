from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=100)
    eye_color = models.ForeignKey('EyeColor')
    second_eye_color = models.IntegerField()

    def __unicode__(self):
        return self.name

class EyeColor(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name
