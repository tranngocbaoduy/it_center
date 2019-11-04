$(document).ready(function(){ 
    $("#submit").attr("disabled",true); 
    $("#payment").on('keyup',function(e){
        e.preventDefault();
        if(isNaN($(this).val())){
            $("#submit").attr("disabled",true);  
            $(".error").text("Payment must be a number !!!") 
            $(".error").show()
        }else if(parseFloat($(this).val()) < 10){
            $("#submit").attr("disabled",true);  
            $(".error").text("Payment must be larger than 10 !!!") 
            $(".error").show()
        }else {
            $("#submit").attr("disabled",false); 
            $(".error").hide() 
        }
        if(parseFloat($(this).val()) > parseFloat($("#salary").val())){
            $(".warning").text("Payment must be smaller than basic salary !!") 
            $(".warning").show()
        }else{
            $(".warning").hide()
        }
    });
});