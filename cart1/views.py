from django.shortcuts import render, get_object_or_404
from pipenv.core import console

from .cart1 import Cart1
from django.http import JsonResponse
from core.models import Product

def cart_summary(request):
    return render(request, "cart_summary.html", {})
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from decimal import Decimal

def cart_add(request):
    print(f"CART ADD: {request.POST.get('action')}")
    cart = Cart1(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product)

        return JsonResponse(cart.as_dict())
    return JsonResponse({'error': 'Invalid action'}, status=400)


def cart_remove(request):
    cart = Cart1(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.remove(product_id)
        return JsonResponse(cart.as_dict())
    return JsonResponse({'error': 'Invalid action'}, status=400)

def cart_update(request):
    cart = Cart1(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        quantity = int(request.POST.get('quantity'))
        cart.update(product_id, quantity)
        return JsonResponse(cart.as_dict())
    return JsonResponse({'error': 'Invalid action'}, status=400)

def cart_detail(request):
    cart = Cart1(request)
    return JsonResponse(cart.as_dict())