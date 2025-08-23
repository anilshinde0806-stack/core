from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.utils.crypto import get_random_string
from pipenv.core import console
from .models import UserProfile
from core.models import Product
from .models import Order, OrderItem, Customer
from cart1.cart1 import Cart1
from django.contrib.auth.decorators import login_required
from core.forms import ProfileUpdateForm
from django.contrib import messages
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
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        if order.is_paid:
            return JsonResponse({
                "success": True,
                "payment_id": order.payment_id,
                "amount": float(order.total_price),
            })

        # ⚡ Simulate payment success
        payment_id = f"PAY{order.id}12345"
        amount = order.total_price

        order.payment_id = payment_id
        order.is_paid = True
        order.save()

        return JsonResponse({
            "success": True,
            "payment_id": payment_id,
            "amount": float(amount),
        })

    # If GET → render payment page
    return render(request, "payment.html", {"order": order})
@login_required
def dashboard_view(request):
    user = request.user
    orders = Order.objects.filter(customer=user).order_by('-id')  # show latest first
    context = {
        'user': user,
        'orders': orders,
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def dashboard_view(request):
    customer, _ = Customer.objects.get_or_create(
        user=request.user,
        defaults={'full_name': request.user.get_full_name(), 'email': request.user.email}
    )
    orders = Order.objects.filter(customer=customer).order_by('-id')
    return render(request, 'dashboard.html', {'orders': orders})
@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, 'order_detail.html', {'order': order})

# core/views.py
@login_required
def update_profile_view(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('dashboard')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})



def guest_checkout(request):
    cart = Cart1(request)

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        create_account = request.POST.get("create_account") == "true"

        print(
            f"method:{request.method}, create_account:{create_account}, full_name:{full_name}, email:{email}, phone:{phone}, address:{address}")

        user = None
        account_password = None

        # Logged-in user
        if request.user.is_authenticated:
            user = request.user
        elif create_account:
            # Create a new user automatically
            username = email.split("@")[0] + get_random_string(4)
            account_password = get_random_string(8)
            user = User.objects.create_user(
                username=username,
                email=email,
                password=account_password,
                first_name=full_name.split()[0]
            )

            # Send email with credentials
            subject = "Your New Account at Unisex Salon"
            message = f"""
Hi {full_name},

Your account has been created automatically after your recent purchase.

Username: {username}
Password: {account_password}

You can log in at: https://anilshinde0806.pythonanywhere.com/login/

Thank you for shopping with us!
"""
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
        else:
            # Guest checkout without creating account
            user = None  # no User object, only Customer below

        # Ensure Profile exists if user exists
        if user:
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.phone = phone
            profile.address = address
            profile.save()
            login(request, user)  # log in new or existing user

        # Ensure Customer exists
        if user:
            customer, created = Customer.objects.get_or_create(
                user=user,
                defaults={'full_name': full_name, 'email': email, 'phone': phone, 'address': address}
            )
            if not created:
                # Update existing customer info
                customer.full_name = full_name
                customer.email = email
                customer.phone = phone
                customer.address = address
                customer.save()
        else:
            # Guest checkout without account: create a Customer without User
            customer, _ = Customer.objects.get_or_create(
                email=email,
                defaults={'full_name': full_name, 'phone': phone, 'address': address}
            )

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
                price=item["price"]
            )

        # Clear cart
        request.session["cart"] = {}
        request.session.modified = True

        return JsonResponse({"success": True, "order_id": order.id, "user_created": create_account})

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)
