from django.shortcuts import render, get_object_or_404
from .cart1 import Cart1
from django.http import JsonResponse
from core.models import Product
from .models import Order, OrderItem, Customer
from cart1.cart1 import Cart1
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

from django.shortcuts import redirect

def checkout(request):
    cart = Cart1(request)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Login required"}, status=403)

        # Get shipping details from POST
        full_name = request.POST.get("full_name", request.user.username)
        email = request.POST.get("email", request.user.email)
        phone = request.POST.get("phone", "")
        address = request.POST.get("address", "")

        # Get or create Customer
        customer, created = Customer.objects.get_or_create(
            user=request.user,
            defaults={
                "full_name": full_name,
                "email": email,
                "phone": phone,
                "address": address,
            }
        )

        # Update customer info if already exists
        if not created:
            customer.full_name = full_name
            customer.email = email
            customer.phone = phone
            customer.address = address
            customer.save()

        # Create Order
        order = Order.objects.create(
            customer=customer,
            total_price=cart.total_price(),
            is_paid=False
        )

        # Create OrderItems
        for item in cart.get_items():
            OrderItem.objects.create(
                order=order,
                product_id=item["id"],
                quantity=item["quantity"],
                price=item["price"],
            )

        # Clear cart
        request.session["cart"] = {}
        request.session.modified = True

        return JsonResponse({"success": True, "order_id": order.id})

    return JsonResponse({"error": "Invalid request"}, status=400)
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer__user=request.user)
    items = order.items.all()  # related_name="items" from OrderItem model
    return render(request, "payment.html", {
        "order": order,
        "items": items,
    })

from django.shortcuts import redirect

def clear_cart_and_redirect(request):
    # Clear cart session
    if 'cart' in request.session:
        del request.session['cart']
        request.session.modified = True

    # Redirect to shop/products page
    return redirect('home')  # replace with your actual shop URL
def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer__user=request.user)

    if request.method == "POST":
        # Mark order as paid (replace with actual payment gateway logic)
        order.is_paid = True
        order.payment_id = "DEMO-PAYMENT-1234"
        order.save()

        subtotal = 0
        for item in order.items.all():
           subtotal += item.quantity * item.price
        # Return JSON for AJAX
        return JsonResponse({"success": True, "order_id": order.id,"payment_id":order.payment_id,"subtotal":subtotal})

    return render(request, "payment.html", {"order": order})