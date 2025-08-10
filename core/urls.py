from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
#from .views import ajax_login


urlpatterns = [
    #path('', views._home_view, name='home'),
    path('', views.home, name='home'),


    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout, name='logout'),
    path('form1/', views.form1_view, name='form1'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
path('book/', views.booking, name='booking'),

#path('ajax/booking/', views.ajax_booking, name='ajax_booking_submit'),
path('ajax/booking/form/', views.ajax_booking_form, name='ajax_booking_form'),
    path('ajax/booking/submit/', views.ajax_booking_submit, name='ajax_booking_submit'),
path('bookings/', views.booking_list, name='booking_list'),
    path('ajax/login/', views.ajax_login, name='ajax_login'),
path('product/<int:pk>/', views.product_detail, name='product_detail'),
path('checkout/<int:pk>/', views.checkout, name='checkout'),
path('checkout/', views.checkout_view, name='checkout'),
path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
path('place-order/', views.place_order, name='place_order'),
path('api/cart/', views.get_cart, name='get_cart'),


]


