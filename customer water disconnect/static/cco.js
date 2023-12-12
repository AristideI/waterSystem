
function todisplayfun(theval){

    $('#cardtoshow'+theval).show()
   
}

function tohidefun(theval){

    $('#cardtoshow'+theval).hide()
   
}

function toshowSubmitCard(theval){

    $('#cardtoSubmit'+theval).show()
}


function todisplayrsnfun(theval){

    $('#rsntoshow'+theval).show()
   
}

function tohidersnfun(theval){

    $('#rsntoshow'+theval).hide()
   
}


$(document).ready(function(){
    $("#myInput").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $("#myTable tr").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    });
  });


// function tohideSubmitCard(theval){

//     $('#cardtoSubmit'+theval).hide()
// }


// function toSubmitformFunc(theval){

    
//     var fd = new FormData();
//     var files = $('#fl'+theval)[0].files[0];
//     theid=$('#id'+theval).val()
//     fd.append('file', files);
//     // alert(theid)
//     // $.ajax('/saveBOQ',
//     //         {
//     //             data:{theid:theid,file:fd},
//     //             type: 'post',
//     //             contentType: false,
//     //             // processData: false,
//     //             success: function(data) {
//     //                 alert(data)
//     //                 location.reload();
//     //             },
//     //             error: function(xhr,status,msg) {
//     //                 alert(msg);
//     //             },
//     //         });
// }