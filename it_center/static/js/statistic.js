
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
    $(".fas-info").on("click",function(e){
        e.preventDefault(); 
        $("#class_in_active").toggle("slow");
   })
});
