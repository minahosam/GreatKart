from django.db import models
from main.models import *
from accounts.models import *

# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(Profile,related_name='order_user',on_delete=models.CASCADE,null=True)
    transaction_id = models.CharField(max_length=255)
    cart_id = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    item = models.ForeignKey(Product,related_name='product',on_delete=models.SET_NULL,null=True)
    item_variation = models.ManyToManyField(Variation, related_name='product_variation',blank=True)
    items = models.ForeignKey(Order,related_name='order',on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    def sub_total(self):
        return self.item.price * self.quantity