from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
import requests
from django.conf import settings
from django.http import JsonResponse

# Create your views here.
@require_POST
def add_to_cart(request, product_id):
    product_id = str(product_id)  # Ensure it's always a string key
    cart = request.session.get("cart", {})
    cart[product_id] = cart.get(product_id, 0) + 1  # Increment quantity
    request.session["cart"] = cart
    messages.success(request, "Product added to cart!")
    return redirect(request.META.get('HTTP_REFERER', 'product:list'))  # Redirects back to the same page

@require_POST
def increase_quantity(request, product_id):
    cart = request.session.get("cart", {})
    if str(product_id) in cart:
        cart[str(product_id)] += 1
    request.session["cart"] = cart
    return redirect("cart:view_cart")


@require_POST
def decrease_quantity(request, product_id):
    cart = request.session.get("cart", {})
    if str(product_id) in cart:
        cart[str(product_id)] -= 1
        if cart[str(product_id)] <= 0:
            del cart[str(product_id)]
    request.session["cart"] = cart
    return redirect("cart:view_cart")

def view_cart(request):
    cart = request.session.get("cart", {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        res = requests.get(f"{settings.API_BASE_URL}/products/{product_id}")
        if res.status_code == 200:
            product = res.json()
            product["quantity"] = quantity
            product["subtotal"] = product["price"] * quantity
            total_price += product["subtotal"]
            cart_items.append(product)

    return render(request, "cart/index.html", {
        "cart_items": cart_items,
        "total_price": total_price
    })

### Add the Checkout View
@require_POST
def checkout(request):
    cart = request.session.get("cart", {})
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect("cart:view_cart")

    cart_items = []
    for product_id, quantity in cart.items():
        res = requests.get(f"{settings.API_BASE_URL}/products/{product_id}")
        if res.status_code == 200:
            product = res.json()
            product["quantity"] = quantity
            cart_items.append(product)

    items_payload = [
        {
            "product_id": item["id"],
            "quantity": item["quantity"],
            "unit_price": item["price"],
            "description": item.get("summary", "")
        }
        for item in cart_items
    ]

    if isinstance(request.user, dict):
        user_id = request.user.get("id")
    else:
        user_id = getattr(request.user, "id", None)
    token = request.COOKIES.get("access_token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    payload = {
        "customer_id": user_id,
        "user_id": user_id,
        "description": "Checkout from frontend cart",
        "items": items_payload
    }

    try:
        response = requests.post(f"{settings.API_BASE_URL}/orders/", json=payload, headers=headers)
        print("STATUS CODE:", response.status_code)
        print("RESPONSE BODY:", response.text)
        if response.status_code == 200:
            order = response.json()
            request.session["latest_order"] = order  # ✅ Save for summary
            return redirect("cart:order_summary")  # ✅ Redirect here
        else:
            messages.error(request, "Failed to place the order.")
    except Exception as e:
        messages.error(request, f"Error occurred: {e}")

    return redirect("cart:view_cart")

def order_summary(request):
    order = request.session.get("latest_order")
    if not order:
        messages.error(request, "No recent order found.")
        return redirect("cart:view_cart")

    return render(request, "cart/order_summary.html", {"order": order})

def mini_cart_data(request):
    cart = request.session.get("cart", {})
    items = []

    for product_id, quantity in cart.items():
        res = requests.get(f"{settings.API_BASE_URL}/products/{product_id}")
        if res.status_code == 200:
            product = res.json()
            items.append({
                "id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "quantity": quantity,
            })

    return JsonResponse({"items": items})


