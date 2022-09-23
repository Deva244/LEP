from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home_view(request, *args, **kwargs):
    return render(request, 'main/home.html', {})

def about_view(request, *args, **kwargs):
    return render(request, 'main/about.html', {})
