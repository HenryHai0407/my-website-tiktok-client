from django.urls import path

from . import views

app_name = "home"
urlpatterns = [
    path("", views.home, name="home"),
    path("gioi-thieu/", views.about, name="about"),
]