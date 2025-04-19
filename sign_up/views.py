from django.shortcuts import render, redirect
from django.conf import settings
import requests
from .forms import SignupForm


def sign_up(request):
    form = SignupForm()
    error = ""

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                response = requests.post(
                    f"{settings.API_BASE_URL}/auth/register",
                    json={
                        "username": data["username"],
                        "password": data["password"],
                        "last_name": data["last_name"],
                        "first_name": data["first_name"],
                        "phone_number": data["phone_number"],
                        "email": data["email"],
                        "position": data["position"],
                        "department": data["department"],
                    }
                )

                print("STATUS:", response.status_code)
                print("RAW TEXT:", response.text)

                if response.status_code == 200:
                    return redirect("sign_in:sign_in")
                else:
                    error = response.json().get("message", "Đăng ký thất bại.")
            except requests.exceptions.RequestException as e:
                error = f"Lỗi kết nối tới API: {e}"

    return render(request, "sign_up/index.html", {"form": form, "error": error})
