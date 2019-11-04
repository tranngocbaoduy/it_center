$(document).ready(function(){
    $("#next_pay").on("keyup",function(){
        check_tuition();
    }); 
}) 

function check_tuition(){
    let temp = parseFloat($("#next_pay").val()); 
    if( temp <0 ){
        $(".error").text("Input must be larger than 0 !!!") 
        $(".error").show()
        $("#submit").attr("disabled","disabled");
        // $("#reservate_tuition").val(0) 
    }else{
        $("#submit").attr("disabled",false);
        $(".error").hide()
    }
    if( temp + parseFloat($("#reservate_tuition").val()) > parseFloat($("#course_tuition").val()) ){
        $("#money_return").val(Math.abs(parseFloat($("#course_tuition").val() - parseFloat($("#reservate_tuition").val()) - temp))+ " $")
    }else{
        $("#money_return").val(0)
    }
   
} 