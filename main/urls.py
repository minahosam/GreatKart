from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [
    path('',homepage,name='home'),
    path('store/',store,name='store'),
    path('store/<slug>',store,name='store'),
    path('product/<slug>',detail_page,name='detail'),
    path('search/',Search,name='search'),
    path('review/<slug>',reviewFunction,name='review'),
]
