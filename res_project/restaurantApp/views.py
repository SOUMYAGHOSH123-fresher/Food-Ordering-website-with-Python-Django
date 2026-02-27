from django.shortcuts import render
from .models import Restaurant
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# Create your views here.
def resturentView(request):
    restaurants = Restaurant.objects.all()[:10]
    return HttpResponse('restaurant page')


def restaurantDetailView(request, res_id):
    restaurant = get_object_or_404(Restaurant, id=res_id)
    return render(request, 'restaurantTemp/restaurant_detail.html', {'restaurant': restaurant})
