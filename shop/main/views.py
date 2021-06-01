from django.shortcuts import render
from main.models import Product

# Create your views here.
def get_products_page(request):
    # Обрабатываю параметры строки запроса с именем "category".
    choosen_category = request.GET.get("category", "")

    products = None
    if (choosen_category != ""):
        products = Product.objects.all().filter(category__slug=choosen_category)
    else:
        products = Product.objects.all()

    return render(request, "main/products.html", {'products': products, 'category':choosen_category})