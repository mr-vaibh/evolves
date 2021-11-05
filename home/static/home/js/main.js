$(document).ready(function () {
    
    // search submits form
    const searchForm = document.getElementById('search-form');
    const searchField = document.getElementById('search-field');

    searchForm.addEventListener('submit', (e) => {
        e.preventDefault();
        if (searchField.value !== '' && searchField.value.length >= 3) {
            window.location.href = `/search/${searchField.value}/`;
        } else {
            alert('Type atleast 3 characters')
        }
    });

    
    // To update localstorage
    get_cart();

    
    // Updating navigation CART
    let totalCartItems = 0;

    if (localStorage.getItem('cart') !== null) {
        JSON.parse(localStorage.getItem('cart')).forEach(product => {
            totalCartItems += product['quantity'];
        });    
    }
    
    $('#totalCartItems').text(totalCartItems.toString())

});