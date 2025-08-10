// Confirm script is loaded
console.log("modal.js loaded!");
// Function to get CSRF token from cookies
async function loadProducts() {
    try {

        //alert("in loadproducts")
        const response = await fetch('/api/products/');
        const products = await response.json();

        let container = document.getElementById('products-container');
        container.innerHTML = ''; // Clear old products

        // Generate products list
        products.forEach(product => {
                                    container.innerHTML += `<li>
                                      <div class="product-card">
                                        <img src="${product.image}" alt="${product.name}">
                                        <h3>${product.name}</h3>
                                        <p>₹${product.price}</p>
                                       <button class="add-to-cart-btn" data-product-id="${product.id}" data-product-name="${product.name}" data-price="${product.price}">Add to Cart</button>
                                      </div>
                                   </li>`

        });



    } catch (error) {

        alert('laod error'+error);
        console.error('Error loading products:', error);
    }
}
async function openBuyNow(productId) {
  try {
        console.log("Buy Now clicked for ID:", productId); // ✅ Correct variable

        const res = await fetch(`/api/products/${productId}/`);
        if (!res.ok)
            throw new Error('Failed to fetch product');

        const product = await res.json();
        document.getElementById('product_id').innerText =productId;
                //alert(document.getElementById('product_id').innerText);
        document.getElementById('modalTitle').innerText = product.name;
        document.getElementById('modalDescription').innerText = product.description;
        document.getElementById('modalPrice').innerText = `₹${product.price}`;

        const buyModal = new bootstrap.Modal(document.getElementById('buyNowModal'), {
                            backdrop: 'static',
                            keyboard: false
                        });
                        buyModal.show();

       // new bootstrap.Modal(document.getElementById("buyNowModal")).show();
        //document.getElementById('buyNowModal').show()
    } catch (error) {

        //alert(error);
        console.error('Error fetching product:', error);
          }
    }

function closeModal() {
    document.getElementById('buyNowModal').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', loadProducts);
document.addEventListener('DOMContentLoaded', function () {
    // Attach click listeners to all current and future Add to Cart buttons
    document.getElementById('products-container').addEventListener('click', function(e) {

                if (e.target && e.target.classList.contains('add-to-cart-btn')) {

                   // alert("clicked");

            const btn = e.target;
            const productId = btn.getAttribute('data-product-id');
            const productName = btn.getAttribute('data-product-name');
            const price = btn.getAttribute('data-price');
             //alert(price)
            // Prepare data for sending
            const data = {
                product_id: productId,
                product_name: productName,
                price: price,
                quantity: 1  // Default quantity, or you can add UI to select this
            };

            // Send POST request to add to cart endpoint
            fetch('/add-to-cart/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),  // If using Django CSRF protection
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                if(result.status === "success") {
               alert('Added to cart: ' + productName);
                loadCart()

                ;  // Refresh cart UI
}
 else {
                    alert('Failed to add to cart: ' + (result.message || 'Unknown error'));
                }
            })
            .catch(error => {
                console.error('Error adding to cart:', error);
                alert('Error adding to cart');
            });
        }
    });
});

// Utility to get CSRF token cookie (needed for Django POST requests)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
async function loadCart() {
    try {
        const response = await fetch('/api/cart/');
        const data = await response.json();

        const cartList = document.getElementById('cart-items-list');
        cartList.innerHTML = '';

        if (data.cart_items.length === 0) {
            cartList.innerHTML = '<li>Your cart is empty.</li>';
            document.getElementById('cart-total').innerText = '0.00';
            return;
        }

        data.cart_items.forEach(item => {
            const li = document.createElement('li');
            li.innerText = `${item.product_name} — ₹${item.price} × ${item.quantity} = ₹${item.total.toFixed(2)}`;
            cartList.appendChild(li);
        });

        document.getElementById('cart-total').innerText = data.total_price.toFixed(2);

    } catch (error) {
        console.error('Error loading cart:', error);
    }
}
document.addEventListener('DOMContentLoaded', loadCart);
