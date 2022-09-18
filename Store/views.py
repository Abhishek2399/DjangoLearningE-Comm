from django.shortcuts import render

# Create your views here.
def home(request):
    print("Store home view called")
    return render(request, 'home.html')