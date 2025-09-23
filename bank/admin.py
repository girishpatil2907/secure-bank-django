from django.contrib import admin
from .models import Account, Transaction, LoanApplication, PFAccount
from decimal import Decimal

class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'loan_type', 'amount_required', 'status', 'application_date', 'is_disbursed')
    list_editable = ('status',)
    list_filter = ('status', 'loan_type')
    search_fields = ('user__username',)
    readonly_fields = ('user', 'loan_type', 'amount_required', 'monthly_income', 'application_date', 'is_disbursed')

    def save_model(self, request, obj, form, change):
        if obj.status == 'APPROVED' and not obj.is_disbursed:
            try:
                user_account = Account.objects.get(user=obj.user)
                loan_amount = Decimal(obj.amount_required)
                user_account.balance += loan_amount
                user_account.save()
                Transaction.objects.create(
                    account=user_account,
                    transaction_type='DEPOSIT',
                    amount=loan_amount,
                    description=f'{obj.get_loan_type_display()} amount disbursed'
                )
                obj.is_disbursed = True
            except Account.DoesNotExist:
                self.message_user(request, "Error: Could not find bank account for this user. Disbursement failed.", level='error')
        super().save_model(request, obj, form, change)

admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(LoanApplication, LoanApplicationAdmin)
admin.site.register(PFAccount)