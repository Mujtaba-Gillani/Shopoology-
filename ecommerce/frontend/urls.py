from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('aboutus/', views.about_us, name='aboutus'),
    path('menu/', views.menu, name='menu'),
    path('team/', views.team, name='team'),
    path('services/', views.service, name='services'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path('contactus/', views.contactUs, name='contactus'),

]