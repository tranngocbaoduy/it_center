let path = '/static/profile_pics/';
$("#search-staff").on("keyup",function(eve){
    let key_word = $(this).val();
    eve.preventDefault();
    if(key_word.length > 0){
        getStaff(key_word);
    }else{
        getStaff('all');
    } 
});
 
$("#search-removed-staff").on("keyup",function(eve){
    let key_word = $(this).val();
    eve.preventDefault();
    if(key_word.length > 0){
        getRemoveStaff(key_word);
    }else{
        getRemoveStaff('all');
    } 
}); 

$("#search-inactived-staff").on("keyup",function(eve){
    let key_word = $(this).val();
    eve.preventDefault();
    if(key_word.length > 0){
        getInactiveStaff(key_word);
    }else{
        getInactiveStaff('all');
    } 
});

function getInactiveStaff(key_word){
    fetch("/api/staff/get_inactived/" + key_word)
        .then(function( response ) {
        response.json().then(function(result) {
            if(result.status){
                let str = "";
                for(item in result['data']){ 
                    let link = "<a href='/staff/info/"+ result['data'][item].id +"'>";
                    str +="<tr>"+ 
                    "<td>"+ link+ result['data'][item].first_name + ' '+ result['data'][item].last_name +"</a></td>"+
                    "<td>"+ result['data'][item].phone +"</td>"+
                    "<td>"+ result['data'][item].email +"</td>"+
                    "<td>"+ result['data'][item].address +"</td>"+  
                    "<td>"+ result['data'][item].birth +"</td>"+
                    "<td>"+ result['data'][item].gender +"</td>"+
                    "<td>"+ result['data'][item].role +"</td>"+
                    "<td><img  alt='avatar' src='"+ path + result['data'][item].image_file +"' class='staff-img'></img></td>"
                    if (result['data'][item].is_activate){
                        str += "<td><div class='circle check'></div></td>"
                    }else{
                        str +=  "<td><div class='circle uncheck'></div></td>"
                    } 
                    str += "<td><a href='/staff/info/"+ result['data'][item].id +"'><i class='fas fa-edit'></i></a></td>"+
                    
                    " </tr>";
                } 
                $("#body-table-staff").html(str);
                // $("#table-detail-receipt").toggle("slow");
                // $('html, body').animate({
                //     scrollTop: $("#body-table-staff").offset().top
                // }, 2000);
            } 
        });
    }); 
}

function getRemoveStaff(key_word){  
    fetch("/api/staff/get_removed/" + key_word)
        .then(function( response ) {
            response.json().then(function(result) {
                if(result.status){
                    let str = ""; 
                    for(item in result['data']){ 
                        let link = "<a href='/staff/info/"+ result['data'][item].id +"'>";
                        str +="<tr>"+ 
                        "<td>"+ link+ result['data'][item].first_name + ' '+ result['data'][item].last_name +"</a></td>"+
                        "<td>"+ result['data'][item].phone +"</td>"+
                        "<td>"+ result['data'][item].email +"</td>"+
                        "<td>"+ result['data'][item].address +"</td>"+  
                        "<td>"+ result['data'][item].birth +"</td>"+
                        "<td>"+ result['data'][item].gender +"</td>"+
                        "<td>"+ result['data'][item].role +"</td>"+
                        "<td><img  alt='avatar' src='"+ path + result['data'][item].image_file +"' class='staff-img'></img></td>"
                        if (result['data'][item].is_activate){
                            str += "<td><div class='circle check'></div></td>"
                        }else{
                            str +=  "<td><div class='circle uncheck'></div></td>"
                        } 
                        str += "<td><a href='/staff/info/"+ result['data'][item].id +"'><i class='fas fa-edit'></i></a></td>"+
                        
                        " </tr>";
                    } 
                    $("#body-table-staff").html(str);
                    // $("#table-detail-receipt").toggle("slow");
                    // $('html, body').animate({
                    //     scrollTop: $("#body-table-staff").offset().top
                    // }, 2000);
                } 
            });
    }); 
}

function getStaff(key_word){  
    fetch("/api/staff/get/" + key_word)
        .then(function( response ) {
            response.json().then(function(result) {
                if(result.status){
                    let str = ""; 
                    for(item in result['data']){ 
                        let link = "<a href='/staff/info/"+ result['data'][item].id +"'>";
                        str +="<tr>"+ 
                        "<td>"+ link+ result['data'][item].first_name + ' '+ result['data'][item].last_name +"</a></td>"+
                        "<td>"+ result['data'][item].phone +"</td>"+
                        "<td>"+ result['data'][item].email +"</td>"+
                        "<td>"+ result['data'][item].address +"</td>"+  
                        "<td>"+ result['data'][item].birth +"</td>"+
                        "<td>"+ result['data'][item].gender +"</td>"+
                        "<td>"+ result['data'][item].role +"</td>"+
                        "<td><img  alt='avatar' src='"+ path + result['data'][item].image_file +"' class='staff-img'></img></td>"
                        if (result['data'][item].is_activate){
                            str += "<td><div class='circle check'></div></td>"
                        }else{
                            str +=  "<td><div class='circle uncheck'></div></td>"
                        } 
                        str += "<td><a href='/staff/info/"+ result['data'][item].id +"'><i class='fas fa-edit'></i></a></td>"+
                        
                        " </tr>";
                    } 
                    $("#body-table-staff").html(str);
                    // $("#table-detail-receipt").toggle("slow");
                    // $('html, body').animate({
                    //     scrollTop: $("#body-table-staff").offset().top
                    // }, 2000);
                } 
            });
    }); 
}