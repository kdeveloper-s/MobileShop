from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
    
    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    thumbnail = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.TextField(blank=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.name


class Smartphone(Product):
    internal_memory = models.CharField(max_length=50)
    ram = models.CharField(max_length=50)
    memory_card_support = models.CharField(max_length=50)
    memory_card_type = models.CharField(max_length=50)
    processor = models.CharField(max_length=50)
    operating_system = models.CharField(max_length=50)
    screen_size = models.CharField(max_length=50)
    screen_resolution = models.CharField(max_length=50)
    screen_type = models.CharField(max_length=50)
    video_camera = models.CharField(max_length=50)
    sim_card_type = models.CharField(max_length=50)
    weight = models.CharField(max_length=50)
    network_5g_bands = models.CharField(max_length=200)
    network_4g_bands = models.CharField(max_length=200)
    network_3g_bands = models.CharField(max_length=200)
    network_2g_bands = models.CharField(max_length=200)
    wifi = models.CharField(max_length=50)
    body_dimensions = models.CharField(max_length=50)
    battery = models.CharField(max_length=50)


class Smartwatch(Product):
    processor = models.CharField(max_length=50)
    operating_system = models.CharField(max_length=50)
    display = models.CharField(max_length=50)
    memory = models.CharField(max_length=50)
    battery = models.CharField(max_length=50)

    class Meta:
        verbose_name = "smartwatch"
        verbose_name_plural = "smartwatches"


class Headphones(Product):
    battery_life = models.CharField(max_length=50)
    bluetooth_version = models.CharField(max_length=50)
    NOISE_CHOICES = (
        ("NO", "No"),
        ("YES", "Yes")
    )
    noise_cancelling = models.CharField(max_length=3, choices=NOISE_CHOICES, default="NO")

    class Meta:
        verbose_name = "headphones"
        verbose_name_plural = "headphones"


class Earbuds(Product):
    battery_life = models.CharField(max_length=50)
    battery_life_with_case = models.CharField(max_length=50)
    bluetooth_version = models.CharField(max_length=50)
    NOISE_CHOICES = (
        ("NO", "No"),
        ("YES", "Yes")
    )
    noise_cancelling = models.CharField(max_length=3, choices=NOISE_CHOICES, default="NO")

    class Meta:
        verbose_name = "earbuds"
        verbose_name_plural = "earbuds"


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return round(float(self.product.price), 2) * self.quantity

    def __unicode__(self):
        return self.product