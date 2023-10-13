from django.urls import path
from .views import *

app_name = 'delivery'

urlpatterns = [
    path('',placeOrder, name='place-order'),
    path('payments/',payments,name='payment'),
    path('order-complete/',complete, name='order-complete'),
]
