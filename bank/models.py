from django.db import models
from django.contrib.auth.models import User
import random

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=10, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = str(random.randint(1000000000, 9999999999))
        super().save(*args, **kwargs)

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
        ('TRANSFER', 'Transfer'),
    ]
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=100, default='N/A')

    def __str__(self):
        return f'{self.transaction_type} of {self.amount} for {self.account.user.username}'

class LoanApplication(models.Model):
    LOAN_TYPE_CHOICES = [('PERSONAL', 'Personal Loan'), ('HOME', 'Home Loan'), ('CAR', 'Car Loan')]
    STATUS_CHOICES = [('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loan_applications')
    loan_type = models.CharField(max_length=10, choices=LOAN_TYPE_CHOICES)
    amount_required = models.DecimalField(max_digits=12, decimal_places=2)
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    application_date = models.DateTimeField(auto_now_add=True)
    is_disbursed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.get_loan_type_display()} - {self.status}'

class PFAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pf_account')
    pf_account_number = models.CharField(max_length=15, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pf_account_number:
            self.pf_account_number = f'PF-{random.randint(1000000000, 9999999999)}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username}\'s PF Account'