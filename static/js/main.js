// When the user scrolls down 80px from the top of the document, resize the navbar's padding and the logo's font size
window.onscroll = function() {myFunction(); navFunction();};

function myFunction() {
    var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    var scrolled = (winScroll / height) * 100;
    document.getElementById("myBar").style.width = scrolled + "%";
}

function navFunction() {
  if (document.body.scrollTop > 80 || document.documentElement.scrollTop > 80) {
    document.getElementById("navbar").style.padding = "1% 1%";
    document.getElementById("navbar").style.backgroundColor = "#25CCA0";
  } else {
    document.getElementById("navbar").style.padding = "1.8% 1%";
    document.getElementById("navbar").style.backgroundColor = "#2C3E52";
  }
}

