from django.shortcuts import render

# Create your views here.
def home(request):
    print("Tags home view called")
    return render(request, 'home.html')


