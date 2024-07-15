from django.test import TestCase, Client
from django.urls import reverse
from .models import Account, Transfer

class TransferFundsTest(TestCase):

    def setUp(self):
        # Create test accounts
        self.from_account = Account.objects.create(account_number='1234567890', name='John Doe', balance=1000.00)
        self.to_account = Account.objects.create(account_number='0987654321', name='Jane Doe', balance=500.00)
        self.client = Client()

    def test_transfer_funds_success(self):
        response = self.client.post(reverse('transfer_funds'), {
            'from_account': self.from_account.id,
            'to_account': self.to_account.id,
            'amount': '200.00'
        })

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The funds have been transferred successfully.')

        # Refresh accounts from database
        self.from_account.refresh_from_db()
        self.to_account.refresh_from_db()

        # Check the balances
        self.assertEqual(self.from_account.balance, 800.00)
        self.assertEqual(self.to_account.balance, 700.00)

        # Check the transfer record
        transfer = Transfer.objects.get(from_account=self.from_account, to_account=self.to_account)
        self.assertEqual(transfer.amount, 200.00)

    def test_transfer_funds_insufficient_balance(self):
        response = self.client.post(reverse('transfer_funds'), {
            'from_account': self.from_account.id,
            'to_account': self.to_account.id,
            'amount': '2000.00'
        })

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Insufficient funds for transfer.')

        # Refresh accounts from database
        self.from_account.refresh_from_db()
        self.to_account.refresh_from_db()

        # Check the balances
        self.assertEqual(self.from_account.balance, 1000.00)
        self.assertEqual(self.to_account.balance, 500.00)

        # Check no transfer record is created
        self.assertFalse(Transfer.objects.filter(from_account=self.from_account, to_account=self.to_account).exists())
