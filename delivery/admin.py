from django.contrib import admin
from .models import *

# Register your models here.

class OrderProductTabular(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ['order','payment','user', 'product', 'variation', 'quantity', 'product_price']
    extra = 0


class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email', 'city', 'order_total', 'tax', 'status', 'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_per_page = 20
    inlines = [OrderProductTabular,]


admin.site.register(Delivery,DeliveryAdmin)
admin.site.register(Payment)
admin.site.register(OrderProduct)
admin.site.register(PaymentMethod)
