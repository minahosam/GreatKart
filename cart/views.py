from django.shortcuts import render,redirect
from main.models import *
from .models import *
from django.contrib.auth.decorators import login_required
from delivery.models import *

# Create your views here.

def cart_session(request):
    session = request.session.session_key
    if not session:
        session = request.session.create()
    return session

def add_cart(request,pk):
    req_product = Product.objects.get(pk=pk)
    current_user = request.user
    if current_user.is_authenticated:
        variations = []
        if request.POST:
            for i in request.POST:
                key = i 
                value = request.POST[key]
                try:
                    global product_variation
                    product_variation = Variation.objects.get(product=req_product,variation_cat__iexact=key,variation_value__iexact=value)
                    print(product_variation.id)
                    variations.append(product_variation)
                except:
                    pass
        print('---')
        # print(variations.id)
        try:
            cart = Order.objects.filter(user=current_user,order__item__pk=req_product.id)
            if cart:
                    cart = Order.objects.filter(user=current_user,order__item__pk=req_product.id).first()
                    # cart = Order.objects.filter(user=current_user,order__item__pk=req_product.id,order__item_variation__pk=product_variation.id).first()
            else:
                cart = Order.objects.create(
                cart_id=cart_session(request),
                transaction_id=cart_session(request),
                user = current_user
            )
            cart.save()

            # print(cart)
        except Order.DoesNotExist:
            cart = Order.objects.create(
                cart_id=cart_session(request),
                transaction_id=cart_session(request),
                user = current_user
            )
            cart.save()
        is_product_exist = OrderItem.objects.filter(item=req_product,items=cart).exists()
        if is_product_exist:
            is_product_exist = OrderItem.objects.filter(item=req_product,items=cart)
            print('-')
            print(is_product_exist)
            print('--------------------------------')
            # print('1')
            exist_var = []
            id = []
            for var in is_product_exist:
                existing_items = var.item_variation.all()
                print(existing_items)
                print('--------------------------------')
                exist_var.append(list(existing_items))
                print(exist_var)
                print('--------------------------------')
                # print(exist_var)
                # print(variations)
                id.append(var.id)
                # print(id)
            if variations in exist_var:
                index = exist_var.index(variations)
                # print(index)
                item_id = id[index]
                cartItem = OrderItem.objects.get(id=item_id, item=req_product,items=cart)
                cartItem.quantity += 1
                cartItem.save()
            else:
                cartItem = OrderItem.objects.create(
                    item=req_product,items=cart,quantity=1
                )

                if len(variations) != 0:
                    for variant in variations:
                        cartItem.item_variation.add(variant)
                cartItem.save()
        else:
            cartItem = OrderItem.objects.create(
                item=req_product,items=cart,quantity=1
            )
            cartItem.item_variation.clear()
            if len(variations) != 0:
                for variant in variations:
                    cartItem.item_variation.add(variant)
            cartItem.save()

    else:
        variations = []
        if request.POST:
            for i in request.POST:
                key = i 
                value = request.POST[key]
                try:
                    product_variation = Variation.objects.get(product=req_product,variation_cat__iexact=key,variation_value__iexact=value)
                    # print(product_variation)
                    variations.append(product_variation)
                except:
                    pass
            
        try:
            cart = Order.objects.filter(cart_id=cart_session(request))
            if cart:
                cart = Order.objects.filter(cart_id=cart_session(request)).first()
            else:
                cart = Order.objects.create(
                cart_id=cart_session(request),
                transaction_id=cart_session(request)
            )
            cart.save()
        except Order.DoesNotExist:
            cart = Order.objects.create(
                cart_id=cart_session(request),
                transaction_id=cart_session(request)
            )
            cart.save()
        is_product_exist = OrderItem.objects.filter(item=req_product,items=cart).exists()
        if is_product_exist:
            is_product_exist = OrderItem.objects.filter(item=req_product,items=cart)
            exist_var = []
            id = []
            for var in is_product_exist:
                existing_items = var.item_variation.all()
                exist_var.append(list(existing_items))
                # print(exist_var)
                # print(variations)
                id.append(var.id)
                # print(id)
            if variations in exist_var:
                index = exist_var.index(variations)
                # print(index)
                item_id = id[index]
                cartItem = OrderItem.objects.get(id=item_id, item=req_product)
                cartItem.quantity += 1
                cartItem.save()
            else:
                cartItem = OrderItem.objects.create(
                    item=req_product,items=cart,quantity=1
                )

                if len(variations) != 0:
                    for variant in variations:
                        cartItem.item_variation.add(variant)
                cartItem.save()
        else:
            cartItem = OrderItem.objects.create(
                item=req_product,items=cart,quantity=1
            )
            cartItem.item_variation.clear()
            if len(variations) != 0:
                for variant in variations:
                    cartItem.item_variation.add(variant)
            cartItem.save()
    return redirect('cart:item')

