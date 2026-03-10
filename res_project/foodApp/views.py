from django.shortcuts import render, redirect
from .models import Category, Items, Cart, CartItem, Order, OrderItem
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from restaurantApp.models import Restaurant
from userApp.models import CustomUser
import razorpay


# Create your views here.
def categoryList(request):
    categories = Category.objects.prefetch_related('items')
    print(categories)
    restaurants = Restaurant.objects.prefetch_related('items').order_by('-created_at')[:3]
    context={'categories': categories, 'restaurants': restaurants}
    return render(request, 'resAppTemp/food.html', context)


def addCategory(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        image = request.POST.get('image')
        option = request.POST.get('options')

        c = Category(category=category, cat_image=image, options=option)
        c.save()
        return redirect('addcategory')

    return render(request, 'resAppTemp/addcategory.html')


def categoryFoodList(request, category_id):
    cart = None
    cart_items = []

    search = request.GET.get('search', "").strip()
    # print(search)

    try:
        category = Category.objects.get(id=category_id)

        foods = Items.objects.filter(category=category)
        # print("category", category)
        if search:
            foods = Items.objects.filter(category=category ,item_name__icontains=search)
                   

    except Category.DoesNotExist:
        messages.warning(request, "Category item Not present")    
        foods = []
        category=None
           

    context = {
        'foods': foods, 
        'category': category, 
        'search':search
        }
    return render(request, 'resAppTemp/food_collection.html', context)


def itemDetail(request, food_id):
    food = get_object_or_404(Items, id=food_id)
    # print(food)
    food_items = Items.objects.filter(category=food.category).exclude(id=food.id)
    context={'food': food, 'food_items': food_items}
    return render(request, 'resAppTemp/food_detail_page.html', context)


def menuItemsView(request):
    foods = Items.objects.select_related('category').order_by('-price')
    return render(request, 'resAppTemp/menu.html', {'foods': foods})


# ----------------   cart related logincs  --------------------

def CartListView(request):
    cart=[]
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    # print(cart.user)
    if not created:
        cart_items = cart.carts.select_related('product')
        total_price = sum(item.product.price * item.product_qty for item in cart_items)
        total_items = sum(item.product_qty for item in cart_items)
        # print("total_items", total_items)
    else:
        cart_items = []
        total_price = 0
        total_items = 0
    # print(total_price)
    context = {'cart': cart, 'cart_items': cart_items, 'total': total_price, 'total_items': total_items}
    return render(request, 'resAppTemp/cart.html', context)


def add_to_cart(request, food_id):
    if not request.user.is_authenticated:
        return redirect('/login')

    food = get_object_or_404(Items, id=food_id)

    cart, created = Cart.objects.get_or_create(user=request.user)
    # print(cart)

    cart_item, create_item = CartItem.objects.get_or_create(
        product=food,
        cart=cart,
        defaults={
            'product_qty':1,
            'product_prc': food.price
        })

    # if item already exist
    if not create_item:
        cart_item.product_qty += 1
        cart_item.product_prc = food.price * cart_item.product_qty
        cart_item.save()

    return redirect('cart')


def increase_cart(request, food_id):
    if not request.user.is_authenticated:
        return redirect('/login')

    food = get_object_or_404(Items, id=food_id)
    cart = get_object_or_404(Cart, user=request.user)

    cart_item = get_object_or_404(CartItem, product=food, cart=cart)

    if cart_item.product_qty < 3:
        cart_item.product_qty += 1
        cart_item.product_prc = food.price * cart_item.product_qty
        cart_item.save()

    return redirect('cart')


def decrease_cart(request, food_id):
    if not request.user.is_authenticated:
        return redirect('/login')

    food = get_object_or_404(Items, id=food_id)
    cart = get_object_or_404(Cart, user=request.user)

    cart_item = get_object_or_404(CartItem, product=food, cart=cart)

    if cart_item.product_qty > 1:
        cart_item.product_qty -= 1
        cart_item.product_prc = food.price * cart_item.product_qty
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')


def deleteCartItem(request, food_id):
    food = get_object_or_404(Items, id=food_id)
    cart = get_object_or_404(Cart, user=request.user)

    cart_item = get_object_or_404(CartItem, product=food, cart=cart)
    
    cart_item.delete()
    return redirect('cart')


@login_required(login_url='loginpage')
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    # print('cart', cart.user)

    if not cart or cart.carts.count() == 0:
        messages.error(request, "No active cart found")
        print('no active cart')
        return redirect("cart")

    items = cart.carts.select_related('product').all()
    total = cart.total

    if total <= 0:
        messages.error(request, "Your cart is empty")
        print('Your cart is empty')
        return redirect("cart")

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    payment = client.order.create({
        "amount": int(total * 100),
        "currency": "INR",
        "payment_capture": 1
    })

    print('payment ID', payment['id'])
    print(payment)
  

    callback_url = request.build_absolute_uri(
        reverse("payment_success", args =[request.user.id])
    )
    callback_url = callback_url.replace('https://', 'http://') 
    print(f"Callback URL: {callback_url} ----------")
    
    

    return render(request, "resAppTemp/checkout.html", {
        # "cart": cart,
        "items": items,
        "total": total,
        "payment": payment,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "callback_url": callback_url
    })
    

from django.db import transaction

@csrf_exempt
def payment_success(request, user_id):
    # print(f"!!! SUCCESS VIEW ACCESSED !!! ID: {id} Method: {request.method}")

    if request.method != "POST":
        return redirect("cart")

    print("POST DATA:", request.POST)

    razorpay_payment_id = request.POST.get("razorpay_payment_id")
    razorpay_order_id = request.POST.get("razorpay_order_id")
    razorpay_signature = request.POST.get("razorpay_signature")
    # print(razorpay_signature,'-------razorpay_signature-------')


    if not razorpay_payment_id:
        messages.error(request, "Payment failed or cancelled")
        print('payment failed')
        return redirect("cart")


    if not razorpay_order_id:
        messages.error(request, "Payment failed or cancelled")
        print('payment failed')
        return redirect("cart")


    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    try:
        print("----------")
        client.utility.verify_payment_signature({
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature
        })

    
    except razorpay.errors.SignatureVerificationError:
        messages.error(request, "Payment verification failed")
        return redirect("cart")


    try:
        current_user = CustomUser.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "User session lost.")
        return redirect("cart")

    cart = Cart.objects.filter(user=current_user).first()
    print(cart)
    cart_items = list(cart.carts.select_related("product"))

    with transaction.atomic():
        order = Order.objects.create(
            user = current_user,
            razorpay_order_id = razorpay_order_id,
            razorpay_payment_id = razorpay_payment_id,
            razorpay_signature = razorpay_signature,
            total_amount = cart.total,
            payment_status = 'SHIPPED'
        )

        # Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order = order,
                item = item.product,
                quantity = item.product_qty,
                price = item.product.price
            )

        # clear the cart
        cart.carts.select_related("product").delete()

    return render(request, "resAppTemp/payment_success.html", {'order': order}) 


def orderView(request):
    orders = []

    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).prefetch_related("orders").order_by('-created_at')
        # print("orders", orders)
        
    return render(request, 'resAppTemp/order.html', {'orders': orders})


def orderDetailView(request, order_id):
    if not request.user.is_authenticated:
        return redirect('/login')

    order = get_object_or_404(
        Order.objects.prefetch_related('orders'),
        id=order_id,
        user = request.user
    )
    # orderitems = order.orders
    return render(request, 'resAppTemp/order_detail.html', {'order': order})


def reorder_items(request, order_id):
    if not request.user.is_authenticated:
        return redirect('/login')

    try:
        order = Order.objects.get(id=order_id, user=request.user)
        # print("Order Id", order.id)
    
    except Order.DoesNotExist:
        messages.error(request, "Order Item lost.")
        return redirect("order")
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    order_items = list(order.orders.select_related('item'))
    # print(order_items)

    for food in order_items:
        cart_item, create_item = CartItem.objects.get_or_create(
            cart=cart,
            product=food.item,
            product_qty = food.quantity,
            product_prc = food.price
        )


    return redirect('cart')



