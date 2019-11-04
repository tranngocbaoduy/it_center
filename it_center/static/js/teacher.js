let path = '/static/profile_pics/';
$("#search-teacher").on("keyup",function(eve){
    let key_word = $(this).val();
    eve.preventDefault();
    if(key_word.length > 0){
        getTeacher(key_word);
    }else{
        getTeacher('all');
    } 
});
 
$("#search-removed-teacher").on("keyup",function(eve){
    let key_word = $(this).val();
    eve.preventDefault();
    if(key_word.length > 0){
        getRemoveTeacher(key_word);
    }else{
        getRemoveTeacher('all');
    } 
});

function getRemoveTeacher(key_word){  
    fetch("/api/teacher/get_remove/" + key_word)
        .then(function( response ) {
            response.json().then(function(result) {
                if(result.status){
                    let str = "";
                    for(item in result['data']){ 
                        str +="<tr>"+ 
                        "<td><a href='/teacher/info/"+ result['data'][item].id +"'>"+ result['data'][item].first_name + ' '+ result['data'][item].last_name +"</a></td>"+
                        "<td>"+ result['data'][item].phone +"</td>"+
                        "<td>"+ result['data'][item].email +"</td>"+
                        "<td>"+ result['data'][item].address +"</td>"+  
                        "<td>"+ result['data'][item].birth +"</td>"+
                        "<td>"+ result['data'][item].gender +"</td>"+
                        "<td><img  alt='avatar' src='"+ path+ result['data'][item].image_file +"' class='teacher-img'></img></td>"
                       
                        str += "<td><a href='/teacher/info/"+ result['data'][item].id +"'><i class='fas fa-edit'></i></a></td>"+
                        
                        " </tr>";
                    } 
                    $("#body-table-teacher").html(str);
                    // $("#table-detail-receipt").toggle("slow");
                    // $('html, body').animate({
                    //     scrollTop: $("#body-table-teacher").offset().top
                    // }, 2000);
                } 
            });
    }); 
}

function getTeacher(key_word){  
    fetch("/api/teacher/get/" + key_word)
        .then(function( response ) {
            response.json().then(function(result) {
                if(result.status){
                    let str = "";
                    for(item in result['data']){ 
                        str +="<tr>"+ 
                        "<td><a href='/teacher/info/"+ result['data'][item].id +"'>"+ result['data'][item].first_name + ' '+ result['data'][item].last_name +"</a></td>"+
                        "<td>"+ result['data'][item].phone +"</td>"+
                        "<td>"+ result['data'][item].email +"</td>"+
                        "<td>"+ result['data'][item].address +"</td>"+  
                        "<td>"+ result['data'][item].birth +"</td>"+
                        "<td>"+ result['data'][item].gender +"</td>"+
                        "<td><img  alt='avatar' src='"+ path+  result['data'][item].image_file +"' class='teacher-img'></img></td>"
                        
                        str += "<td><a href='/teacher/info/"+ result['data'][item].id +"'><i class='fas fa-edit'></i></a></td>"+
                        
                        " </tr>";
                    } 
                    $("#body-table-teacher").html(str);
                    // $("#table-detail-receipt").toggle("slow");
                    // $('html, body').animate({
                    //     scrollTop: $("#body-table-teacher").offset().top
                    // }, 2000);
                } 
            });
    }); 
}