from django.contrib import admin
from .models import Account
# Register your models here.


from django import forms
from django.shortcuts import render
from django.urls import path
from django.http import HttpResponseRedirect

class TransferForm(forms.Form):
    from_account = forms.ModelChoiceField(queryset=Account.objects.all())
    to_account = forms.ModelChoiceField(queryset=Account.objects.all())
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

from django.contrib import admin
from .models import Account, Transfer

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'name', 'balance')
    actions = ['transfer_funds']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('transfer/', self.admin_site.admin_view(self.transfer_view), name='transfer_funds'),
        ]
        return custom_urls + urls

    def transfer_view(self, request):
        form = TransferForm()
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
                    Transfer.objects.create(from_account=from_account, to_account=to_account, amount=amount)
                    self.message_user(request, "Funds transferred successfully")
                    return HttpResponseRedirect("../")
                else:
                    self.message_user(request, "Insufficient funds", level='error')
        context = {
            'form': form,
            'title': 'Transfer Funds',
            'opts': self.model._meta,
            'has_permission': self.has_change_permission(request),
        }
        return render(request, 'admin/transfer_funds.html', context)

    def transfer_funds(self, request, queryset):
        return HttpResponseRedirect("transfer/")

    transfer_funds.short_description = "Transfer Funds Between Accounts"

@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('from_account', 'to_account', 'amount', 'timestamp')
    list_filter = ('timestamp', 'from_account', 'to_account')
    search_fields = ('from_account__name', 'to_account__name')
