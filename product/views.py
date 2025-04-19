from django.shortcuts import render
from django.conf import settings
import requests

# Create your views here.


def list(request):

    reponse = requests.get(f"{settings.API_BASE_URL}/products")
    print(reponse)

    items = reponse.json()  

    return render(request, 'product/index.html', {'items': items})


def detail(request, id):

    reponse = requests.get(f"{settings.API_BASE_URL}/products/{id}")
    print(reponse)

    item = reponse.json()

    return render(request, 'product/detail.html', {'item': item})

def search_products(request):
    query = request.GET.get("q","")
    items = []

    if query:
        try:
            response = requests.get(f"{settings.API_BASE_URL}/products/search", params={"q": query})
            if response.status_code == 200:
                items = response.json()
        except Exception as e:
            print(f"Error fetching search results: {e}")
    return render(request, "product/search_results.html", {"items":items,"query":query})