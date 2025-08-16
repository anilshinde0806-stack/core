import json
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, logger
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt  # only if needed
from pipenv.core import console
from django.views.decorators.http import require_GET
from .forms import BookingForm
from .models import Booking
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache
from django.template.loader import render_to_string
from .models import Product
from django.views.decorators.cache import cache_page
from functools import wraps
from django.views.decorators.vary import vary_on_cookie
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
import logging
from django.contrib.auth import logout, authenticate

def anonymous_cache_page(timeout):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                # Logged-in user → skip caching
                return view_func(request, *args, **kwargs)
            # Not logged-in → apply caching
            return cache_page(timeout)(view_func)(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def home(request):
    #return render(request, 'index.html', {})
   products = Product.objects.all()
   return render(request, 'home/newhome.html', {'products': products})


# Register View
def register_view(request):
    print(request.POST)

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print(request.POST)
        print(form.errors)

        if form.is_valid():
            form.save()
            print('form saved')
            return redirect('login')  # Redirect to login after successful registration
    else:

        form = UserCreationForm()

    return render(request, 'core/register.html', {'form': form})

# Login View




def login_view(request):

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if request.user.is_superuser:
               return redirect('dashboard')

            else:
               return redirect('home')

    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})


# Logout View
# ✅ Only allow POST for security
 # ✅ CSRF protection
def logout_view(request):
    # ✅ Remove cart data if it exists
    request.session.pop('cart', {})

    request.session.flush()


    # ✅ Log out the user
    logout(request)

    # ✅ Redirect to homepage
    return redirect('home')  # 'home' should be the name of your homepage URLlogin_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')
@login_required
def form1_view(request):
    return render(request, 'core/form1.html')
# views.py

def booking(request):
    if request.method == 'POST':
        # Handle booking logic or save to DB
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        service = request.POST.get('service')
        date = request.POST.get('date')
        time = request.POST.get('time')
        print(f"Booked: {name}, {phone}, {service}, {date}, {time}")
        return HttpResponseRedirect('/')
    return render(request, 'dashboard/booking.html')



ogger = logging.getLogger(__name__)

@require_http_methods(["POST"])  # ✅ Only allow POST for booking submission
@csrf_exempt  # ❌ Prefer CSRF token in AJAX — only keep if you can’t send CSRF token
def ajax_booking_submit(request):
    try:
        # ✅ Check login
        if not request.user.is_authenticated:
            return JsonResponse({"status": "login_required"})

        # ✅ Handle POST booking
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            return JsonResponse({"status": "success", "booking_id": booking.id})
        else:
            # Return form errors instead of a wrong method message
            return JsonResponse({
                'status': 'error',
                'message': 'Form validation failed',
                'errors': form.errors
            })

    except Exception as e:
        logger.error(f"Exception in ajax_booking_submit: {e}", exc_info=True)
        return JsonResponse({'status': 'error', 'message': 'Server error'}, status=500)
@csrf_exempt
@login_required
def ajax_booking(request):
    if request.method == 'POST':
        service = request.POST.get('service')
        date = request.POST.get('date')
        time = request.POST.get('time')
        # ߔ Save to DB or log for now
        print(f"{request.user.username} booked {service} on {date} at {time}")
        return JsonResponse({'message': 'Booking confirmed!'})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def booking_form_view(request):
    form = BookingForm()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render(request, 'partials/booking_form.html', {'form': form}).content.decode('utf-8')
        return JsonResponse({'html': html})
    return render(request, 'home/newhome.html', {'form': form})

def ajax_booking_form(request):
    form = BookingForm(initial={
        'name': request.user.get_full_name() if request.user.is_authenticated else '',
        'email': request.user.email if request.user.is_authenticated else '',
        'appointment_date': ''
    })
    #form = BookingForm()
    html = render_to_string('partials/booking_form.html', {'form': form}, request=request)

    return JsonResponse({'form_html': html})
def booking_list(request):
    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'booking/booking_list.html', {'bookings': bookings})



def ajax_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "error", "message": "Invalid credentials"})
    return JsonResponse({"status": "error", "message": "Invalid request"})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})
def checkout(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/checkout.html', {'product': product})
@require_POST
def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        name = request.POST.get('name')
        price = float(request.POST.get('price'))

        cart = request.session.get('cart', {})

        if product_id in cart:
            cart[product_id]['quantity'] += 1
        else:
            cart[product_id] = {'name': name, 'price': price, 'quantity': 1}

        request.session['cart'] = cart

        total_items = sum(item['quantity'] for item in cart.values())
        total_price = sum(item['price'] * item['quantity'] for item in cart.values())
        console.log(f"Total items: {cart}")
        cart_items = []
        total_price = 0

        for item_id, item in cart.items():
            subtotal = item['price'] * item['quantity']
            total_price += subtotal
            cart_items.append({
                'id': item_id,
                'name': item['name'],
                'price': item['price'],
                'quantity': item['quantity'],
                'subtotal': subtotal
            })



        return JsonResponse({'items': cart_items,'total_items': len(cart_items),'total_price': total_price })

    return JsonResponse({'error': 'Invalid request'}, status=400)
def checkout_view(request):
    if not request.user.is_authenticated:
        request.session.pop('cart', None)  # Clear cart for anonymous or logged out users
        return JsonResponse({'cart_items': [], 'total_price': 0})
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('home')

    total_price = sum(item['price'] * item['quantity'] for item in cart.values())

    return render(request, 'core/checkout.html', {
        'cart': cart,
        'total_price': total_price
    })


# views.py
from django.http import JsonResponse
def get_cart(request):
    cart = request.session.get('cart', {})
    total_items = sum(item['quantity'] for item in cart.values())
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())

    return JsonResponse({
        'total_items': total_items,
        'total_price': total_price
    })
@login_required
@csrf_exempt  # if using JS fetch without CSRF in headers
def remove_cart_item(request, product_id):

    console.log(f"p id :{request.method}")
    if request.method == "POST":
        cart = request.session.get("cart", {})

        # product_id might come as int or str, normalize
        product_id = str(product_id)

        if product_id in cart:
            del cart[product_id]
            request.session["cart"] = cart
            return JsonResponse({"success": True, "message": "Item removed", "count": len(cart)})
        return JsonResponse({"success": False, "message": "Item not found"}, status=404)
    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)


def cart_details_api(request):
    console.log(f" API session_key:")

    cart = request.session.get('cart', {})
    console.log(f" API session_key: {cart}")
    cart_items = []
    total_price = 0

    for item_id, item in cart.items():
        subtotal = item['price'] * item['quantity']
        total_price += subtotal
        cart_items.append({
            'id': item_id,
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'subtotal': subtotal
        })
    console.log(cart_items)


    return JsonResponse({'items': cart_items, "total_items":len(cart_items),'total_price': total_price})


def clear_cart(request):
    request.session['cart'] = {}  # Empty dict for cart
    request.session.modified = True
    return JsonResponse({"message": "Cart cleared"})
