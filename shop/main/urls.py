from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.get_main_page, name="main"),
    path('about-us', views.get_about_us_page, name="about"),
    path('products/', views.get_products_page, name='products'),
    path('products/<slug:slug>/', views.get_specific_product, name='specific_product_url_with_slug'),
    path('categories/', views.get_categories, name='categories')
]