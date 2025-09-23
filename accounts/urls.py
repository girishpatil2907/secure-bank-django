from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('verify-otp/<str:username>/', views.verify_otp, name='verify_otp'),
    
    path('login/', auth_views.LoginView.as_view(
            template_name='login.html',
            redirect_authenticated_user=True
        ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]