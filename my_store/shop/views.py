from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from my_store.shop.models import Order, Product

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})

from django.contrib.auth.decorators import login_required

@login_required
def create_order(request, product_id):
    product = Product.objects.get(id=product_id)
    order = Order.objects.create(product=product, quantity=1, user=request.user)
    return redirect('product_list')
