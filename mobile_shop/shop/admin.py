from django.contrib import admin
from .models import Category, Smartphone, Smartwatch, Headphones, Earbuds


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Smartphone, ProductAdmin)
admin.site.register(Smartwatch, ProductAdmin)
admin.site.register(Headphones, ProductAdmin)
admin.site.register(Earbuds, ProductAdmin)

