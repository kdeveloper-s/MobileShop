from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('phones', views.phones, name='phones'),
    path('accessories', views.accessories, name='accessories'),
    path('guide', views.guide, name='guide'),
    path('cart', views.cart, name='cart'),
    path('login', views.login, name='login'),
]
