from django.urls import path, re_path
from . import views

urlpatterns = [
    path('products/', views.get_products_page, name='products'),
    # change view
    path('categories/', views.get_categories, name='categories'),
    # path('', views.get_products_page, name='products_url'),
    path('', views.get_main_page, name="main"),
    path('about-us', views.get_about_us_page, name="about")
]