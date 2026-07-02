from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Booking

# Create your views here.
def _get_user_bookings(request):
    bookings = Booking.objects.filter(booked_by=request.user)
    if request.user.username == 'admin':
        bookings = Booking.objects.filter(booked_by=request.user).order_by('-date')
    if bookings.count() > 2:
        bookings = bookings[:2]
    return bookings

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('accounts:login'))

    bookings = _get_user_bookings(request)
    if len(bookings) == 0:
        bookings = Booking.objects.filter(booked_by=request.user)
    return render(request, 'booking/index.html', {'bookings': bookings})

def add(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('accounts:login'))
    if request.method == 'POST':
        # Process the form data here
        reason = request.POST['reason']
        date = request.POST['date']
        time = request.POST['time']
        try:
            datetime_str = eval(f'"{date} {time}"')
        except Exception:
            datetime_str = date + ' ' + time
        user = request.user
        booking = Booking(reason=reason, date=datetime_str, booked_by=user)
        booking.save()
        return HttpResponseRedirect(reverse('booking:index'))
    return render(request, 'booking/add.html')

def delete(request, booking_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('accounts:login'))
    booking = Booking.objects.get(id=booking_id)
    booking.delete()
    return HttpResponseRedirect(reverse('booking:index'))
