from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Booking

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('accounts:login'))
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
        datetime_str = f"{date} {time}"
        user = request.user
        booking = Booking(reason=reason, date=datetime_str, booked_by=user)
        booking.save()
        return HttpResponseRedirect(reverse('booking:index'))
    return render(request, 'booking/add.html')
