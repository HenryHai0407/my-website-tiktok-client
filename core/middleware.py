# core/middleware.py
import requests
from django.conf import settings


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get("access_token")
        request.user = None

        if token:
            try:
                headers = {"Authorization": f"Bearer {token}"}
                response = requests.get(
                    f"{settings.API_BASE_URL}/users/profile", headers=headers
                )
                if response.status_code == 200:
                    request.user = response.json()

            except Exception:
                pass

        response = self.get_response(request)
        return response
