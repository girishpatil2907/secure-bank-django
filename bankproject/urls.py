from django.contrib import admin
from django.urls import path, include
from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', accounts_views.home, name='home'),
    path('accounts/', include('accounts.urls')),
    # Hum 'bank' app ke URLs ko bhi yahan jod rahe hain
    path('', include('bank.urls')),
]