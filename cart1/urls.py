from django.urls import path
from . import views


urlpatterns = [
path('', views.cart_summary, name='cart_summary'),

path('add/', views.cart_add , name='cart_add'),
 path("remove/", views.cart_remove, name="cart_remove"),
    path("update/", views.cart_update, name="cart_update"),
    path("detail/", views.cart_detail, name="cart_detail"),
path('checkout/', views.checkout, name='checkout'),
path("orders/<int:order_id>/", views.order_confirmation, name="order_confirmation"),
    path("clear-cart/", views.clear_cart_and_redirect, name="clear_cart"),
    path("payment/<int:order_id>/", views.payment, name="payment"),
]


