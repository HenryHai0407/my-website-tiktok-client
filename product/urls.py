from django.urls import path

from . import views

app_name = "product"
urlpatterns = [
    path("", views.list, name="list"),
    path("<int:id>", views.detail, name="detail"),
    path('search/', views.search_products, name="search"),
]
