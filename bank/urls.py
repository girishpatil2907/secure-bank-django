# bank/urls.py

from django.urls import path
from . import views
from accounts.views import home # Home view ko accounts app se import karein

urlpatterns = [
    # Root URL ab 'accounts.views.home' handle karega
    path('', home, name='home'), 
    path('dashboard/', views.dashboard, name='dashboard'),
    path('transactions/', views.transaction_history_view, name='transactions'),
    path('deposit/', views.deposit_view, name='deposit'),
    path('withdraw/', views.withdrawal_view, name='withdraw'),
    path('transfer/', views.transfer_view, name='transfer'),
    path('apply-loan/', views.loan_application_view, name='apply_loan'),
    path('pf-deposit/', views.pf_deposit_view, name='pf_deposit'),
    path('create-pf-account/', views.create_pf_account_view, name='create_pf_account'),
    path('download-csv/', views.download_transactions_csv, name='download_csv'),
    path('sip-calculator/', views.sip_calculator_view, name='sip_calculator'),
]