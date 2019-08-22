from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Marker(models.Model):
    name = models.CharField(max_length=50)
    short_description = models.CharField(max_length=200)
    long_description = models.CharField(max_length=500)
    longitude = models.DecimalField(decimal_places=14, max_digits=17, null=True, blank=True)
    latitude = models.DecimalField(decimal_places=14, max_digits=17, null=True, blank=True)
    marker_region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
