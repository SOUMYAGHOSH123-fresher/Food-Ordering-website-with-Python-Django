from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser, Profile
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

# from django.contrib.auth import 

# Create your views here.

def homeView(request):
    return render(request, 'resAppTemp/index.html')


def UserRegisterView(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        date_of_birth = request.POST.get('dateofbirth')

        if len(fname) < 5:
            messages.warning(request, "first name is too short")
            return redirect("registerpage")

        if len(lname) < 5:
            messages.warning(request, "Last name is too short")
            return redirect("registerpage")

        if "@" not in email and "." not in email:
            messages.warning(request, "User email is invalid")
            return redirect("registerpage")
        
        if len(password) < 5 and len(password) > 8:
            messages.warning(request, 'Your password must be 5–8 characters long.')
            return redirect('registerpage')
        
        if not any(char.isupper() for char in password):
            messages.warning(request, "password must have a UpperCase")
            return redirect("registerpage")
        
        if not any(char.isalpha() for char in password):
            messages.warning(request, "password must have lowercase letter")
            return redirect("registerpage")

        if not any(char.isdigit() for char in password):
            messages.warning(request, "password must have lowercase letter")
            return redirect("registerpage")        
       
    
        user = CustomUser(
            first_name=fname, 
            last_name=lname, 
            email=email,
            date_of_birth=date_of_birth
            )
        user.set_password(password)
        user.save()
        messages.success(request, 'User registration Successfully.')
        print('user register successfully.')
        return redirect('loginpage')

    return render(request, 'userAppTemp/user_register.html')


def UserLoginView(request):
    user = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if '@' not in email or '.' not in email:
            messages.warning(request, 'Your password is not valid')
            return redirect('loginpage')
        
        if len(password) < 5 and len(password) > 8:
            messages.warning(request, 'Your password must be 5–8 characters long.')
            return redirect('loginpage')
 
                
        if CustomUser.objects.filter(email=email).exists():
            user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'User login successfully.')
            print('login successfully.')
            return redirect('homepage')        
        else:
            messages.warning(request, 'Login user failed.')
            print('Login user failed.')
            return redirect('loginpage')

    return render(request, 'userAppTemp/user_login.html')


def UserLogoutView(request):
    logout(request)
    return redirect('homepage')


def conformEmailView(request):
    if request.method == "POST":
        conform_email = request.POST.get('conform_email')
        # print(conform_email)

        if '@' not in conform_email and '.' not in conform_email:
            messages.warning(request, 'Invalid email enter')
            return redirect('conformemailpage')            
        
        user = CustomUser.objects.filter(email=conform_email)
        print(user)
        
        if user.exists():
            u = CustomUser.objects.get(email=conform_email)
            send_otp_email(u.email, u)
            return redirect(f'/otpvalidation?email={u.email}')
        else:
            messages.warning(request, 'Email not found')
            return render(request, 'userAppTemp/conform_email.html')
    return render(request, 'userAppTemp/conform_email.html')



def send_otp_email(email, user):
    
    user.generateOtp()
    user.save()
    # print(email, user.otp)
    # print(user)
    subject = 'Your OTP for Verification'
    message = f'Hi {user.first_name}, your OTP for Validation is {user.otp}. It is valid for 10 minutes.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, 'gsoumya671@gmail']
    send_mail(subject, message, email_from, recipient_list)

    # return render(request, 'userAppTemp/conform_email.html')


def optValidationView(request):
    email = request.GET.get('email')
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        print(otp_entered)
        

        user = CustomUser.objects.get(email=email)
        print(user,'--------------')
        print(user.otp)


        if '@' not in email and '.' not in email:
            messages.warning(request, 'Invalid Email.')
            return redirect('otpvalidationpage')

        if len(otp_entered) < 6:
            messages.warning(request, 'Length of otp is too short.')
            return redirect('otpvalidationpage')

        if user.otp == otp_entered and user.otp_expiry > timezone.now():
            user.is_verified = True
            user.save()
            messages.success(request, 'Otp successufully')
            print(email, user.otp)
            return redirect(f'/conformpass?email={email}')
    
    return render(request, 'userAppTemp/otpValidationForm.html', {'email': email})


