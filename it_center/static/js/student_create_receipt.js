$(document).ready(function(){
    load();
    $("#submit").attr("disabled","disabled"); 
})
$("#course").on("change", function() {
    fetch_data()
});

function fetch_data(e){
    let id_student = $("#id-student").val();
    console.log(id_student)
    fetch("/api/educate/" + $("#course option:selected").val())
        .then(function( response ) {
            response.json().then(function(result) {
                if(result.status){ 
                    $("#course_tuition").val(result.data.tuition) 
                    $("#course_name").val(result.data.name)
                   
                    let id = result.data.shift['$oid'] 
                    fetch("/api/shift/" + id)
                        .then(function( response ) {
                            response.json().then(function(result) {
                                if(result.status){ 
                                    $("#shift").val(result.data.name +' | from '+ result.data.start+' to ' +result.data.finish)
                                } else{
                                    $("#shift").val("Can\'t find shift, you should reload this page !! ")
                                } 
                            });
                    }); 
                    for(item of result.data.list_student){
                        if(item['$oid'] == id_student){
                            $(".error").text( $(".error").val() + " This student is exist in that class !!!") 
                            $(".error").show()
                            $("#reservate_tuition").attr('readonly',true)
                            $("#submit").attr("disabled","disabled"); 
                            return
                        }  
                    }
                    $("#reservate_tuition").attr('readonly',false) 
                    check_tuition(); 
                }
            });
    }); 
}

$("#reservate_tuition").on("keyup",function(){ 
    check_tuition();
    if(parseFloat($("#course_tuition").val() < parseFloat($("#reservate_tuition").val()))){
        $("#money_return").val(Math.abs(parseFloat($("#course_tuition").val() - parseFloat($("#reservate_tuition").val())))+ " $")
    } 
});


function check_tuition(){
    let temp = parseFloat($("#reservate_tuition").val()); 
    if( temp <= 0 || $("#reservate_tuition").val() == ""){
        $(".error").text("Reservate tuition must be larger than 0 !!!") 
        $(".error").show()
        $("#submit").attr("disabled","disabled");
        // $("#reservate_tuition").val(0) 
    } else if( temp < (parseFloat($("#course_tuition").val()) /3 )){
        $(".error").text("Reservate tuition must be larger than one by third tuition of course !!!") 
        $(".error").show()
        $("#submit").attr("disabled","disabled");
        // $("#reservate_tuition").val(0) 
    }else{
        $("#submit").attr("disabled",false);
        $(".error").hide()
    }
}
function load(){
    fetch_data(); 
    check_tuition();
}