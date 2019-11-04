
$("#search-course").on("keyup",function(eve){
    let key_word = $(this).val();
    eve.preventDefault();
    if(key_word.length > 0){
        getCourse(key_word);
    }else{
        getCourse('all');
    } 
});
  
function getCourse(key_word){  
    fetch("/api/educate/get/" + key_word)
        .then(function( response ) {
            response.json().then(function(result) {
                if(result.status){
                    let str = "";
                    for(item in result['data']){  
                        str +="<tr>"+ 
                        
                        "<td><a href='/educate/info/"+ result['data'][item].id +"'>"+ result['data'][item].id_course +"</a></td>"+
                        "<td>"+ result['data'][item].name +"</td>"+
                        "<td>"+ result['data'][item].start_date +"</td>"+
                        "<td>"+ result['data'][item].finish_date +"</td>"+  
                        "<td>"+ result['data'][item].shift +"</td>"+
                        "<td>"+ result['data'][item].teacher +"</td>"+
                        "<td>"+ result['data'][item].tuition +"</td>" 
                        if (result['data'][item].is_activate){
                            str += "<td><div class='circle check'></div></td>"
                        }else{
                            str +=  "<td><div class='circle uncheck'></div></td>"
                        } 
                        str += "<td><a href='/educate/info/"+ result['data'][item].id +"'><i class='fas fa-edit'></i></a></td>"+
                        
                        " </tr>";
                    } 
                    $("#body-table-course").html(str); 
                } 
            });
    }); 
}