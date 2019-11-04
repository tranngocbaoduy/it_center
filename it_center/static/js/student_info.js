function getDetailReceipt(el){ 
    let id = jQuery(el).children(":first").val()
    fetch("/api/student/receipt/" + id)
        .then(function( response ) {
            response.json().then(function(result) {
                console.log(result)
                if(result.status){
                    let str = "";
                    for(item in result['data']){ 
                        str +="<tr>"+ 
                        "<td>"+ result['data'][item].id +"</td>"+
                        "<td>"+ result['data'][item].tuition +"</td>"+
                        "<td>"+ result['data'][item].money_return +"</td>"+
                        "<td>"+ result['data'][item].user_name +"</td>"+  
                        "<td>"+ result['data'][item].created_date +"</td>"+
                        " </tr>";
                    } 
                    $("#body-table-detail-receipt").html(str);
                    $("#table-detail-receipt").toggle("slow");
                    $('html, body').animate({
                        scrollTop: $("#table-detail-receipt").offset().top
                    }, 2000);
                } 
            });
    }); 
}