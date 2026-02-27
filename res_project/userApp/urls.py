from userApp import views
from django.urls import path

urlpatterns = [
    path('', views.homeView, name='homepage'),
    path('register/', views.UserRegisterView, name='registerpage'),
    path('login/', views.UserLoginView, name='loginpage'),
    path('logout/', views.UserLogoutView, name='logoutpage'),
    path('conformemail/', views.conformEmailView, name='conformemailpage'),
    path('otpvalidation/', views.optValidationView, name='otpvalidationpage'),
    # path('sendemail/', views.send_otp_email),
    path('conformpass/', views.ConformPasswordView, name='conformpasswordpage'),
    path('user_profile/', views.UserProfileView, name='userprofilepage'),
    path('edituser_profile/', views.editUserProfileView, name='edituserprofile'),
    path('update_profile_image/', views.update_profile_image, name='update_profile_image'),
]



