from django.urls import path
from foodApp import views


urlpatterns = [
    path('addcategory/', views.addCategory, name='addcategory'),
    path('food/', views.categoryList, name='food'),
    path('food/<int:category_id>/', views.categoryFoodList, name='foodlist'),
    path('food/detail/<int:food_id>/', views.itemDetail, name='fooddetail'),

    path('add-to-cart/<int:food_id>/', views.add_to_cart, name='addtocart'),
    path('cart/', views.CartListView, name='cart'),
    path('delete-cart/<int:food_id>/', views.deleteCartItem, name='deletecartitem'),
    path('cart_increse/<int:food_id>/', views.increase_cart, name='cartincrement'),
    path('cart_decrease/<int:food_id>/', views.decrease_cart, name='cartsdecrement'),
    
    path('checkout/', views.checkout, name='checkout'),
    path('payment-success/<int:user_id>/', views.payment_success, name='payment_success'),

    path('order/', views.orderView, name='order'),
    path('order/<int:order_id>/', views.orderDetailView, name='order_detail'),
    path('menu/', views.menuItemsView, name='menu'),
    path('reorders/<int:order_id>/', views.reorder_items, name='reorder'),
]