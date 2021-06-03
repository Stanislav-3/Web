from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.get_main_page, name="main"),
    path('about-us', views.get_about_us_page, name="about"),

    path('products/', views.get_products_page, name='products'),
    path('products/<slug:slug>/', views.get_specific_product, name='specific_product_url_with_slug'),

    path('categories/', views.get_categories, name='categories'),

    # user
    path('registration/', views.get_registration_page, name='registration'),
    path('login/', views.get_login_page, name='login'),
    # path('logout/', views.logout_user, name="logout"),
    # path('user-profile/', views.get_user_profile_page, name="user_profile"),
]