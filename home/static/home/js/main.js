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

    // shortcut key to search
    document.addEventListener('keyup', (e) => {
        // this would test for whichever key is 40 (down arrow) and the ctrl key at the same time
        if (e.ctrlKey && e.key === '/') {
            // call your function to do the thing
            searchField.focus();
        }
    }, false);


    // To update localstorage
    get_cart();

});