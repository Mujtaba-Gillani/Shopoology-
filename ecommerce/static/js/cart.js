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

function updateUserOrder(productId, action){
    console.log('User is authenticated, Sending data....');
    var url = '/update_item/';
    fetch(url,{
        method: 'POST', headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId':productId, 'action':action})
    })
    .then((response)=>{
        return response.json();
    })
    .then((data)=>{
        console.log('Data: ', data);
        location.reload();
    });
}

