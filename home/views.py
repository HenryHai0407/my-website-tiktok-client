from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import requests

# Create your views here.


def home(request):
    return render(request, 'home/index.html')


def about(request):

    return render(request, 'home/about.html')
