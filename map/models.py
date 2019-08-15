from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=100)
    longitude = models.DecimalField(decimal_places=8, max_digits=11)
    latitude = models.DecimalField(decimal_places=8, max_digits=10)
    color = models.CharField(max_length=10)