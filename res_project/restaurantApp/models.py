from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=200)
    price = models.FloatField()
    address = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default='0.0')
    description = models.TextField(blank=True, null=True)
    res_phone = models.CharField(max_length=15)
    res_image = models.ImageField(upload_to='restaurants/')
    is_open = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.restaurant_name
    


