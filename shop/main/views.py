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


def get_specific_product(request, slug):
    pass
#     product = Product.objects.get(slug=slug)
#     # Collect statistics from user.
#     if request.user.is_authenticated:
#         StatisticsItem.add_click(user=request.user, product=product)
#
#     cart_product_form = CartAddProductForm()
#     context = {'product': product,
#                'cart_product_form': cart_product_form}
#     return render(request, 'first_app/specific_product.html', context)


def get_categories(request):
    categories = Category.objects.all()
    return render(request, "main/categories.html", {'categories': categories})