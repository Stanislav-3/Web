from django.shortcuts import render, get_object_or_404, redirect
from .forms import OrderCreateForm
from .models import OrderItem, Order
from django.contrib import messages
from cart.cart import Cart



def order_create(request):
    # 1) Берем текущую карзину или создаем пустую если её нет.
    cart = Cart(request)

    # 2) Обрабатываем данные полученные от пользователя.
    if request.method == "POST":

        # 3) Передаём данные из запроса в форму.
        form = OrderCreateForm(request.POST)

        # 4) Валидируем форму.
        if form.is_valid():
            # 5) Сохраняем "чистые" данные.
            order = form.save(commit=False)
            if request.user.is_authenticated:
                cd = form.cleaned_data
                order.user = request.user
            order.save()

            # 6) Перемещаем все элементы из текущей карзины 
            #    в элементы заказа
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])

            # 7) Очищаем карзину от всех продуктов.
            #    т.к. они уже в заказе.
            cart.clear()

            messages.success(request, 'Success: Order added')
            if request.user.is_authenticated:
                orders = Order.objects.filter(user=request.user)
                context = {'order': order, 'orders': orders}
                return render(request,'orders/orders.html', context)
            else:
                context = {'order': order}
                return redirect('orders:order_specific', order.id)
    else:
        form = OrderCreateForm()
        return render(request, 'orders/create.html', {'cart': cart, 'form': form})


def order_specific(request, order_id):
    '''
    Даже аноним сможет получить эту информацию
    '''
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    context = {'order': order, 'order_items': order_items}

    return render(request, 'orders/order.html', context)


def order_all(request):
    '''
    Даже аноним сможет получить эту информацию
    '''    
    orders = Order.objects.filter(user=request.user)                

    context = {'orders': orders}
    return render(request, 'orders/orders.html', context)

