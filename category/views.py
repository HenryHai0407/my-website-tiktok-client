from django.shortcuts import render
from django.conf import settings
import requests

# Create your views here.


def list(request):

    reponse = requests.get(f"{settings.API_BASE_URL}/categories")
    print(reponse)

    items = reponse.json()

    return render(request, 'category/index.html', {'items': items})


def detail(request, id):

    reponse = requests.get(f"{settings.API_BASE_URL}/categories/{id}")
    print(reponse)

    item = reponse.json()

    return render(request, 'category/detail.html', {'item': item})
