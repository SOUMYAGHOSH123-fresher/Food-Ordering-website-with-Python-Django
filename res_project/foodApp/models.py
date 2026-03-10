from django.db import models
from userApp.models import CustomUser
from restaurantApp.models import Restaurant

# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=100)
    cat_image = models.ImageField(upload_to='product_images')
    options = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class Items(models.Model):
    restaurent = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, related_name='items', null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=100)
    item_image = models.ImageField(upload_to='item_images')
    price = models.PositiveIntegerField()
    rating = models.FloatField(null=True, blank=True, default=0.0)
    quantity = models.IntegerField()
    description = models.TextField()
    is_veg = models.BooleanField(default=True)

    def __str__(self):
        return self.item_name



class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        return sum(item.product_prc for item in self.carts.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='carts')
    product = models.ForeignKey(Items, on_delete=models.CASCADE)
    product_qty= models.PositiveIntegerField(default=1)
    product_prc = models.FloatField(blank=True)

    def __str__(self):
        return self.product.item_name


class Order(models.Model):
    STATUS_CHOICES = (
        ("PROCESSING", "Processing"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    razorpay_order_id = models.CharField(max_length=200, unique=True)
    razorpay_payment_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=500, blank=True, null=True)

    total_amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    payment_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PROCESSING"
    )

    def __str__(self):
        return f"Order {self.id} - {self.user.first_name} - {self.payment_status}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orders')
    item = models.ForeignKey(Items, on_delete=models.CASCADE, related_name='orderitems')
    quantity = models.PositiveIntegerField()
    price = models.FloatField()

    @property
    def subtotal(self):
        return self.quantity * self.price
    
    def __str__(self):
        return f"OrderItem {self.item.item_name}"





