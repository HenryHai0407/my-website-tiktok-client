from django.urls import path

from . import views

app_name = "sign_out"
urlpatterns = [
    path("", views.sign_out, name="sign_out"),

]
