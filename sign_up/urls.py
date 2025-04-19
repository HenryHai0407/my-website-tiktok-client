from django.urls import path

from . import views

app_name = "sign_up"
urlpatterns = [
    path("", views.sign_up, name="sign_up"),
]