def ConformPasswordView(request):
    conform_email = request.GET.get('email')
    if request.method == 'POST':
        password1 = request.POST.get('new_password')
        password2 = request.POST.get('confor_password')
        conform_email = request.GET.get('email')
        # print(conform_email)

        if len(password1) < 5 and len(password1) > 8:
            messages.warning(request, 'Your new password must be 5–8 characters long.')
            return redirect('conformpasswordpage')

        if len(password2) < 5 and len(password2) > 8:
            messages.warning(request, 'Your conform password must be 5–8 characters long.')
            return redirect('conformpasswordpage')

        if not any(char.isupper() for char in password1):
            messages.warning(request, "password must have an UpperCase")
            return redirect("conformpasswordpage")
        
        if not any(char.isupper() for char in password2):
            messages.warning(request, "password must have an UpperCase")
            return redirect("conformpasswordpage")
        
        if not any(char.isalpha() for char in password1):
            messages.warning(request, "password must have lowercase letter")
            return redirect("conformpasswordpage")
        
        if not any(char.isalpha() for char in password2):
            messages.warning(request, "password must have lowercase letter")
            return redirect("conformpasswordpage")

        if not any(char.isdigit() for char in password1):
            messages.warning(request, "password must have lowercase letter")
            return redirect("conformpasswordpage")
        
        if not any(char.isdigit() for char in password2):
            messages.warning(request, "password must have lowercase letter")
            return redirect("conformpasswordpage")

        if password1 and password2 and password1 == password2:
            try:
                user = CustomUser.objects.get(email=conform_email)
                user.password = make_password(password1)  # convert to hash_passowrd
                user.save()
                messages.success(request, 'Password changes successfully.')
                # print(user.password)

                return redirect('loginpage')
            
            except CustomUser.DoesNotExist:
                messages.warning(request, 'Email not found.')
                return render(request, 'userAppTemp/conform_pass.html')
        
        else:
            messages.warning(request, 'Password doen not match')
            return render(request, 'userAppTemp/conform_pass.html')
        
    return render(request, 'userAppTemp/conform_pass.html', {'email': conform_email})



def UserProfileView(request):
    # profile = Profile.objects.get(user=request.user)
    if not request.user.is_authenticated:
        return redirect('/login')

    profile, created = Profile.objects.get_or_create(
        user = request.user,
        defaults={"bio": f"Hello, {request.user.first_name}"}
    )
    context = {'profile': profile}
    return render(request, 'userAppTemp/user_profile_page.html', context)


def editUserProfileView(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    profile, created = Profile.objects.get_or_create(
        user = request.user,
        defaults={"bio": f"Hello, I am food lover"}
    )
    # print("profile", profile)

    # print(profile)
    if request.method == "POST":
        fname = request.POST.get('fname', profile.user.first_name)
        lname = request.POST.get('lname', profile.user.last_name)
        phone = request.POST.get('phone', profile.user.phone)
        bio = request.POST.get('bio', profile.bio)
        location = request.POST.get('location', profile.location)

        print('bio', len(bio), "profile bio", profile.bio)
        print(bio, location)

        if len(fname) < 6:
            messages.warning(request, "The first name must be of 6 chracters")
            return redirect('edituserprofile')

        if len(lname) < 5:
            messages.warning(request, "The last name must be of 6 chracters")
            return redirect('edituserprofile')


        if len(str(phone)) != 10:
            messages.warning(request, "Phone number must be 10 digits")
            return redirect('edituserprofile')

        if len(bio) <= 0:
            messages.warning(request, "Your bio must have at least 5 character")
            return redirect('edituserprofile')

        if len(location) < 4:
            messages.warning(request, "Your location must have at least 5 character")
            return redirect('edituserprofile')

        
        profile.user.phone = phone
        profile.user.first_name = fname
        profile.user.last_name = lname
        profile.user.save()

        # profile, created = Profile.objects.update_or_create(
        #     user = request.user,
        #     bio = request.POST.get('bio'),
        #     location = request.POST.get('location'),
        #     defaults={"bio": f"Hello, I am {request.user.first_name}"}
        # )

        profile.bio = bio
        profile.location = location
        profile.save()

        messages.success(request, "User Profile Update Successfuly.")
        return redirect('userprofilepage')

    return render(request, 'userAppTemp/edituser_profile.html', {'profile': profile})



def update_profile_image(request):

    if not request.user.is_authenticated:
        return redirect('/login')

    if request.method == 'POST' and request.FILES.get('profile_image'):
        profile = request.user.profile
        print(request.FILES.get('image'))
        profile.profile_image = request.FILES['profile_image']
        profile.save()
        return redirect('userprofilepage')
    
    return render(request, 'userAppTemp/user_profile.html')



