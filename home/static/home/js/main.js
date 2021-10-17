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