from django.shortcuts import render
from main.models import Product, Category


# Create your views here.

def get_main_page(request):
    return render(request, "main/main.html", {})


def get_about_us_page(request):
    return render(request, "main/about_us.html", {})


def get_products_page(request):
    # Обрабатываю параметры строки запроса с именем "category".
    chosen_category = request.GET.get("category", "")

    products = None
    if (chosen_category != ""):
        products = Product.objects.all().filter(category__slug=chosen_category)
    else:
        products = Product.objects.all()

    return render(request, "main/products.html", {'products': products, 'category':chosen_category})


def get_categories(request):
    categories = Category.objects.all()
    return render(request, "main/categories.html", {'categories': categories})