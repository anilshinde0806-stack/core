from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from .views import login_modal_view


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('form1/', views.form1_view, name='form1'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
path('book/', views.booking, name='booking'),

path('ajax/booking/', views.ajax_booking, name='ajax_booking_submit'),
path('ajax/booking/form/', views.ajax_booking_form, name='ajax_booking_form'),
    path('ajax/booking/submit/', views.ajax_booking_submit, name='ajax_booking_submit'),
path('bookings/', views.booking_list, name='booking_list'),
    path('ajax/login/', login_modal_view, name='login_modal'),
path('product/<int:pk>/', views.product_detail, name='product_detail'),
path('checkout/<int:pk>/', views.checkout, name='checkout'),




]


