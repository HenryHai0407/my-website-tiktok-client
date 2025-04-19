from django.urls import path

from . import views

app_name = "category"
urlpatterns = [
    path("", views.list, name="list"),
    path("<int:id>", views.detail, name="detail"),
]
