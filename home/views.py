from django.shortcuts import render

# Create your views here.
def index(request):
    user = request.user
    return render(request, 'home/index.html', {'user': user})

def cards(request):
    return render(request, 'home/index.html')