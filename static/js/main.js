$(document).ready(function() {
  $('.posts .post').not('.animation').each(function(i){
    setTimeout(function(){
       $('.posts .post').eq(i).addClass('animation');
    },150*i);
  });

  $(document.links).filter(function() {
    return this.hostname != window.location.hostname;
  }).attr('target', '_blank');
});