from django.shortcuts import render
from .models import Cake
# Create your views here.

def home(request):
    return render(request, 'frontend/home.html')

def about_us(request):
    return render(request, 'frontend/about.html')



def menu(request):
    birthday_cakes = Cake.objects.filter(type='Birthday', active=True)
    wedding_cakes = Cake.objects.filter(type='Wedding', active=True)
    custom_cakes = Cake.objects.filter(type='Custom', active=True)
    context = {
        'birthday_cakes': birthday_cakes,
        'wedding_cakes': wedding_cakes,
        'custom_cakes': custom_cakes,
    }
    return render(request, 'frontend/menu.html', context)


def team(request):
    return render(request, 'frontend/team.html')

def service(request):
    return render(request, 'frontend/services.html')

def testimonial(request):
    return render(request, 'frontend/testimonial.html')

def contactUs(request):
    return render(request, 'frontend/contact.html')



def registraion(request):
    return render(request, 'frontend/sign.html')


def AddToCart(request):
    return render(request, 'frontend/cart.html')