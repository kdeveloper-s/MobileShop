from django.contrib import admin
from .models import Smartphone, Smartwatch, Headphones, Earbuds


class SmartphoneAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class SmartwatchAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('brand','model',)}


class HeadphonesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('brand','model',)}


class EarbudsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('brand','model',)}

admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(Smartwatch, SmartwatchAdmin)
admin.site.register(Headphones, HeadphonesAdmin)
admin.site.register(Earbuds, EarbudsAdmin)

