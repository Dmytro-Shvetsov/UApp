from django.db import models
from PIL import Image, ExifTags
from authorization.models import User


class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Marker(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, null=False, blank=False, default='No description given')
    longitude = models.DecimalField(decimal_places=20, max_digits=25, null=True, blank=True)
    latitude = models.DecimalField(decimal_places=20, max_digits=25, null=True, blank=True)
    marker_region = models.ForeignKey(Region, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    # creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        exif = img._getexif()
        output_size = (350, 350)
        img.thumbnail(output_size)
        orientation_key = 274
        if exif and orientation_key in exif:
            orientation = exif[orientation_key]
            rotate_values = {
                3: Image.ROTATE_180,
                6: Image.ROTATE_270,
                8: Image.ROTATE_90
            }
            if orientation in rotate_values:
                img = img.transpose(rotate_values[orientation])
        img.save(self.image.path)

    def __str__(self):
        return self.name
