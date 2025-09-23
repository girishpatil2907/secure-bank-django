from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import random
from .forms import SignUpForm
from .models import UserProfile
from django.contrib import messages

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.set_password(form.cleaned_data['password'])
            user.save()

            otp_code = str(random.randint(100000, 999999))
            mpin = form.cleaned_data['mpin']
            hashed_mpin = make_password(mpin)
            
            # Update or create UserProfile
            profile, created = UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    'mpin': hashed_mpin,
                    'otp': otp_code,
                    'otp_created_at': timezone.now()
                }
            )

            subject = 'Verify your Secure Bank Account'
            message = f'Hello {user.first_name},\n\nYour OTP to verify your account is: {otp_code}\n\nThis OTP is valid for 10 minutes.\n\nThank you,\nSecure Bank Team'
            
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
                messages.success(request, 'A verification OTP has been sent to your email.')
                return redirect('verify_otp', username=user.username)
            except Exception as e:
                messages.error(request, 'Failed to send verification email. Please check your settings.')
                user.delete() # Agar email fail ho toh user delete kar dein
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def verify_otp(request, username):
    try:
        user = User.objects.get(username=username)
        profile = UserProfile.objects.get(user=user)
    except (User.DoesNotExist, UserProfile.DoesNotExist):
        messages.error(request, 'User not found. Please sign up again.')
        return redirect('signup')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        
        time_limit = profile.otp_created_at + timedelta(minutes=10)

        if profile.otp == entered_otp and timezone.now() < time_limit:
            user.is_active = True
            user.save()
            profile.otp = None
            profile.otp_created_at = None
            profile.save()
            
            login(request, user)
            messages.success(request, 'Your account has been verified successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid or expired OTP. Please try again.')
            
    return render(request, 'accounts/verify_otp.html', {'username': username})