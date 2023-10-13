from django.urls import path
from .views import *


app_name = 'cart'
urlpatterns = [
    path('',cart,name='item'),
    path('addcart/<pk>',add_cart,name='add'),
    path('deccart/<pk>/<item_id>',decrease_cart,name='decrease'),
    path('remove/<pk>/<item_id>',remove_cart,name='remove'),
    path('checkout/',checkout,name='checkout'),
]
