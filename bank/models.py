# bank/models.py

from django.db import models
from django.contrib.auth.models import User
import random

def generate_account_number():
    return ''.join([str(random.randint(0, 9)) for _ in range(10)])

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    account_number = models.CharField(max_length=10, unique=True, default=generate_account_number)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.account_number}'

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
        ('TRANSFER', 'Transfer'),
    )
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.transaction_type} of {self.amount} for {self.account.user.username}'
# bank/models.py

class LoanApplication(models.Model):
    LOAN_TYPES = (
        ('PERSONAL', 'Personal Loan'),
        ('HOME', 'Home Loan'),
        ('CAR', 'Car Loan'),
    )
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES)
    amount_required = models.DecimalField(max_digits=12, decimal_places=2)
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    application_date = models.DateTimeField(auto_now_add=True)
    is_disbursed = models.BooleanField(default=False) # <-- YEH NAYI LINE ADD KAREIN

    def __str__(self):
        return f'Loan for {self.user.username} - {self.status}'
    
class PFAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pf_account')
    pf_account_number = models.CharField(max_length=12, unique=True, default=lambda: f'PF{generate_account_number()}')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'PF Account for {self.user.username}'