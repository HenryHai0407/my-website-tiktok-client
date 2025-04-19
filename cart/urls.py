from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.view_cart, name="view_cart"),
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("increase/<int:product_id>/", views.increase_quantity, name="increase_quantity"),
    path("decrease/<int:product_id>/", views.decrease_quantity, name="decrease_quantity"),
    path("checkout/", views.checkout, name="checkout"),
    path("summary/", views.order_summary, name="order_summary"),
    path("mini-cart-data/", views.mini_cart_data, name="mini_cart_data"),
]
