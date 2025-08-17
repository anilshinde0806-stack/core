from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    #path('', views.home, name='home'),
   path('', views.home, name='home'),

    # path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    # path('logout/', views.logout_view, name='logout'),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),

    path('form1/', views.form1_view, name='form1'),
    path("login/", auth_views.LoginView.as_view(template_name="core/login.html"), name="login"),
    #path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
path('book/', views.booking, name='booking'),

#path('ajax/booking/', views.ajax_booking, name='ajax_booking_submit'),
path('ajax/booking/form/', views.ajax_booking_form, name='ajax_booking_form'),
    path('ajax/booking/submit/', views.ajax_booking_submit, name='ajax_booking_submit'),
path('bookings/', views.booking_list, name='booking_list'),
    path('ajax/login/', views.ajax_login, name='ajax_login'),
path('product/<int:pk>/', views.product_detail, name='product_detail'),


path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
path('api/cart1/', views.get_cart, name='get_cart'),
path('api/cart/add/', views.add_to_cart, name='cart_add'),

path("api/cart/remove/<int:product_id>/", views.remove_cart_item, name="remove_cart_item"),

    #path('api/cart/remove/', views.cart_remove_api, name='cart_remove_api'),
    path('api/cart/', views.cart_details_api, name='cart_details_api'),
path("api/cart/clear/", views.clear_cart, name="clear_cart"),

]


