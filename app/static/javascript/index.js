document.addEventListener('DOMContentLoaded', function() {
    let slideIndex = 0;
    showSlides(slideIndex);

    // Find arrows
    const prevArrow = document.querySelector('.prev');
    const nextArrow = document.querySelector('.next');

    // Attach click events to arrows
    if (prevArrow) {
        prevArrow.addEventListener('click', function() {
            moveSlide(-1); // Move to the previous slide
        });
    }

    if (nextArrow) {
        nextArrow.addEventListener('click', function() {
            moveSlide(1); // Move to the next slide
        });
    }

    function moveSlide(n) {
        showSlides(slideIndex += n);
      }
  
    function showSlides(n) {
      let i;
      let slides = document.getElementsByClassName("slide");
      if (n >= slides.length) {slideIndex = 0}
      if (n < 0) {slideIndex = slides.length - 1}
      for (i = 0; i < slides.length; i++) {
          slides[i].style.display = "none";
      }
      slides[slideIndex].style.display = "block";
    }
  
    // Automatic slideshow
    setInterval(function() { moveSlide(1); }, 4000); // Change slide every 4 seconds
});

  