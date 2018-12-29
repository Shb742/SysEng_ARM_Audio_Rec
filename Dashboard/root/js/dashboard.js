var tableRef = document.getElementById('Alerts').getElementsByTagName('tbody')[0];
var table;
var latestAlert;
const alertsPerPage = 10;
var totalAlerts = 0;
var newAlerts = 0;

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
            alert( "error" );
            window.location.replace("/pages/login.html");
        });
       
    }
}


function updateAlerts(page_num,update){
    if ((page_num * alertsPerPage)<totalAlerts){
        var jqxhr = $.getJSON( "/api/alerts/?file=none&limit="+alertsPerPage+"&skip="+(page_num*alertsPerPage))
          .done(function(json) {
            for (newAlerts;newAlerts>0;newAlerts--){
                var item = json.pop();
                table.row.add([item["_id"],item["content"],item["location"],new Date(item["createdAt"]).toString(),"<a style='font-size: 100%;cursor: pointer;' idd='"+item["_id"]+"' class='fa fa-play' onclick='playAudio(this)'></a>"]).draw();
                if(update == false){
                    tableRef.rows[0].classList.remove("highlight");//don't have highlight animation on first load
                }
            }
          })
          .fail(function(err) {
            alert( "error" );
            window.location.replace("/pages/login.html");
        });
    }
    
}

//change this will not work when operating at alert limit (change to get newest alert and compare ids)
function checkForAlerts(update){
    var jqxhr = $.getJSON( "/api/alerts/count/")
      .done(function(json) {
        newAlerts = json["TotalAlerts"] - totalAlerts;
        totalAlerts = json["TotalAlerts"];
        updateAlerts(0,update)
      })
      .fail(function() {
        alert( "error" );
        window.location.replace("/pages/login.html");
      });
}


 $(document).ready(function() {
    //set up alerts table
    table = $('#Alerts').DataTable({
        "createdRow": function(row, data, dataIndex) {
        $(row).attr('style',"text-align: center;vertical-align: middle;");
        $(row).attr('class',"highlight");
        $(row).attr('onclick','(function(elem){ elem.classList.remove("highlight"); })(this);');
        },
        responsive: true,
        order: [[ 3, "desc" ]]
    });
    checkForAlerts(false);
    setInterval(function(){checkForAlerts(true); }, 30000);//check for new alerts every half-minute
    
});





