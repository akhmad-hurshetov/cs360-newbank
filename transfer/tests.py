from django.test import TestCase
from accounts.models import Account
from decimal import Decimal


class TransferAmountValidationTest(TestCase):

    def setUp(self):
        self.sender = Account.objects.create_user(
            username='sender', password='pass123', email='sender@test.com', balance=Decimal('200.00')
        )
        self.recipient = Account.objects.create_user(
            username='recipient', password='pass123', email='recipient@test.com', balance=Decimal('100.00')
        )
        self.client.login(username='sender', password='pass123')

    def test_transfer_below_minimum_is_rejected(self):
        response = self.client.post('/transfers/new/', {
            'amount': '50',
            'to_account': 'recipient@test.com'
        })
        self.sender.refresh_from_db()
        self.assertEqual(self.sender.balance, Decimal('200.00'))

    def test_float_precision_amount_is_rejected(self):
        response = self.client.post('/transfers/new/', {
            'amount': '99.99999999999999',
            'to_account': 'recipient@test.com'
        })
        self.sender.refresh_from_db()
        self.assertEqual(self.sender.balance, Decimal('200.00'))

    def test_valid_transfer_succeeds(self):
        response = self.client.post('/transfers/new/', {
            'amount': '100',
            'to_account': 'recipient@test.com'
        })
        self.sender.refresh_from_db()
        self.recipient.refresh_from_db()
        self.assertEqual(self.sender.balance, Decimal('100.00'))
        self.assertEqual(self.recipient.balance, Decimal('200.00'))
