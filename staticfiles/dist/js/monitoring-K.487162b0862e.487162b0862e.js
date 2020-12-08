$(document).ready(function(){
    $(".dial").show();
     // ------knob------
    $(".dial").knob({
        readOnly: true,
        bgColor: "#d2d6de",
        fgColor: "#00a65a",
        thickness: 0.2,
        width : 90,
        height :90 ,
                    });
        // ------knob------
    $(".box-content").each(function(){
       var IP = $(this).find('.box-title').html();
       var that = $(this);
       var ramUsed = $(this).find('.ramUsed');
       var resultLoad = $(this).find('.resultLoad');
       var warningIcon = $(this).find('.fa-warning');
       var boxColor = $(this).find('.box')
       var userCpu = $(this).find('.userCpu');
       var cpuBox = $(this).find('.cpuBox');
       var inputDial = $(this).find('.dial');

       $.ajax({
        type: "GET", //rest Type
        data:{
            "ip": IP,
            "server_type": "K",
        },
        // dataType: 'jsonp', //mispelled
        url:  "/monitor/server_status",
        async: true,
        headers:{
            contentType: "application/json"
        },
        success: function (response) {
            if (response.connected == true){
                if(response.status == true){
                    ramUsed.html(response.ram_used + " %");
                    resultLoad.html(response.load + " %");
                    inputDial.val(response.user_cpu);
                    inputDial.trigger('change');
                     inputDial.trigger(
                        'configure',
                        {
                        fgColor: "#00a65a",
                    });
                    inputDial.css("color","#00a65a");
                    boxColor.removeClass('box-default').addClass('box-success');
                    warningIcon.remove();
                } else {
                    ramUsed.html(response.ram_used + " %");
                    resultLoad.html(response.load + " %");
                    inputDial.val(response.user_cpu);
                    inputDial.trigger('change');
                    inputDial.trigger(
                        'configure',
                        {
                        fgColor: "#dd4b39",
                    });
                    inputDial.css("color","#dd4b39");
                    boxColor.removeClass('box-default').addClass('box-danger');
                    warningIcon.remove();
                }
            } else {
                ramUsed.html("no information");
                resultLoad.html("no information");
                cpuBox.remove();
            };

            that.find('.overlay').hide();
        },
        error: function(xhr, ajaxOptions, thrownError){
            console.log(xhr.status);
        }
});
});
});
