from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('category/<slug:category_slug>/', views.products, name='products_by_category'),
    # path('smartwatches/<slug:smartwatch_slug>/', views.product_detail, name='product_detail'),
    path('products/search/', views.search, name='search'),
    path('guide', views.guide, name='guide'),
    path('cart', views.cart, name='cart'),
    path('register', views.register_request, name='register'),
    path('login', views.login_request, name='login'),
    path('logout', views.logout_request, name="logout"),
    path("password_reset", views.password_reset_request, name="password_reset"),
]
