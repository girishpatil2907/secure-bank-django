from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('deposit/', views.deposit_view, name='deposit'),
    path('withdrawal/', views.withdrawal_view, name='withdrawal'),
    path('download-csv/', views.download_transactions_csv, name='download_csv'),
    path('transfer/', views.transfer_view, name='transfer'),
    path('apply-loan/', views.loan_application_view, name='apply_loan'),
    path('sip-calculator/', views.sip_calculator_view, name='sip_calculator'),
    path('transactions/', views.transaction_history_view, name='transactions'),
    path('create-pf/', views.create_pf_account_view, name='create_pf'),
    path('pf-deposit/', views.pf_deposit_view, name='pf_deposit'),
]