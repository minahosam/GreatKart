from django.db import models
from accounts.models import *
from main.models import *

# Create your models here.
METHOD = (('credit','credit'),('cash','cash'),('paypal','paypal'))

class PaymentMethod(models.Model):
    payment_method = models.CharField(max_length=20,choices=METHOD)    

    def __str__(self):
        return self.payment_method

class Payment(models.Model):
    user = models.ForeignKey(Profile,related_name='payment_user',on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=20,choices=METHOD)
    paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.payment_method

STATUS = (('Now','Now'),('Accept','Accept'),('Completed','Completed'),('Cancelled','Cancelled'),)

class Delivery(models.Model):
    user = models.ForeignKey(Profile,related_name='user_delivery',on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, related_name='delivery_payment',on_delete=models.CASCADE,null=True)
    payment_type = models.ForeignKey(PaymentMethod, related_name='pay',null=True,on_delete=models.CASCADE)
    order_number = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    order_note = models.CharField(max_length=255,null=True)
    order_total = models.FloatField(null=True)
    tax = models.FloatField(null=True)
    status = models.CharField(max_length=20,choices=STATUS,default='Now')
    ip = models.CharField(max_length=100)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'
    
    def order_without_tax(self):
        return self.order_total - self.tax

class OrderProduct(models.Model):
    order = models.ForeignKey(Delivery,related_name='order_req',on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,related_name='order_payment',on_delete=models.CASCADE)
    user = models.ForeignKey(Profile,related_name='o_user',on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='o_product',on_delete=models.CASCADE)
    variation = models.ManyToManyField(Variation, related_name='o_variation',null=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)