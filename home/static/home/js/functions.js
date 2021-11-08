function parseListOfObjects(string) {
    // Logic: https://gist.github.com/mr-vaibh/3f02a58e7dbf698347675ea72d9bdc2f
    return string.slice(1, -1).split(",").map(obj => JSON.parse(obj))
}

function removeDuplicates(data, key) {
    return [...new Map(data.map(item => [key(item), item])).values()]
};


function get_cart(reload=false) {
    // TODO: fix- localstorage getting overided to cloud cart without merging
    
    $.ajax({
        type: "GET",
        url: "/api/getcart/",
        dataType: "json",
        success: function (response) {
            if (response['loggedin'] == true) {
                const cart = response['cart'];

                localStorage.setItem('cart', JSON.stringify(cart));
            }

            if (reload) {
                window.location.reload();
            } else {
                // Updating navigation CART
                let totalCartItems = 0;
                if (localStorage.getItem('cart') !== null) {
                    JSON.parse(localStorage.getItem('cart')).forEach(product => {
                        totalCartItems += product['quantity'];
                    });    
                }
                $('#totalCartItems').text(totalCartItems.toString());
            }
        }
    });
}


function update_cart(updatedCart, csrftoken) {
    $.ajax({
        type: "POST",
        url: "/api/updatecart/",
        data: {
            cart: JSON.stringify(updatedCart),
        },
        headers: { "X-CSRFToken": csrftoken },
        dataType: "json",
        success: function (response) {
            if (response['loggedin'] != true) {
                const localCart = JSON.parse(response['localCart']);
                
                for (let i = 0; i < localCart.length - 1; i++) {
                    const product = localCart[i];
                    
                    if (product['id'] == localCart[localCart.length - 1]['id']) {
                        product['quantity'] = localCart[localCart.length - 1]['quantity'];
                        localCart.pop();
                        break;
                    }
                }
                
                localStorage.setItem('cart', JSON.stringify(localCart));
            }

            // fetch cart
            get_cart();
        }
    });
}


function delete_cart(productId, csrftoken) {
    $.ajax({
        type: "DELETE",
        url: "/api/deletecart/" + productId,
        headers: { "X-CSRFToken": csrftoken },
        dataType: "json",
        success: function (response) {
            if (response['loggedin'] == true) {
                // some logged in cart stuff
                get_cart(reload=true);
            } else {
                let cart = JSON.parse(localStorage.getItem('cart'));

                for (let i = 0; i < cart.length; i++) {
                    const product = cart[i];
                    
                    if (product['id'] == productId) {
                        const productIndex = cart.indexOf(product);
                        cart.splice(productIndex, 1);
                        break;
                    }
                }

                localStorage.setItem('cart', JSON.stringify(cart));
            }

            window.location.reload();
        }
    });
}