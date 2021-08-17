from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('phones', views.phones, name='phones'),
    path('accessories', views.accessories, name='accessories'),
    path('guide', views.guide, name='guide'),
    path('cart', views.cart, name='cart'),
    path('register', views.register_request, name='register'),
    path('login', views.login_request, name='login'),
]
