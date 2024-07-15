import csv
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Account , Transfer

def import_accounts(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        reader = csv.DictReader(csv_file.read().decode('utf-8').splitlines())
        for row in reader:
            Account.objects.create(
                account_number=row['ID'],
                name=row['Name'],
                balance=row['Balance']
            )
        return HttpResponse("Accounts imported successfully")
    return render(request, 'import.html')



def list_accounts(request):
    accounts = Account.objects.all()
    return render(request, 'list_accounts.html', {'accounts': accounts})


def account_detail(request, account_number):
    account = get_object_or_404(Account, account_number=account_number)
    
    # Retrieve all transfers made by this account and received by this account
    transfers_made = account.transfers_made.all()
    transfers_received = account.transfers_received.all()
    
    return render(request, 'account_detail.html', {
        'account': account,
        'transfers_made': transfers_made,
        'transfers_received': transfers_received
    })

from django import forms

class TransferForm(forms.Form):
    from_account = forms.ModelChoiceField(queryset=Account.objects.all())
    to_account = forms.ModelChoiceField(queryset=Account.objects.all())
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

def transfer_funds(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            from_account = form.cleaned_data['from_account']
            to_account = form.cleaned_data['to_account']
            amount = form.cleaned_data['amount']

            if from_account.balance >= amount:
                from_account.balance -= amount
                to_account.balance += amount
                from_account.save()
                to_account.save()

                # Create a transfer record
                Transfer.objects.create(from_account=from_account, to_account=to_account, amount=amount)

                return render(request, 'transfer_success.html')
            else:
                return render(request, 'transfer_fail.html', {'error': 'Insufficient funds'})
    else:
        form = TransferForm()
    return render(request, 'transfer.html', {'form': form})
