// Get the button:
let mybutton = document.getElementById("myBtn");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}

document.addEventListener("DOMContentLoaded", function() {
  const carouselInner = document.querySelector('.carousel-inner');
  const carouselItems = document.querySelectorAll('.carousel-item');
  let currentIndex = 0;

  function showSlide(index) {
    const offset = -index * 100;
    carouselInner.style.transform = `translateX(${offset}%)`;
    currentIndex = index;
  }

  document.querySelector('.carousel-control-prev').addEventListener('click', function() {
    if (currentIndex > 0) {
      showSlide(currentIndex - 1);
    } else {
      showSlide(carouselItems.length - 1);
    }
  });

  document.querySelector('.carousel-control-next').addEventListener('click', function() {
    if (currentIndex < carouselItems.length - 1) {
      showSlide(currentIndex + 1);
    } else {
      showSlide(0);
    }
  });
});
