from django.urls import path
from . import views

urlpatterns = [
    path('aboutus/', views.about_us, name='aboutus'),

]