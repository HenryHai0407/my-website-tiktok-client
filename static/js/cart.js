
  document.addEventListener("DOMContentLoaded", function () {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    document.querySelectorAll(".add-to-cart-btn").forEach(button => {
      button.addEventListener("click", function (e) {
        e.preventDefault();
        const productId = this.dataset.productId;

        fetch(`/cart/add/${productId}/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": csrftoken,
          }
        })
        .then(response => response.json())
        .then(data => {
          updateMiniCart(data.cart_items);
        })
        .catch(err => {
          console.error("Cart error:", err);
        });
      });
    });

    function updateMiniCart(items) {
      const cartDropdown = document.getElementById("mini-cart-items");
      cartDropdown.innerHTML = "";

      if (items.length === 0) {
        cartDropdown.innerHTML = `<li class="dropdown-item">Your cart is empty</li>`;
      } else {
        items.forEach(item => {
          cartDropdown.innerHTML += `
            <li class="dropdown-item d-flex justify-content-between">
              <span>${item.name}</span>
              <span>x${item.quantity}</span>
            </li>
          `;
        });
      }

      document.getElementById("mini-cart-count").innerText = items.reduce((sum, item) => sum + item.quantity, 0);
    }
  });
