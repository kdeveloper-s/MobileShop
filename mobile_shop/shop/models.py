from django.db import models

# Create your models here.
class MobilePhone(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    color1 = models.CharField(max_length=50)
    color2 = models.CharField(max_length=50)
    color3 = models.CharField(max_length=50)
    camera_resolution = models.IntegerField()
