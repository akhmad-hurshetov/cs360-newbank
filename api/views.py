from booking.models import Booking
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import BookingSerializer
from rest_framework import status
from transfer.models import Transaction
from .serializers import TransactionSerializer
from decimal import Decimal
from accounts.models import Account
from django.utils import timezone
import rest_framework.status

# Create your views here.
def register(request):
    pass

def account(request):
    pass

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def booking(request):
    if request.method == 'GET':
        bookings = Booking.objects.filter(booked_by=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(booked_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def transfer(request):
    if request.method == 'POST':
        serializer = TransactionSerializer(data=request.data)
        amount = request.data.get('amount')
        to_account = request.data.get('to_account')

        if float(amount) < 100:
            error_message = "The minimum transfer amount is 100."
            return Response({'error_message': error_message}, status=status.HTTP_400_BAD_REQUEST)
        current_user = request.user
        if current_user.email == to_account:
            error_message = "You cannot transfer money to yourself."
            return Response({'error_message': error_message}, status=status.HTTP_400_BAD_REQUEST)
        if current_user.balance < float(amount):
            error_message = "Insufficient balance."
            return Response({'error_message': error_message}, status=status.HTTP_400_BAD_REQUEST)
        try:
            to_user = Account.objects.get(email=to_account)
        except Account.DoesNotExist:
            error_message = "Recipient account does not exist."
            return Response({'error_message': error_message}, status=status.HTTP_400_BAD_REQUEST)

        transaction = Transaction.objects.create(
            sender=current_user,
            recipient=to_user,
            amount=amount,
            timestamp=timezone.now(),
        )
        transaction.save()

        current_user.balance -= Decimal(amount)
        current_user.save()
        
        to_user.balance += Decimal(amount)
        to_user.save()

        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    transfers = Transaction.objects.filter(sender=request.user) | Transaction.objects.filter(recipient=request.user)
    serializer = TransactionSerializer(transfers, many=True)
    return Response(serializer.data)
