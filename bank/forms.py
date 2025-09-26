# bank/forms.py

from django import forms
from .models import LoanApplication

class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.01, widget=forms.NumberInput(attrs={'class': 'form-control form-control-lg'}))
    mpin = forms.CharField(widget=forms.PasswordInput(attrs={'maxlength': '4', 'class': 'form-control form-control-lg'}), label="4-Digit MPIN", max_length=4)

class WithdrawalForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.01, widget=forms.NumberInput(attrs={'class': 'form-control form-control-lg'}))
    mpin = forms.CharField(widget=forms.PasswordInput(attrs={'maxlength': '4', 'class': 'form-control form-control-lg'}), label="4-Digit MPIN", max_length=4)

class TransferForm(forms.Form):
    recipient_account_number = forms.CharField(label="Recipient's Account Number", max_length=10, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.01, widget=forms.NumberInput(attrs={'class': 'form-control form-control-lg'}))
    mpin = forms.CharField(widget=forms.PasswordInput(attrs={'maxlength': '4', 'class': 'form-control form-control-lg'}), label="Your 4-Digit MPIN", max_length=4)

class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        fields = ['loan_type', 'amount_required', 'monthly_income']
        widgets = {
            'loan_type': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'amount_required': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'e.g., 500000'}),
            'monthly_income': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'e.g., 75000'}),
        }

class PFDepositForm(forms.Form):
    amount = forms.DecimalField(label="Amount to Deposit in PF", max_digits=12, decimal_places=2, min_value=100.00, widget=forms.NumberInput(attrs={'class': 'form-control form-control-lg'}))
    mpin = forms.CharField(widget=forms.PasswordInput(attrs={'maxlength': '4', 'class': 'form-control form-control-lg'}), label="Your 4-Digit MPIN to Confirm", max_length=4)