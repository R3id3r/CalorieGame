header('Content-Type: text/javascript');

$(document).ready(function(){

$(".navbar-brand").click(function(){
    $(".navbar-toggler").addClass("collapsed");
    $(".navbar-toggler").attr("aria-expanded","false");
    $(".navbar-collapse").removeClass("show");
});

});