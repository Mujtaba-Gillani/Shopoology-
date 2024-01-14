from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'frontend/home.html')

def about_us(request):
    return render(request, 'frontend/about.html')



def menu(request):
    return render(request, 'frontend/menu.html')

def team(request):
    return render(request, 'frontend/team.html')

def service(request):
    return render(request, 'frontend/services.html')

def testimonial(request):
    return render(request, 'frontend/testimonial.html')

def contactUs(request):
    return render(request, 'frontend/contact.html')