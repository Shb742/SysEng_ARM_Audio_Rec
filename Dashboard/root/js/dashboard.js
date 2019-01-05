var tableRef = document.getElementById('Alerts').getElementsByTagName('tbody')[0];
var table;
var latestAlert;
const maxAlerts = 100;


function escapeHtml(unsafe) {
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
 }


function playAudio(elem){ 
    if (elem.audio != undefined) {

        if($(elem).hasClass('fa-play'))
        {
            $(elem).removeClass('fa-play');
            $(elem).addClass('fa-pause');
            elem.audio.play();
        }
        else
        {
            $(elem).removeClass('fa-pause');
            $(elem).addClass('fa-play');
            elem.audio.pause();
        }

     }else{
        var jqxhr = $.getJSON( "/api/alerts/"+elem.getAttribute("idd"))
          .done(function(json) {
            elem.audio =  new Audio("data:audio/wav;base64," + json["file"] );
            elem.audio.onended = function() {
                $(elem).removeClass('fa-pause');
                $(elem).addClass('fa-play');
            };
            $(elem).removeClass('fa-play');
            $(elem).addClass('fa-pause');
            elem.audio.play();
          })
          .fail(function(err) {
            alert(err.responseText);
            window.location.replace("/pages/login.html");
        });
       
    }
}


function updateAlerts(first_update){
        var jqxhr = $.getJSON( "/api/alerts/?file=none&limit="+maxAlerts)
          .done(function(json) {
            var latest = table.rows( { order: [ 3, "desc" ] } ).row(0).data();
            if (latest != undefined){
                latest = latest[0];
            }
            while ((json.length > 0) && (first_update || (json[0]["_id"] != latest))) {
                var item = json.shift();
                table.row.add([item["_id"],"<pre>"+escapeHtml(item["content"])+"</pre>","<pre>"+escapeHtml(item["location"])+"</pre>" ,new Date(item["createdAt"]).toString(),"<a style='font-size: 100%;cursor: pointer;' first='"+first_update+"' idd='"+item["_id"]+"' class='fa fa-play' onclick='playAudio(this)'></a>"]);
            }
            table.draw();
          })
          .fail(function(err) {
            alert(err.responseText);
            window.location.replace("/pages/login.html");
        });
    
}

//change this will not work when operating at alert limit (change to get newest alert and compare ids)
function checkForAlerts(first_update){
    if (first_update) {
        //set up alerts table
        table = $('#Alerts').DataTable({
            "createdRow": function(row, data, dataIndex) {
                if ( $(row.cells[4].children[0]).attr("first") == "false" ){
                    $(row).attr('class',"highlight");
                }
                $(row).attr('style',"text-align: center;vertical-align: middle;");
                $(row).attr('onclick','(function(elem){ elem.classList.remove("highlight"); })(this);');
            },
            responsive: true,
            autoWidth: true,
            order: [[ 3, "desc" ]]
        });
        updateAlerts(first_update);
    }else{
        var newXhr = $.getJSON( "/api/alerts/?file=none&limit=1")
        .done(function(json) {
            if (json[0]["_id"] != tableRef.rows[0].cells[0].innerText) {
                updateAlerts(first_update);
            }

        })
        .fail(function(err) {
                alert(err.responseText);
                window.location.replace("/pages/login.html");
        });
    }
}

 $(document).ready(function() {
    checkForAlerts(true);
    setInterval(function(){checkForAlerts(false); }, 15000);//check for new alerts every quarter-minute 15000
    
});




