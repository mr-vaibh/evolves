function parseListOfObjects(string) {
    // Logic: https://gist.github.com/mr-vaibh/3f02a58e7dbf698347675ea72d9bdc2f
    return string.slice(1, -1).split(",").map(obj => JSON.parse(obj))
}

function removeDuplicates(data, key) {
    return [...new Map(data.map(item => [key(item), item])).values()]
};

function get_cart() {
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
            if (response['loggedin'] == true) {
                // some logged in cart stuff
                get_cart();
            } else {
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
        }
    });
}