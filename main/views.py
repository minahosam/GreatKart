from django.shortcuts import render
from .models import *
from cart.models import *
from cart.views import *
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .forms import *
from delivery.models import *


# Create your views here.
def homepage(request):
    products = Product.objects.all().filter(is_available=True)
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 6)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    context = {
        'products': pages,
    }

    return render(request, 'main/index.html', context)

def store(request,slug=None):
    products = None
    categories = None
    if slug != None:
        categories = Category.objects.get(cat_slug=slug)
        products = Product.objects.filter(product_category=categories)
        count = products.count()
    else:
        products = Product.objects.all()
        count = products.count()
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 4)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    for product in products:
        reviews = Review.objects.filter(product=product,status=True)
    context = {'products': pages, 'Count': count,'reviews': reviews}
    return render(request, 'main/store.html', context)

def detail_page(request,slug):
    required_product = Product.objects.get(slug=slug)
    try:
        cart = Order.objects.filter(cart_id=cart_session(request)).first()
        added = OrderItem.objects.filter(items=cart,item=required_product).exists()
    except Order.DoesNotExist:
        added = None
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user,product=required_product).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None
    reviews = Review.objects.filter(product=required_product,status=True)
    product_gallery = productGallery.objects.filter(product=required_product)
    context = {'product':required_product,'added':added,'orderproduct':orderproduct,'reviews':reviews,'product_gallery':product_gallery}
    return render(request, 'main/product-detail.html', context)



def Search(request):
    result = request.GET.get('search')
    search_result = Product.objects.filter(product_name__icontains=result)
    count = Product.objects.filter(product_name__icontains=result).count()
    # for one_result in search_result:
    #     single_result = Product.objects.get(id=one_result.id)
    #     cart = Order.objects.get(cart_id=cart_session(request))
    #     added = OrderItem.objects.get(items=cart,item=single_result).exists()
    #     return added
    # print(added)
    page = request.GET.get('page', 1)
    paginator = Paginator(search_result, 3)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    context = {'result': pages,'counts': count,'s':result}
    return render(request, 'main/search-result.html', context)

def reviewFunction(request,slug):
    url = request.META.get('HTTP_REFERER')
    req_product = Product.objects.get(id=slug)
    if request.method == 'POST':    
        try:
            review = Review.objects.get(product=req_product,user=request.user)
            reviewForm = ReviewForm(request.POST,instance=review)
            if reviewForm.is_valid():
                reviewForm.save()
                return redirect(url)
        except Review.DoesNotExist:
            reviewForm = ReviewForm(request.POST)
            if reviewForm.is_valid():
                form = reviewForm.save(commit=False)
                form.title = reviewForm.cleaned_data['title']
                form.review = reviewForm.cleaned_data['review']
                form.rating = reviewForm.cleaned_data['rating']
                form.user = request.user
                form.product = req_product
                form.ip = request.META.get('REMOTE_ADDR')
                form.save()
                return redirect(url)
            else:
                return redirect(url)
    return render(request, 'main/product-detail.html')