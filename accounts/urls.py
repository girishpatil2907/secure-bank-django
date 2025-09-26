# accounts/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Function ka naam 'signup' hai, isliye yahan bhi 'views.signup' hoga
    path('signup/', views.signup, name='signup'), 
    path('verify-otp/<str:username>/', views.verify_otp, name='verify_otp'),
    
    # Login aur logout ke liye sahi tarika
    path('login/', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]