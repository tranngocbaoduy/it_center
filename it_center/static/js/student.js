let path = '/static/profile_pics/';
$("#search-student").on("keyup",function(eve){
    let key_word = $(this).val();
    eve.preventDefault();
    if(key_word.length > 0){
        getStudent(key_word);
    }else{
        getStudent('all');
    } 
});
 
$("#search-removed-student").on("keyup",function(eve){
    let key_word = $(this).val();
    eve.preventDefault();
    if(key_word.length > 0){
        getRemoveStudent(key_word);
    }else{
        getRemoveStudent('all');
    } 
});

function getRemoveStudent(key_word){  
    fetch("/api/student/get_remove/" + key_word)
        .then(function( response ) {
            response.json().then(function(result) {
                if(result.status){
                    let str = "";
                    for(item in result['data']){ 
                        str +="<tr>"+ 
                        "<td><a href='/student/info/"+ result['data'][item].id +"'>"+ result['data'][item].first_name + ' '+ result['data'][item].last_name +"</a></td>"+
                        "<td>"+ result['data'][item].phone +"</td>"+
                        "<td>"+ result['data'][item].email +"</td>"+
                        "<td>"+ result['data'][item].address +"</td>"+  
                        "<td>"+ result['data'][item].birth +"</td>"+
                        "<td>"+ result['data'][item].gender +"</td>"+
                        "<td><img  alt='avatar' src='"+ path+ result['data'][item].image_file +"' class='student-img'></img></td>"
                        if (result['data'][item].is_activate){
                            str += "<td><div class='circle check'></div></td>"
                        }else{
                            str +=  "<td><div class='circle uncheck'></div></td>"
                        } 
                        str += "<td><a href='/student/info/"+ result['data'][item].id +"'><i class='fas fa-edit'></i></a></td>"+
                        
                        " </tr>";
                    } 
                    $("#body-table-student").html(str);
                    // $("#table-detail-receipt").toggle("slow");
                    // $('html, body').animate({
                    //     scrollTop: $("#body-table-student").offset().top
                    // }, 2000);
                } 
            });
    }); 
}

function getStudent(key_word){  
    fetch("/api/student/get/" + key_word)
        .then(function( response ) {
            response.json().then(function(result) {
                if(result.status){
                    let str = "";
                    for(item in result['data']){ 
                        str +="<tr>"+ 
                        "<td><a href='/student/info/"+ result['data'][item].id +"'>"+ result['data'][item].first_name + ' '+ result['data'][item].last_name +"</a></td>"+
                        "<td>"+ result['data'][item].phone +"</td>"+
                        "<td>"+ result['data'][item].email +"</td>"+
                        "<td>"+ result['data'][item].address +"</td>"+  
                        "<td>"+ result['data'][item].birth +"</td>"+
                        "<td>"+ result['data'][item].gender +"</td>"+
                        "<td><img  alt='avatar' src='"+ path+ result['data'][item].image_file +"' class='student-img'></img></td>"
                       
                        str += "<td><a href='/student/info/"+ result['data'][item].id +"'><i class='fas fa-edit'></i></a></td>"+
                        
                        " </tr>";
                    } 
                    $("#body-table-student").html(str);
                    // $("#table-detail-receipt").toggle("slow");
                    // $('html, body').animate({
                    //     scrollTop: $("#body-table-student").offset().top
                    // }, 2000);
                } 
            });
    }); 
}