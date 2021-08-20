from django.db import models


class Smartphone(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    thumbnail = models.CharField(max_length=200)
    internal_memory = models.CharField(max_length=50)
    memory_card_support = models.CharField(max_length=50)
    ram = models.CharField(max_length=50)
    memory_card_type = models.CharField(max_length=50)
    processor = models.CharField(max_length=50)
    operating_system = models.CharField(max_length=50)
    screen_size = models.CharField(max_length=50)
    screen_resolution = models.CharField(max_length=50)
    screen_type = models.CharField(max_length=50)
    main_camera = models.CharField(max_length=50, blank=True)
    selfie_camera = models.CharField(max_length=50, blank=True)
    video_camera = models.CharField(max_length=50)
    bluetooth = models.CharField(max_length=50, blank=True)
    two_sim_card_support = models.CharField(max_length=50, blank=True)
    sim_card_type = models.CharField(max_length=50)
    weight = models.CharField(max_length=50)
    network_5g_bands = models.CharField(max_length=200, blank=True)
    network_4g_bands = models.CharField(max_length=200)
    network_3g_bands = models.CharField(max_length=200)
    network_2g_bands = models.CharField(max_length=200)
    wifi = models.CharField(max_length=50)
    wifi_hotspot = models.CharField(max_length=50, blank=True)
    body_dimensions = models.CharField(max_length=50)
    battery = models.CharField(max_length=50)
    nfc = models.CharField(max_length=50)
    usb_type = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    # network_speed = models.CharField(max_length=50)
    # screen_size = models.CharField(max_length=50)
    # camera = models.CharField(max_length=100)
    # operating_system = models.CharField(max_length=50)
    # processor = models.CharField(max_length=50)
    # battery_life = models.CharField(max_length=50)
    # memory = models.CharField(max_length=50)
    # ram = models.CharField(max_length=50)
    # price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self) -> str:
        return self.name


class Smartwatch(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    thumbnail = models.CharField(max_length=200)
    processor = models.CharField(max_length=50)
    operating_system = models.CharField(max_length=50)
    display = models.CharField(max_length=50)
    memory = models.CharField(max_length=50)
    battery = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = "Smartwatch"
        verbose_name_plural = "Smartwatches"

    def __str__(self) -> str:
        return self.brand + " " + self.model


class Headphones(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    thumbnail = models.CharField(max_length=200)
    battery_life = models.CharField(max_length=50)
    bluetooth_version = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    NOISE_CHOICES = (
        ("NO", "No"),
        ("YES", "Yes")
    )
    noise_cancelling = models.CharField(max_length=3, choices=NOISE_CHOICES, default="NO")

    class Meta:
        verbose_name = "Headphones"
        verbose_name_plural = "Headphones"

    def __str__(self) -> str:
        return self.brand + " " + self.model


class Earbuds(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    thumbnail = models.CharField(max_length=200)
    battery_life = models.CharField(max_length=50)
    battery_life_with_case = models.CharField(max_length=50)
    bluetooth_version = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    NOISE_CHOICES = (
        ("NO", "No"),
        ("YES", "Yes")
    )
    noise_cancelling = models.CharField(max_length=3, choices=NOISE_CHOICES, default="NO")

    class Meta:
        verbose_name = "Earbuds"
        verbose_name_plural = "Earbuds"

    def __str__(self) -> str:
        return self.brand + " " + self.model

