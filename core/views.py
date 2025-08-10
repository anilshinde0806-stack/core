import json
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt  # only if needed
from decimal import Decimal
from django.contrib.auth import login, logout, authenticate, user_logged_in
from pandas.io.sas.sas_constants import column_name_text_subheader_length
from pipenv.core import console
from .forms import BookingForm
from .models import Booking
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache
from django.template.loader import render_to_string
from .models import Product
from django.views.decorators.cache import cache_page
from functools import wraps
from django.views.decorators.vary import vary_on_cookie
from django.shortcuts import render, redirect
from django.contrib import messages



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

@anonymous_cache_page(60 * 15)  # cache only for guests
@vary_on_cookie
def home(request):
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

@never_cache
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
@never_cache
@never_cache
def logout_view(request):
    logout(request)
    request.session.flush()
    response = redirect('home')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    try:
        del request.session['cart']  # Remove cart on logout
    except KeyError:
        pass

    return response

@login_required
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

@csrf_exempt  # if needed, but prefer proper CSRF token usage instead
def ajax_booking_submit(request):

    try:


        if not request.user.is_authenticated:
            return JsonResponse({"status": "login_required"})

        if request.method == "POST":
            form = BookingForm(request.POST)
            if form.is_valid():
                booking = form.save()
                return JsonResponse({"status": "success", "booking_id": booking.id})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid HTTP method'}, status=405)

        return JsonResponse({"status": "invalid_method"})
    except Exception as e:
      #  logger.error(f"Exception in ajax_booking_submit: {e}", exc_info=True)
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
    return render(request, 'newhome.html', {'form': form})

def ajax_booking_form(request):

    form = BookingForm()
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
        try:
                cart = request.session.get('cart', {})
                data = json.loads(request.body)  # expecting JSON POST
                product_id = data.get('product_id')
                product_name = data.get('product_name')
                price = data.get('price')
                quantity = data.get('quantity', 1)
                console.log(product_id)
                console.log(product_name)
                console.log(price)
                console.log(quantity)


                if product_id in cart:
                    cart[product_id]['quantity'] += 1
                else:
                    cart[product_id] = {
                        'name': product_name,
                        'price': float(price),
                        'quantity': quantity,
                    }

                request.session['cart'] = cart  # Save back to session!
                request.session.modified = True  # Mark session as modified so Django saves it

                return JsonResponse({'status': 'success', 'cart': cart})


        except Exception as e:
            return JsonResponse({"status": "try error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

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

def place_order(request):
    if request.method == "POST":
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('home')

        # TODO: Save order to DB here

        request.session['cart'] = {}  # Clear cart
        messages.success(request, "Order placed successfully!")
        return redirect('home')

# views.py
from django.http import JsonResponse

def get_cart(request):
    cart = request.session.get('cart', {})

    console.log(cart)
    # Opticart.onally, format cart items nicely

    cart.items()
    cart_items = []
    for key, item in cart.items():
        cart_items.append({
            'product_id': key,
            'product_name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'total': float(item['price']) * item['quantity'],
        })
    total_price = sum(item['total'] for item in cart_items)

    console.log(cart_items)
    return JsonResponse({'cart_items': cart_items, 'total_price': total_price})
