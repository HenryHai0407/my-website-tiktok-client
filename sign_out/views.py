from django.shortcuts import render, redirect

# Create your views here.


def sign_out(request):
    response = redirect('sign_in:sign_in')
    response.delete_cookie('access_token')
    return response
