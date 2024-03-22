document.addEventListener('DOMContentLoaded', function() {
    var buttons = document.querySelectorAll('.category-button');
    buttons.forEach(function(button) {
        //category button event listener to make the XMLHttpRequest
        button.addEventListener('click', function(event) {
        event.preventDefault(); //prevent default action of button click
        var category = this.textContent.trim(); //gets the button's text (what the user sees)
        if (category == "All") {
            category = ""
        }
        
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/places/?category=' + category, true);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest') //indicates an AJAX request to the server
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) { //request done and request successful
                var response = JSON.parse(xhr.responseText)
                var placesHTML = response.places_html
                document.getElementById('places-container').innerHTML = placesHTML;
            }
        };
        xhr.send();
        });
    });
});