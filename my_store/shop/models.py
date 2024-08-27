from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"


from django.shortcuts import render
from .models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})


from django.shortcuts import redirect
from .models import Order

def create_order(request, product_id):
    product = Product.objects.get(id=product_id)
    Order.objects.create(product=product, quantity=1)
    return redirect('product_list')


from django.contrib.auth.models import User
from django.db import models

# Extend the user model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)

    def __str__(self):
        return self.user.username


from django.core.exceptions import ValidationError

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.user.profile.balance >= self.product.price * self.quantity:
            self.user.profile.balance -= self.product.price * self.quantity
            self.user.profile.save()
            super().save(*args, **kwargs)
        else:
            raise ValidationError("Insufficient balance.")
