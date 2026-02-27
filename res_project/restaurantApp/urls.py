from django.urls import path
from restaurantApp import views




urlpatterns = [
    path('restaurant/', views.resturentView, name='restaurant'),
    path('restaurant/<int:res_id>/', views.restaurantDetailView, name='restaurant_detail'),
]