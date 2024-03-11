/* When the user clicks on the button, 
  toggle between hiding and showing the dropdown content */
  function showDropdown() {
    showPlaces();
  }
  
  function showPlaces() {
    document.getElementById("place").classList.toggle("show");
  }
  
  function showEvents() {
    document.getElementById("place").classList.toggle("show");
  }
  
  // Close the dropdown if the user clicks outside of it
  window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }

    //If Find Places button is clicked
    if (!event.target.matches('.button')) {
      
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }