from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.http import HttpResponse
from django.core.paginator import Paginator
import csv
from .models import Account, Transaction, LoanApplication, PFAccount
from accounts.models import UserProfile
from .forms import DepositForm, WithdrawalForm, TransferForm, LoanApplicationForm, PFDepositForm
from decimal import Decimal

@login_required
def dashboard(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    account = Account.objects.get(user=request.user)
    loan_applications = LoanApplication.objects.filter(user=request.user).order_by('-application_date')
    try:
        pf_account = PFAccount.objects.get(user=request.user)
    except PFAccount.DoesNotExist:
        pf_account = None
    context = {
        'account': account,
        'loan_applications': loan_applications,
        'pf_account': pf_account,
        'active_page': 'dashboard',
    }
    return render(request, 'bank/dashboard.html', context)

@login_required
def transaction_history_view(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    account = Account.objects.get(user=request.user)
    transaction_list = Transaction.objects.filter(account=account).order_by('-timestamp')
    paginator = Paginator(transaction_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'account': account,
        'page_obj': page_obj,
        'active_page': 'transactions',
    }
    return render(request, 'bank/transactions.html', context)

@login_required
def deposit_view(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            mpin = form.cleaned_data['mpin']
            try:
                account = request.user.account
                user_profile = request.user.userprofile
                if check_password(mpin, user_profile.mpin):
                    account.balance += Decimal(amount)
                    account.save()
                    Transaction.objects.create(account=account, transaction_type='DEPOSIT', amount=amount, description='Self Deposit')
                    messages.success(request, f'₹{amount} has been deposited successfully!')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Invalid MPIN. Please try again.')
            except (Account.DoesNotExist, UserProfile.DoesNotExist):
                messages.error(request, 'Your account profile is not set up correctly.')
    else:
        form = DepositForm()
    context = {'form': form, 'account': request.user.account, 'active_page': 'deposit'}
    return render(request, 'bank/deposit.html', context)

@login_required
def withdrawal_view(request):
    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            mpin = form.cleaned_data['mpin']
            try:
                account = request.user.account
                user_profile = request.user.userprofile
                if check_password(mpin, user_profile.mpin):
                    if account.balance >= amount:
                        account.balance -= amount
                        account.save()
                        Transaction.objects.create(account=account, transaction_type='WITHDRAWAL', amount=amount, description='Self Withdrawal')
                        messages.success(request, f'₹{amount} has been withdrawn successfully!')
                        return redirect('dashboard')
                    else:
                        messages.error(request, 'Insufficient balance.')
                else:
                    messages.error(request, 'Invalid MPIN. Please try again.')
            except (Account.DoesNotExist, UserProfile.DoesNotExist):
                messages.error(request, 'Your account profile is not set up correctly.')
    else:
        form = WithdrawalForm()
    context = {'form': form, 'account': request.user.account, 'active_page': 'withdrawal'}
    return render(request, 'bank/withdrawal.html', context)

@login_required
def transfer_view(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            recipient_account_number = form.cleaned_data['recipient_account_number']
            amount = form.cleaned_data['amount']
            mpin = form.cleaned_data['mpin']
            try:
                sender_account = request.user.account
                user_profile = request.user.userprofile
                if not check_password(mpin, user_profile.mpin):
                    messages.error(request, 'Invalid MPIN. Please try again.')
                    return render(request, 'bank/transfer.html', {'form': form, 'account': sender_account, 'active_page': 'transfer'})
                recipient_account = Account.objects.get(account_number=recipient_account_number)
                if sender_account == recipient_account:
                    messages.error(request, "You cannot transfer money to your own account.")
                    return render(request, 'bank/transfer.html', {'form': form, 'account': sender_account, 'active_page': 'transfer'})
                if sender_account.balance < amount:
                    messages.error(request, 'Insufficient balance.')
                    return render(request, 'bank/transfer.html', {'form': form, 'account': sender_account, 'active_page': 'transfer'})
                sender_account.balance -= amount
                recipient_account.balance += amount
                sender_account.save()
                recipient_account.save()
                Transaction.objects.create(account=sender_account, transaction_type='TRANSFER', amount=amount, description=f'Sent to {recipient_account.user.username} ({recipient_account.account_number})')
                Transaction.objects.create(account=recipient_account, transaction_type='TRANSFER', amount=amount, description=f'Received from {sender_account.user.username} ({sender_account.account_number})')
                messages.success(request, f'₹{amount} has been successfully transferred to {recipient_account.user.username}!')
                return redirect('dashboard')
            except Account.DoesNotExist:
                messages.error(request, 'Recipient account number does not exist.')
            except Exception as e:
                messages.error(request, 'An unexpected error occurred. Please try again.')
    else:
        form = TransferForm()
    context = {'form': form, 'account': request.user.account, 'active_page': 'transfer'}
    return render(request, 'bank/transfer.html', context)

@login_required
def download_transactions_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'
    writer = csv.writer(response)
    writer.writerow(['Timestamp', 'Transaction Type', 'Description', 'Amount'])
    transactions = Transaction.objects.filter(account=request.user.account).order_by('-timestamp')
    for transaction in transactions:
        writer.writerow([transaction.timestamp.strftime('%Y-%m-%d %H:%M:%S'), transaction.get_transaction_type_display(), transaction.description, transaction.amount])
    return response

@login_required
def loan_application_view(request):
    if request.method == 'POST':
        form = LoanApplicationForm(request.POST)
        if form.is_valid():
            loan_application = form.save(commit=False)
            loan_application.user = request.user
            loan_application.save()
            messages.success(request, 'Your loan application has been submitted successfully! We will get back to you soon.')
            return redirect('dashboard')
    else:
        form = LoanApplicationForm()
    context = {'form': form, 'active_page': 'apply_loan'}
    return render(request, 'bank/loan_application.html', context)

def sip_calculator_view(request):
    context = {'active_page': 'sip_calculator'}
    return render(request, 'bank/sip_calculator.html', context)

@login_required
def create_pf_account_view(request):
    if not PFAccount.objects.filter(user=request.user).exists():
        PFAccount.objects.create(user=request.user)
        messages.success(request, 'Congratulations! Your Provident Fund (PF) account has been created.')
    return redirect('dashboard')

@login_required
def pf_deposit_view(request):
    try:
        pf_account = PFAccount.objects.get(user=request.user)
    except PFAccount.DoesNotExist:
        messages.error(request, 'You do not have a PF account. Please create one first.')
        return redirect('dashboard')
    if request.method == 'POST':
        form = PFDepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            mpin = form.cleaned_data['mpin']
            try:
                main_account = request.user.account
                user_profile = request.user.userprofile
                if not check_password(mpin, user_profile.mpin):
                    messages.error(request, 'Invalid MPIN.')
                elif main_account.balance < amount:
                    messages.error(request, 'Insufficient balance in your main account.')
                else:
                    main_account.balance -= amount
                    main_account.save()
                    pf_account.balance += amount
                    pf_account.save()
                    Transaction.objects.create(account=main_account, transaction_type='TRANSFER', amount=amount, description=f'Deposit to PF Account ({pf_account.pf_account_number})')
                    messages.success(request, f'₹{amount} has been successfully deposited to your PF account.')
                    return redirect('dashboard')
            except Exception:
                messages.error(request, 'An unexpected error occurred.')
    else:
        form = PFDepositForm()
    context = {'form': form, 'pf_account': pf_account, 'main_account_balance': request.user.account.balance, 'active_page': 'provident_fund'}
    return render(request, 'bank/pf_deposit.html', context)