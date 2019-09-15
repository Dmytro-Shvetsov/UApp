from django.db import models
from authorization.models import User
from PIL import Image, ExifTags


class Region(models.Model):
    name = models.CharField(max_length=100)
    longitude = models.DecimalField(decimal_places=20, max_digits=25, null=True, blank=True)
    latitude = models.DecimalField(decimal_places=20, max_digits=25, null=True, blank=True)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    is_district_center = models.BooleanField(default=False)
    is_region_center = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Town(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Village(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Marker(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, null=False, blank=False)
    longitude = models.DecimalField(decimal_places=20, max_digits=25, null=True, blank=True)
    latitude = models.DecimalField(decimal_places=20, max_digits=25, null=True, blank=True)
    marker_region = models.ForeignKey(Region, on_delete=models.CASCADE)
    upload_key = models.ImageField(upload_to='images/', null=True, blank=True)
    # image_storage = models.ForeignKey(ImageStorage, on_delete=models.CASCADE, default=1)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=-1)
    in_process = models.BooleanField(default=False)

    def get_likes_count(self):
        return len(self.markerestimator_set.all().filter(vote=1))

    def get_dislikes_count(self):
        return len(self.markerestimator_set.all().filter(vote=-1))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # img = Image.open(self.image.path)
        #
        # exif = img._getexif()
        # output_size = (350, 350)
        # img.thumbnail(output_size)
        # orientation_key = 274
        # if exif and orientation_key in exif:
        #     orientation = exif[orientation_key]
        #     rotate_values = {
        #         3: Image.ROTATE_180,
        #         6: Image.ROTATE_270,
        #         8: Image.ROTATE_90
        #     }
        #     if orientation in rotate_values:
        #         img = img.transpose(rotate_values[orientation])
        # img.save(self.image.path)

    def __str__(self):
        return self.name


class MarkerEstimator(models.Model):
    LIKE = 1
    DISLIKE = -1

    vote = models.SmallIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    marker = models.ForeignKey(Marker, on_delete=models.CASCADE)
