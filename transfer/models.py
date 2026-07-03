from django.db import models
from accounts.models import Account

# Create your models here.
class Transaction(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sent_transactions')
    recipient = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='received_transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def transfer(self):
        if self.sender == self.recipient:
            raise ValueError("Cannot transfer to yourself")
        if self.amount <= 0:
            raise ValueError("Amount must be positive")
        if self.sender.balance < self.amount:
            raise ValueError("Insufficient balance")

        self.sender.balance -= self.amount
        self.recipient.balance += self.amount
        self.sender.save()
        self.recipient.save()
        self.save()

    def __str__(self):
        return f'Transaction from {self.sender} to {self.recipient} of {self.amount}'