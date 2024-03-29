from django.contrib import admin
from .models import Category, Smartphone, Smartwatch, Headphones, Earbuds, Cart, CartItem


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    prepopulated_fields = {'slug': ('name',)}


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Smartphone, ProductAdmin)
admin.site.register(Smartwatch, ProductAdmin)
admin.site.register(Headphones, ProductAdmin)
admin.site.register(Earbuds, ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartItem, CartItemAdmin)
