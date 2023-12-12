
$(document).ready(function() {

    $('#additembtn').click(function() {
        let itemid=$('.items').length+1;
        let adftr=$('.items').length;
        let the_itm=`<tr id="item${itemid}" class="items">
        <td>${itemid}</td>
        <td><input type="text" style="border-style:none;"></td>
        <td><input type="number" name="" id="iq${itemid}" min="0" value="0" style="border-style:none;" onchange="itemfunct(this)"></td>
        <td><input type="number" name="" id="ipu${itemid}" min="0" value="0" style="border-style:none;" onchange="itemfunct(this)"></td>
        <td id="itt${itemid}">0</td>
      </tr>`;
        $('#item'+adftr).after(the_itm);
    });


    $('#addmanpbtn').click(function() {
        let itemid=$('.mans').length+1;
        let adftr=$('.mans').length;
        let the_itm=`<tr id="manp${itemid}" class="mans">
        <td>${itemid}</td>
        <td><input type="text" style="border-style:none;"></td>
        <td><input type="number" name="" id="mq${itemid}" min="0" value="0" style="border-style:none;" onchange="manpfunct(this)"></td>
        <td><input type="number" name="" id="mppu${itemid}" min="0" value="0" style="border-style:none;" onchange="manpfunct(this)"></td>
        <td id="mtt${itemid}">0</td>
      </tr>`;
        $('#manp'+adftr).after(the_itm);
    });

});

function itemfunct(itemid){
    let itemIdNumber =`${itemid.id}`.slice(-1)
    let qty= Number.parseInt( $('#iq'+itemIdNumber).val() );
    let pu= Number.parseInt( $('#ipu'+itemIdNumber).val() );
    let qpu=qty*pu;
    if(!isNaN(qpu)){

        $('#itt'+itemIdNumber).text(qpu);
        let currentTT1= Number.parseInt( $('#ittps').text() );
        let newTT1= currentTT1 + qpu;
        $('#ittps').text(newTT1)
        let currentTT3= Number.parseInt( $('#total3').text() );
        let newTT3= currentTT3+qpu
        let newVAT=newTT3*0.18
        let finalTT4=newTT3+newVAT
        $('#total3').text(newTT3)
        $('#vat').text( (newVAT).toFixed(1) )
        $('#total4').text((finalTT4).toFixed(1))

        $.ajax('/wordsToNumbers',
            {
                data: {word:finalTT4},
                success: function(data) {
                    $('#wrdamt').text(data+"  Rwandan Francs")
                },
                error: function(xhr,status,msg) {
                    alert(msg);
                },
            });
    }
        
    
}


function manpfunct(itemid){
    let itemIdNumber =`${itemid.id}`.slice(-1)
    let qty= Number.parseInt( $('#mq'+itemIdNumber).val() );
    let pu= Number.parseInt( $('#mppu'+itemIdNumber).val() );
    let qpu=qty*pu;
    if(!isNaN(qpu)){

        $('#mtt'+itemIdNumber).text(qpu);
        let currentTT1= Number.parseInt( $('#mttps').text() );
        let newTT1= currentTT1 + qpu;
        $('#mttps').text(newTT1)
        let currentTT3= Number.parseInt( $('#total3').text() );
        let newTT3= currentTT3+qpu
        let newVAT=newTT3*0.18
        let finalTT4=newTT3+newVAT
        $('#total3').text(newTT3)
        $('#vat').text( (newVAT).toFixed(1) )
        $('#total4').text((finalTT4).toFixed(1))


        $.ajax('/wordsToNumbers',
            {
                data: {word:finalTT4},
                success: function(data) {
                    $('#wrdamt').text(data+" Rwandan Francs")
                },
                error: function(xhr,status,msg) {
                    alert(msg);
                },
            });
    }
        
    
}


function convert_Html(){

    const elemnt=document.getElementById('contentToPrint');
    html2pdf()
    .from(elemnt)
    .save('WASAC-BOQ');
}
