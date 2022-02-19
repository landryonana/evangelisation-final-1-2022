

$(function() {
    
    //addd zoom button in table
    $('#btn-zoom-plus').click(function(e){
        var zoomMin = $('#person-evang').css('zoom');
        zoom = parseFloat(zoomMin);
        if (zoom>=1) {
            $('#person-evang').css('zoom', 1.0);
            alert(`Zoom max atteint : ${zoom}`); 

        } else {
            $('#person-evang').css('zoom', zoom+0.1);
        }
           
    });

    $('#btn-zoom-moins').click(function(e){
        var zoomMin = 0;
        var zoomMax = $('#person-evang').css('zoom');
        zoom = parseFloat(zoomMax);
        if (zoom<=zoomMin) {
            $('#person-evang').css('zoom', zoom); 
            alert(`Zoom minimum atteint : ${zoom}`); 
        } else {
            $('#person-evang').css('zoom', zoom-0.1);
            zoomMin = $('#person-evang').css('zoom');
        }    
    });


    //==========================rechercher bar================
    $('#empty-result').html('');
    $('#query').keyup(function(){
        var input = $(this).val();
        query = {
            name: $(this).attr('name'),
            value: $(this).val()
        }
        if(input.length>0){
            $.ajax({
                url: $(this).attr("data-url"),
                type:'get',
                dataType:'json',
                data: query,
                beforeSend:function(){
                    $('#spinner').addClass('active');
                },
                success:function(data){
                    $('#spinner').removeClass('active');
                    $('#person-evang tbody').html(data.models);
                    console.log(data.models)
                    $('#result-search').html(data.counter_str);
                    if (data.counter == 0) {
                        $('#empty-result').html(data.empty_result);
                    } else {
                        $('#empty-result').html('');
                    }
                }
            });
        }else{
            $.ajax({
                url: $(this).attr("data-url"),
                type:'get',
                dataType:'json',
                beforeSend:function(){
                    $('#spinner').addClass('active');
                },
                success:function(data){
                    $('#spinner').removeClass('active');
                    $('#person-evang tbody').html(data.models);
                    $('#result-search').html("");
                }
            })
        }
        
    });


    $(".btn-ajax-operations").click(()=>{
        $('#modal-form').modal('show');
        console.log("======= : ",$(this).attr('data-url'));
    });


});