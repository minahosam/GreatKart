from main.models import *
from .models import *


def all_category(request):
    all_categories = Category.objects.all()
    return dict( all_categories = all_categories)


def info(request):
    all_info = information.objects.all().first()
    return dict( all_info = all_info )