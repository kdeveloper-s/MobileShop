from django.db import models


class MobilePhone(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    thumbnail = models.CharField(max_length=200)
    network_technology = models.CharField(max_length=50)
    dimensions = models.CharField(max_length=50)
    weight = models.PositiveIntegerField()
    ip_rating = models.CharField(max_length=4, blank=True)
    display_type = models.CharField(max_length=50)
    display_refresh_rate = models.PositiveIntegerField()
    display_size = models.DecimalField(max_digits=3, decimal_places=2)
    screen_to_body_ratio = models.DecimalField(max_digits=4, decimal_places=2)
    display_resolution = models.CharField(max_length=50)
    display_protection = models.CharField(max_length=50, blank=True)
    operating_system = models.CharField(max_length=50)
    chipset = models.CharField(max_length=50)
    cpu = models.CharField(max_length=100)
    gpu = models.CharField(max_length=50)
    card_slot = models.BooleanField(default=False)
    # internal_memory = models.
    # ram = models.
    camera_resolution = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.brand + " " + self.model

