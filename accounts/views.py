from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.models import auth
from .forms import *
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from cart.models import *
from cart.views import *
import requests
from delivery.models import *

# Create your views here.
# def register(request):
#     if request.method == 'POST':
#         fname =request.POST.get('fname')
#         lname = request.POST.get('lname')
#         email = request.POST.get('email')
#         gender = request.POST.get('gender')
#         city = request.POST.get('city')
#         country = request.POST.get('country')
#         password = request.POST.get('password')
#         password_confirmation = request.POST.get('password2')
#         phone = request.POST.get('phone')
#         if len(password) < 6:
#             messages.error(request,'Password must be at least 6 characters')
#         if password != password_confirmation:
#             messages.error(request,'Password did not match')
#         if Profile.objects.filter(email=email).exists:
#             messages.error(request,'email already exists')
#         country_get = Country.objects.get(name=country)
#         new_member = Profile.objects.create_user(first_name=fname, last_name=lname,email=email,gender_type=gender,city=city,
#                                                  country=country_get,password=password,username=email.split('@')[0],mobile_number=phone)
#         if new_member:
#             return redirect('account:login')
#     else:
#         countries = Country.objects.all()
#         context = {'countries': countries}
#         return render(request,'pages/register.html', context)

def register(request):
    if request.method == 'POST':
        form = registerationForm(request.POST)
        gender = request.POST.get('gender')
        city = request.POST.get('city')
        country = request.POST.get('country')
        if form.is_valid():
            print('2')
            fname = form.cleaned_data['first_name']
            lname = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['mobile_number']
            password = form.cleaned_data['password']
            password_confirmation = form.cleaned_data['confirm_password']
        if len(password) < 6:
            messages.error(request,'Password must be at least 6 characters')
        if password != password_confirmation:
            messages.error(request,'Password did not match')
        if Profile.objects.filter(email=email).exists:
            messages.error(request,'email already exists')
            country_get = Country.objects.get(name=country)
            new_member = Profile.objects.create_user(first_name=fname, last_name=lname,email=email,gender_type=gender,city=city,
                                                    country=country_get,password=password,username=email.split('@')[0],mobile_number=phone)
            new_member.save()
            # sending mail
            site = get_current_site(request)
            subject = "Please Activate Your Account"
            message = render_to_string('pages/activate_account.html',{
                'user': new_member,
                'site': site,
                'uid': urlsafe_base64_encode(force_bytes(new_member.pk)),
                'token': default_token_generator.make_token(new_member)
            })
            mail = EmailMessage(subject, message,to=[email])
            mail.send()
            if new_member:
                return redirect('account:login')
        else:
            print(form.errors)
            
    else:
        form = registerationForm()
    countries = Country.objects.all()
    context = {'form': form,'countries': countries}
    return render(request,'pages/register.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user:
            try:
                cart1 = Order.objects.get(cart_id=cart_session(request))
                cart1.save()
                cartItem1 = OrderItem.objects.filter(items=cart1)
                
                variations = []
                for item in cartItem1:
                    items = item.item_variation.all()
                    
                    variations.append(list(items))
                    
                # cart2 = Order.objects.get(user=user)
                # 
                cartItem2 = OrderItem.objects.filter(items__user=user)
                
                id = []
                exist = []
                for item in cartItem2:
                    items = item.item_variation.all()
                    
                    exist.append(list(items))
                    
                    id.append(item.id)
                    
                for pr in variations:
                    if pr in exist:
                        
                        index = exist.index(pr)
                        
                        print(index)
                        item_id = id[index]
                        print('2')
                        print(item_id)
                        cart3 = Order.objects.get(cart_id=cart_session(request))
                        # print(cart)
                        item = OrderItem.objects.get(id=item_id)
                        item.quantity += 1
                        item.save()
                        # cart1.user = user
                        # cart1.save()
                        cart3 = cart1
                        cart3.delete()
                    else:
                        cart = Order.objects.get(cart_id=cart_session(request))
                        print(cart)
                        if cart:
                            cart.user = user
                            cart.save()
            except Order.DoesNotExist:
                print("e")
                pass    
        if user:
            auth.login(request,user)
            messages.success(request,'login successful')
            url = request.META.get('HTTP_REFERER')
        try:
            querry = requests.utils.urlparse(url).query
            params = dict(x.split('=') for x in querry.split('&'))
            if 'next' in params:
                nextpage = params['next']
                return redirect (nextpage)
        except:
            return redirect('account:login')
            # return redirect('main:store')
        
        else:
            messages.error(request,'login failed')
            return redirect('account:login')
    else:
        return render(request,'pages/login.html')
    
def logout(request):
    auth.logout(request)
    messages.success(request,'logout successful')
    return redirect('main:store')

def activate(request,uid,token):
    try:
        uid64 =  urlsafe_base64_decode(uid).decode()
        # user = Profile.objects.get(pk=uid64)
        user = Profile._default_manager.get(pk=uid64)
    except(TypeError, ValueError, OverflowError, Profile.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        user .is_active = True
        user.save()
        messages.success(request,'activate successful')
        
    else:
        messages.error(request,'activate failed')
        return redirect('account:register')

@login_required    
def dashboard(request):
    orders = Delivery.objects.filter(user=request.user,is_ordered=True)
    order_count = orders.count()
    context = {'orders_count': order_count}
    return render(request, 'pages/dashboard.html', context)

def reset_pass(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Profile.objects.get(email=email)
            site = get_current_site(request)
            subject = 'please reset your password'
            message = render_to_string('pages/reset_password.html',{
                'user': user,
                'site': site,
                'uid':urlsafe_base64_encode(force_bytes(user.id)),
                'token':default_token_generator.make_token(user),
            })
            mail = EmailMessage(subject,message,to=[email])
            mail.send()
            # messages.success(request,'mail sent to reset password')
        except Profile.DoesNotExist:
            messages.error(request,'email is not found')
            return redirect('account:register')

    return render(request,'pages/reset_pass.html')

def reset(request,uid,token):
    try:
        uid64 = urlsafe_base64_decode(uid).decode()
        user = Profile.objects.get(pk=uid64)
    except(TypeError, ValueError, OverflowError, Profile.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid64
        messages.success(request,'please change your password')
        return redirect('account:change_password')
    else:
        messages.error(request,'something went wrong')
        return redirect('account:login')
    
def change_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Profile.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'password changed successfully')
            return redirect('account:login')
        else:
            messages.error(request,'password does not match!')
            return redirect('account:change_password')

    return render(request, 'pages/change_password.html')

def my_orders(request):
    order = Delivery.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    context={'orders': order}
    return render(request, 'pages/my_orders.html',context)

def update_profile(request):
    main_profile = Profile.objects.get(email=request.user)
    if request.method == 'POST':
        
        form = profileForm(request.POST,request.FILES,instance=main_profile)
        if form.is_valid():
            form.save()
    else:
        form = profileForm(instance=request.user)
    context={'form':form,'profile':main_profile}
    return render(request,'pages/edit_profile.html',context)

def changePassword(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        user = Profile.objects.get(email=request.user)
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
            else:
                messages.error(request,'your current password is incorrect')
        else:
            messages.error(request,'your new password and confirm_password need to be the same')
    return render(request,'pages/changePassword.html')

def order_details(request,orderNo):
    order = Delivery.objects.get(order_number__exact=orderNo)
    order_detail = OrderProduct.objects.filter(order=order)
    context={'order': order,'order_detail': order_detail}
    return render(request,'pages/orderDetails.html',context)