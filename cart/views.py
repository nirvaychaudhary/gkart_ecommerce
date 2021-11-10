from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Cart, CartItem
from store.models import Product, Variation
# Create your views here.

def _cart_id(request):
    cart = request.session.session_key #getting session from the browser
    if not cart:
        cart = request.session.create() #if there is no session available in cart then create new session for cart
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            print('key::: ',key, 'value::: ',value)

            try:
                variation = Variation.objects.get(variation_category__iexact = key, variation_value__iexact = value)
                print("variations::: ", variation)
                product_variation.append(variation)

            except:
                pass
        # return HttpResponse(color + ' ' + size)
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart = _cart_id(request)) #get the cart using  cart field present in the session
        print("Cart:::", cart)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart = _cart_id(request)
        )
    cart.save()

    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product, cart=cart)
        '''
        existing variations => getting from database
        current variation => getting from product variation list
        item_id => getting from database
        '''
        ex_var_list = []
        id = []
        for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)
        print(ex_var_list)

        if product_variation in ex_var_list:
            '''increase the cart item quantity'''
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product=product, id = item_id)
            item.quantity += 1
            item.save()
        
        else:
            item = CartItem.objects.create(product = product, quantity = 1, cart = cart)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
            # cart_item.quantity += 1
            item.save()

    else:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()

    # return HttpResponse("Product Name::: "+ str(cart_item.product) +"===>"+  "Product Quantity::: " + str(cart_item.quantity))
    return redirect('cart:cart')

def decrease_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart = _cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart:cart')

def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart:cart')

def Cart_page(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (13 * total)/100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass
    context = {
        'title': 'Cart',
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        
    }
    return render(request, 'cart/cart.html', context=context)