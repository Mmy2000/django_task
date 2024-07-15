import csv
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Account , Transfer
from django.contrib import messages
from .forms import TransferForm
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
        messages.success(request,'Accounts imported successfully')
       
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

                messages.success(request, 'The funds have been transferred successfully.')
            else:
                messages.error(request, 'Insufficient funds for transfer.')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = TransferForm()
    return render(request, 'transfer.html', {'form': form})
