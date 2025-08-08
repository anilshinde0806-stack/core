from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, user_logged_in
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from pipenv.core import console
import logging
from .forms import BookingForm
from django.core.mail import send_mail
from .models import Booking
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.contrib.auth.forms import UserCreationForm
from .models import Product
from django.shortcuts import get_object_or_404
@cache_page(60 * 15)  # Cache the homepage for 15 minutes
def home(request):
        products = Product.objects.all()#.order_by('-created_at')
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
        console.print(form.errors)  # ߑ check this in the console
        console.print('form created')

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
               console.print(user.user_type)
            else:
               return redirect('home')

    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('home')

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


@require_POST
@login_required

def ajax_booking_submit(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user  # optional if you're tracking users
            booking.save()
            return JsonResponse({'success': True})  # ✅ this must exist
        else:
            return JsonResponse({'success': False, 'error': form.errors.as_json()})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
#if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':

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
    return render(request, 'booking_page.html', {'form': form})

def ajax_booking_form(request):
        form = BookingForm()
        # ߑ This should only render the form partial, NOT the full HTML page
        html = render(request, 'partials/booking_form.html', {'form': form}).content.decode('utf-8')
        return JsonResponse({'form_html': html})
def booking_list(request):
    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'booking/booking_list.html', {'bookings': bookings})


def login_modal_view(request):
    try:
     if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            logger = logging.getLogger('core')
            logger.info("Login successful for user %s", user.username)

            if user.is_superuser:
                print('superuser logged in')

                print("Reverse dashboard URL:", reverse('dashboard'))
                return JsonResponse({'success': True, 'redirect_url': reverse('dashboard')})
            else:
                print('staff user logged in')

                print("Reverse home URL:", reverse('home'))
                return JsonResponse({'success': True, 'redirect_url': reverse('home')})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid credentials'})
     return JsonResponse({'success': False, 'error': 'Invalid request method'})
    except Exception as e:
     return JsonResponse({'success': False, 'error': f'Server error: {str(e)}'})
    #return render(request, 'core/login_modal_form.html')


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})
def checkout(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/checkout.html', {'product': product})
