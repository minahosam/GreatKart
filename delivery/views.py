from django.shortcuts import render,redirect
from cart.models import *
import datetime
from .forms import *
import json
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


# Create your views here.
def placeOrder(request):
    user = request.user
    fname = request.POST['first_name']
    lname = request.POST['last_name']
    email = request.POST['email']
    phone = request.POST['phone']
    address_line_1 = request.POST['address_line_1']
    address_line_2 = request.POST['address_line_2']
    payment = request.POST['payment']
    country = request.POST['country']
    city = request.POST['city']
    state = request.POST['state']
    order_note = request.POST['order_note']
    cart = Order.objects.filter(user=user)
    pay = PaymentMethod.objects.get(payment_method=payment)
    cart_count = cart.count()
    catege = cart.first()
    cart_items = OrderItem.objects.filter(items__user=request.user)
    if cart_count == 0:
        return redirect('main:store')
    tax = 0
    grand_total = 0
    total_price = 0
    for cart_item in cart_items:
        totalItem = cart_item.item.price * cart_item.quantity
        total_price += totalItem
    tax = (2*total_price)/100
    grand_total = total_price + tax
    if request.method == 'POST':
        form = PlaceOrder(request.POST)
        print(form.errors)
        if form.is_valid():
            data = form.save(commit=False)
            data.first_name = fname
            data.last_name = lname
            data.email = email
            data.mobile_number = phone
            data.address_line_1 = address_line_1
            data.address_line_2 = address_line_2
            data.payment_type = pay
            data.city = city
            data.state = state
            data.country = country
            data.order_note = order_note
            data.user = user
            data.ip = request.META.get('REMOTE_ADDR')
            data.tax = tax
            data.order_total = grand_total
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            return redirect('place:payment')
    else:
        return redirect('cart:checkout')
    

def payments(request):
    user = request.user
    req_user = Profile.objects.get(email=user)
    order = Delivery.objects.filter(user=user,is_ordered=False).first()
    cart_items = OrderItem.objects.filter(items__user=request.user)
    tax = 0
    grand_total = 0
    total_price = 0
    for cart_item in cart_items:
        totalItem = cart_item.item.price * cart_item.quantity
        total_price += totalItem
    tax = (2*total_price)/100
    grand_total = total_price + tax
    try:
        body = json.loads(request.body)
        payment = Payment.objects.create(
            user=request.user,
            payment_id=body['transactionId'],
            payment_method=body['payment_method'],
            paid=grand_total,
            status=body['status']
        )
        payment.save()
        order.payment = payment
        order.is_ordered = True
        order.save()
        for item in cart_items:
            order_product = OrderProduct()
            order_product.order = order
            order_product.payment = payment
            order_product.user = request.user
            order_product.product = item.item
            order_product.quantity = item.quantity
            order_product.product_price = item.item.price
            order_product.ordered = order.is_ordered
            order_product.save()
            cart_ite = OrderItem.objects.get(id=item.id)
            product_variation = cart_ite.item_variation.all()
            orderProduct = OrderProduct.objects.get(id=order_product.id)
            orderProduct.variation.set(product_variation)
            orderProduct.save()
            product = Product.objects.get(id=item.item.id)
            product.stock -= item.quantity
            product.save()
        req_order = Order.objects.get(user=request.user)
        req_order.delete()
        # sending mail
        subject = "Order Completed successfully"
        message = render_to_string('orders/succesed_order.html',{
            'user': request.user,
            'order': order,
        })
        e_mail = req_user.email
        mail = EmailMessage(subject, message,to=[e_mail])
        mail.send()
        data = {
            'order_number': order.order_number,
            'transaction_id': payment.payment_id,
        }
        return JsonResponse(data)

    except json.JSONDecodeError as e:
        pass
    context = {'order':order,'cart_items':cart_items,'total':total_price,'tax':tax,'grand_total':grand_total}
    return render(request, 'orders/payment.html',context)

def complete(request):
    order_no = request.GET['orderNo']
    paymet_no = request.GET['paymentId']
    try:
        req_order = Delivery.objects.get(order_number=order_no)
        order_products = OrderProduct.objects.filter(order=req_order)
        payment = Payment.objects.get(payment_id=paymet_no)
    except Order.DoesNotExist:
        return redirect('main:home')
    context = {'order':req_order,'order_products':order_products,'payment':payment}
    return render(request, 'orders/complete.html',context)