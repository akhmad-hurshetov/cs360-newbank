from decimal import Decimal

from django.shortcuts import redirect, render
from .models import Transaction
from django.http import HttpResponseRedirect
from django.urls import reverse
from accounts.models import Account

def history(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('accounts:login'))

    transfers = Transaction.objects.filter(sender=request.user) | Transaction.objects.filter(recipient=request.user)
    context = {'transfers': transfers}
    return render(request, 'transfer/history.html', context)


def transfer(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('accounts:login'))

    if request.method == 'POST':
        amount = request.POST.get('amount')
        to_user = request.POST.get('to_account')
        if Decimal(amount) < 100:
            error_message = "The minimum transfer amount is 100."
            return render(request, 'transfer/transfer.html', {'error_message': error_message})

        if Decimal(amount) > 10000:
            error_message = "The maximum transfer amount is 10000."
            return render(request, 'transfer/transfer.html', {'error_message': error_message})

        current_user = request.user
        if current_user.email == to_user:
            error_message = "You cannot transfer money to yourself."
            return render(request, 'transfer/transfer.html', {'error_message': error_message})

        if current_user.balance < Decimal(amount):
            error_message = "Insufficient balance."
            return render(request, 'transfer/transfer.html', {'error_message': error_message})

        try:
            to_user = Account.objects.get(email=to_user)
        except Account.DoesNotExist:
            error_message = "Recipient account does not exist."
            return render(request, 'transfer/transfer.html', {'error_message': error_message})

        transaction = Transaction(
            sender=current_user,
            recipient=to_user,
            amount=Decimal(amount),
        )
        try:
            transaction.transfer()
        except ValueError as e:
            return render(request, 'transfer/transfer.html', {'error_message': str(e)})

        return HttpResponseRedirect(reverse('transfers:history'))

    return render(request, 'transfer/transfer.html')
