var updateBtns = document.getElementsByClassName('update-cart');

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.getAttribute('data-product');
        var action = this.getAttribute('data-actions'); 
        console.log('productId:', productId, 'action:', action);
        console.log('USER: ', user);
        if (user == 'AnonymousUser') {
            addCookieItem(productId, action)
        } else {
            updateUserOrder(productId, action)
        }
    })
}

var cart = JSON.parse(getCookie('cart')) || {};  // Initialize cart if 'cart' is undefined

function addCookieItem(productId, action) {
    console.log('User Not logged in..');
    if (!cart[productId]) {
        cart[productId] = { 'quantity': 0 };
    }

    if (action == 'add') {
        cart[productId]['quantity'] += 1;
    } else if (action == 'remove') {
        cart[productId]['quantity'] = Math.max(0, cart[productId]['quantity'] - 1);
    }

    if (cart[productId]['quantity'] <= 0) {
        console.log('Item is Deleted');
        delete cart[productId];
    }

    console.log('cart: ', cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
    // location.reload();
}
    // Assuming you want to perform the action on elements with specific IDs

    function updatePageContent(data) {
        var itemNumbElement = document.getElementById('ItemNumb');
        var totalNumbElement = document.getElementById('TotalNumb');
        var quantityNumElement = document.getElementById('quantityNum');
        var nettotalElement = document.getElementById('nettotal');
    
        // Update the content of the elements based on the data
        if (itemNumbElement) {
            itemNumbElement.innerHTML = '<h5>Items: <strong>' + data.order.get_cart_items + '</strong></h5>';
        }
    
        if (totalNumbElement) {
            totalNumbElement.innerHTML = '<h5>Total:<strong> Rs.' + data.order.get_cart_total + '</strong></h5>';
        }
    
        if (quantityNumElement) {
            quantityNumElement.innerHTML = '<strong>Quantity:</strong>';
        }
    
        if (nettotalElement) {
            nettotalElement.innerHTML = '<strong>Total</strong>';
        }
    
        // Call additional functions or perform other actions as needed
        // ...
    
        alert('Content updated successfully!');
    }

function updateUserOrder(productId, action){
    // get div/element ids 

    console.log('User is authenticated, Sending data....');
    var url = '/update_item/';
    fetch(url,{
        method: 'POST', 
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId':productId, 'action':action})
    })
    .then((response)=>{
        // window.location.reload(true); // Force a full page reload

        return response.json();
    })
    .then((data)=>{
        console.log('Data: ', data);
        // location.reload();
        updateCart(data)

    })
    .catch((error)=>{
        console.log('Error: ', error);
    });
}
function updateCart(data) {
    // Update the cart items count
    var cartElement = document.getElementById('cart');
    cartElement.innerHTML = 'Cart Items: ' + data.cartItems;

    // Create a container for cart items
    var cartContainer = document.createElement('div');

    // Check if there are items in the cart
    if (data.items.length > 0) {
        // Iterate through items and update cart content
        data.items.forEach(function (item) {
            var itemDiv = document.createElement('div');
            itemDiv.innerHTML = `
                <p>Product: ${item.product.name}</p>
                <p>Quantity: ${item.quantity}</p>
                <p>Total: $${item.get_total}</p>
            `;
            cartContainer.appendChild(itemDiv);
        });
    } else {
        // Display a message if the cart is empty
        cartContainer.innerHTML = '<p>Your cart is empty</p>';
    }

    // Append the cart content to the existing structure
    cartElement.appendChild(cartContainer);

    // Call the function to update other page content
    updatePageContent(data);

    // Optionally, provide user feedback (e.g., a notification) about the cart update
    alert('Cart updated successfully!');
}

// Function to update specific elements on the page
function updatePageContent(data) {
    var itemNumbElement = document.getElementById('ItemNumb');
    var totalNumbElement = document.getElementById('TotalNumb');
    var quantityNumElement = document.getElementById('quantityNum');
    var nettotalElement = document.getElementById('nettotal');

    // Update the content of the elements based on the data
    if (itemNumbElement) {
        itemNumbElement.innerHTML = '<h5>Items: <strong>' + data.order.get_cart_items + '</strong></h5>';
    }

    if (totalNumbElement) {
        totalNumbElement.innerHTML = '<h5>Total:<strong> Rs.' + data.order.get_cart_total + '</strong></h5>';
    }

    if (quantityNumElement) {
        quantityNumElement.innerHTML = '<strong>Quantity:</strong>';
    }

    if (nettotalElement) {
        nettotalElement.innerHTML = '<strong>Total</strong>';
    }
}
