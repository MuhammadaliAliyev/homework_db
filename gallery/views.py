from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Product
from .form import ProductForm
# Create your views here.
def product_list(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product
    }
    return render(request, 'product_detail.html', context)

def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    context = {
        'form': form
    }
    return render(request, 'edit_product.html', context)

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    context = {
        'product': product
    }
    return render(request, 'delete_product.html', context)

def home(request):
    return HttpResponse('Hello, World!')