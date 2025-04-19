from django.shortcuts import render, redirect
from django.conf import settings
import requests

# Create your views here.


def sign_in(request):
    error = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            response = requests.post(
                f"{settings.API_BASE_URL}/auth/login",
                json={"username": username, "password": password}
            )

            if response.status_code == 200:
                access_token = response.json().get('access_token')
                print(f"token: {access_token}")
                resp = redirect("home:home")
                resp.set_cookie(
                    key='access_token',
                    value=access_token,
                    httponly=True,
                    secure=False,
                    samesite='Lax',
                    max_age=3600
                )
                return resp
            else:
                error = response.json().get('message', 'Invalid credentials.')

        except requests.exceptions.RequestException as e:
            error = f"Error connecting to API: {e}"

    context = {
        "error": error
    }
    return render(request, 'sign_in/index.html', context)
