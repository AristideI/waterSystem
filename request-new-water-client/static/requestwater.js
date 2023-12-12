
$(document).ready(function() {

    $('#prov').change(function() {
        province =$('#prov').val();
        $('#distr').empty();
        $('#sect').empty();
        $('#cell').empty();
        $('#bra').empty();
        if(province!='choose'){

            $.ajax('/provinceName',
            {
                data: {province:province},
                success: function(data) {
                    $('#distr').append('<option>choose</option>')
                    for(let i of data){
                        $('#distr').append('<option>'+i.name+'</option>')
                    }
                },
                error: function(xhr,status,msg) {
                    alert(msg);
                },
            });
        }
    });


    $('#distr').change(function() {
        district =$('#distr').val();
        $('#sect').empty();
        $('#cell').empty();
        $('#bra').empty();
        if(district!='choose'){

            $.ajax('/districtName',
            {
                data: {district:district},
                success: function(data) {
                    $('#sect').append('<option>choose</option>')
                    for(let i of data.sectors){
                        $('#sect').append('<option value="'+i._id+'">'+i.name+'</option>')
                    }
                },
                error: function(xhr,status,msg) {
                    alert(msg);
                },
            });
        }
    });


    $('#sect').change(function() {
        sector =$('#sect').val();
        $('#cell').empty();
        $('#bra').empty();
        if(sector!='choose'){

            $.ajax('/sectorName',
            {
                data: {sector:sector},
                success: function(data) {
                    for(let i of data.cells){
                        $('#cell').append('<option>'+i.name+'</option>')
                    }

                    $('#bra').append('<option value="'+data.branch_code+'">'+data.branch.name+'</option>')
                    
                },
                error: function(xhr,status,msg) {
                    alert(msg);
                },
            });
        }
    });


});