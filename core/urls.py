from django.urls import path
from . import views

urlpatterns = [
    #path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard_home, name='dashboard_home'),
    path('form1/', views.form1_view, name='form1'),
    path('form2/', views.form2_view, name='form2'),
]


