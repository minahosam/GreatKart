from django import forms
from .models import *


class PlaceOrder(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ('first_name', 'last_name', 'phone', 'address_line_1', 'address_line_2','email', 'country','state','city','order_note')