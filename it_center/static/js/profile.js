
// function scrollToTopBtn(){
//     function scrolling(){
//         if(window.scrollY> 0){
//         setTimeout(function(){
//             window.scrollTo(0, window.scrollY - window.innerHeight*15/100);
//             scrolling();
//         },6)
//         } 
//     }  
//     scrolling()
// }

$( document ).ready(function() {   
    $('.btn-edit-profile').on('click',function(e){ 
        $('#form-update-profile').toggle("slow")
        $('html, body').animate({
            scrollTop: $("#form-update-profile").offset().top
        }, 2000);
        e.preventDefault();
    });   
});
