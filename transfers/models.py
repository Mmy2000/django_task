from django.db import models

class Account(models.Model):
    account_number = models.CharField(max_length=36, unique=True)  # UUID length
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.name} ({self.account_number})'

class Transfer(models.Model):
    from_account = models.ForeignKey(Account, related_name='transfers_made', on_delete=models.CASCADE)
    to_account = models.ForeignKey(Account, related_name='transfers_received', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Transfer {self.amount} from {self.from_account} to {self.to_account} on {self.timestamp}'