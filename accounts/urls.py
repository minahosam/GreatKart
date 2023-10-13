from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('register',register,name='register'),
    path('login',login,name='login'),
    path('logout',logout,name='logout'),
    path('activate/<uid>/<token>/',activate,name='activate'),
    path('dashboard',dashboard,name='dashboard'),
    path('',dashboard,name='dashboard'),
    path('reset-password/',reset_pass,name='reset_password'),
    path('reset/<uid>/<token>/',reset,name='reset'),
    path('change-password/',change_password,name='change_password'),
    path('my_orders/',my_orders,name='my_orders'),
    path('edit_profile/',update_profile,name='edit_profile'),
    path('changePassword/',changePassword,name='changePassword'),
    path('order-detail/<orderNo>/',order_details,name='orderDetails'),
]
