from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('smartphones', views.smartphones, name='smartphones'),
    path('smartwatches', views.smartwatches, name='smartwatches'),
    path('headphones', views.headphones, name='headphones'),
    path('earbuds', views.earbuds, name='earbuds'),
    path('guide', views.guide, name='guide'),
    path('cart', views.cart, name='cart'),
    path('register', views.register_request, name='register'),
    path('login', views.login_request, name='login'),
    path('logout', views.logout_request, name="logout"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    # path('<slug:smartwatch_slug>/', views.product_detail, name='product_detail'),
]
