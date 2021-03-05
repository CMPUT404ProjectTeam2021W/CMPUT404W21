$(document).ready(function() {
  setTimeout(function() {
    $('.hermes-big').animate({
      marginTop: "-=15vh",
      opacity: 1
    }, 250);
  },400);
  setTimeout(function() {
    $('.big-marker').animate({
      opacity: 1
    }, 250);
  },500);

  setTimeout(function() {
    $('.friendly-reminder').animate({
      opacity: 1
    }, 250);
  },700);

  setTimeout(function() {
    $('.link-box').animate({
      opacity: 1,
      display: "visible"
    }, 250);
  },900);


});
