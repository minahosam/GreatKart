from .models import *
from .views import *

def cart_count(request):
    count = 0
    user=request.user
    if 'admin' in request.path:
        pass
    else:
        try:
            cart = Order.objects.filter(cart_id=cart_session(request))
            if user.is_authenticated:
                cartf = Order.objects.filter(user=user)
                for i in cartf:
                    cartItem = OrderItem.objects.filter(items=i)
                    for c in cartItem:
                        count += c.quantity
            else:
                cartItem = OrderItem.objects.filter(items=cart[:1])
                for item in cartItem:
                    count += item.quantity
        except Order.DoesNotExist:
            count = 0
    return {'COUNT': count}