def decrease_cart(request,pk,item_id):
    req_product = Product.objects.get(pk=pk)
    if request.user.is_authenticated:
        try:
            cart = Order.objects.filter(user=request.user,order__item__pk=req_product.id).first()
        except Order.DoesNotExist:
            pass
        cartItem = OrderItem.objects.filter(item=req_product,items=cart,pk=item_id).first()
        if cartItem.quantity > 1:
            cartItem.quantity -= 1
            cartItem.save()
        if cartItem.quantity < 1:
            cartItem.delete()
            cart.delete()
    else:
        try:
            cart = Order.objects.get(cart_id=cart_session(request))
        except Order.DoesNotExist:
            pass
        cartItem = OrderItem.objects.get(item=req_product,items=cart,pk=item_id)
        if cartItem.quantity > 1:
            cartItem.quantity -= 1
            cartItem.save()
        if cartItem.quantity < 1:
            cartItem.delete()
    return redirect('cart:item')



def cart(request,totalItem=0,total_price=0,tax=0,total=0):
    
    try:
        if request.user.is_authenticated:
            cart = Order.objects.filter(user=request.user)
            # cart = Order.objects.filter(user=request.user)
            # # print(cart)
            # for i init carts:
            cartItem = OrderItem.objects.filter( items__user=request.user)
            print(cartItem)
            # cartItem=list(cartItems)
            # # print(cartItem)

        else:
            cart = Order.objects.get(cart_id=cart_session(request))
            cartItem = OrderItem.objects.filter(items__cart_id=cart_session(request))
    except Order.DoesNotExist:
        cart = {}
        cartItem = {}
    # if cart:
    #     cartItem = OrderItem.objects.filter(items=cart)
    # else:
    #     cartItem={}
    for item in cartItem:
        totalItem = item.item.price * item.quantity
        total_price += totalItem
    tax = (2*total_price)/100
    total = total_price + tax
    context = {'cart': cartItem,'totalItem': totalItem,'tax': tax,'total': total,'totalPrice': total_price}
    return render(request,'carts/cart.html', context)

def remove_cart(request,pk,item_id):
    if request.user.is_authenticated:
        req_product = Product.objects.get(pk=pk)
        try:
            cart = Order.objects.filter(user=request.user,order__item__pk=req_product.id).first()
        except Order.DoesNotExist:
            pass
        cartItems = OrderItem.objects.all()
        cartItem = OrderItem.objects.get(item=req_product,items=cart,pk=item_id)
        cartItem.delete()
        if len(cartItems) == 0:
            cart.delete()
    else:
        try:
            cart = Order.objects.get(cart_id=cart_session(request))
        except Order.DoesNotExist:
            pass
        req_product = Product.objects.get(pk=pk)
        cartItems = OrderItem.objects.all()
        cartItem = OrderItem.objects.get(item=req_product,items=cart,pk=item_id)
        cartItem.delete()
        if len(cartItems) == 0:
            cart.delete()
    return redirect('cart:item')

@login_required(login_url='account:login')
def checkout(request,totalItem=0,total_price=0,tax=0,total=0):
    try:
        cart = Order.objects.get(cart_id=cart_session(request))
    except Order.DoesNotExist:
        cart = {}
    if cart:
        cartItem = OrderItem.objects.filter(items=cart)
    else:
        cartItem={}
    for item in cartItem:
        totalItem = item.item.price * item.quantity
    total_price += totalItem
    tax = (2*total_price)/100
    total = total_price + tax
    paymets_method = PaymentMethod.objects.all()
    print(paymets_method)
    context = {'cart': cartItem,'totalItem': totalItem,'tax': tax,'total': total,'totalPrice': total_price,'paymet':paymets_method}
    return render(request,'carts/checkout.html',context)