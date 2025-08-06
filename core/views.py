from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
#from django.shortcuts import render
from django.http import HttpResponseRedirect
#from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
#from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
#from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
#from .forms import BookingForm  # Assuming you've created one
from django.shortcuts import render
from django.http import JsonResponse
from .forms import BookingForm
from django.core.mail import send_mail

#from .forms import RegisterForm
#from django.contrib.auth.views import LoginView, LogoutView
# Register View

from django.contrib.auth.forms import UserCreationForm

def home(request):
    return render(request, 'home/newhome.html')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
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
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

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
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = BookingForm(request.POST)
        if form.is_valid():
            existing = Booking.objects.filter(
                appointment_date=form.cleaned_data['appointment_date'],
                appointment_time=form.cleaned_data['appointment_time']
            )

            if existing.exists():
                return JsonResponse({'error': 'Time slot already booked!'}, status=400)

            if form.is_valid():
                booking = form.save()

                # ✅ Send confirmation email
                send_mail(
                    'Booking Confirmed',
                    'Thank you for your booking!',
                    'anilshinde0806@gmail.com',
                    [booking.email],
                    fail_silently=False,  # ❗ Set to False to raise any error
                )

                return JsonResponse({'success': True})

            return JsonResponse({'message': 'Booking successful'})
        else:
            # If form has errors, re-render HTML to return
            html = render(request, 'partials/booking_form.html', {'form': form}).content.decode('utf-8')
            return JsonResponse({'form_html': html}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

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

from django.shortcuts import render
from .models import Booking

def booking_list(request):
    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'booking/booking_list.html', {'bookings': bookings})

