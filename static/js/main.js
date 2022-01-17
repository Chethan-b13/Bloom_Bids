$(document).ready(function () {
       
    window.setTimeout(function() {
        $("#messages").slideUp(2500, function(){
            $(this).remove(); 
        });
    }, 1200);
     
    });