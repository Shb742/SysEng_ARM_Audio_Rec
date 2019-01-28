var tableRef = document.getElementById('Alerts').getElementsByTagName('tbody')[0];
var table;
var latestAlert;
const maxAlerts = 100;


function escapeHtml(unsafe) {
    return decodeURI(unsafe)
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
            //find index of newest current one
            var latest = "";
            var start = true;
            if (!first_update && (tableRef.rows.length != 0)) {
                var latest = table.rows( { order: "index" } ).data().reverse()[0][0];//$(table.rows( { order: "index" } ).data().reverse()[0][0])[0].innerText;
                start = false;
            }

            while (json.length > 0) {
                var item = json.pop();
                if (start){
                    table.row.add([item["_id"],"<pre>"+escapeHtml(item["content"])+"</pre>","<p first='"+first_update+"'>"+escapeHtml(item["location"])+"</p>" ,new Date(item["createdAt"]),"<a style='font-size: 100%;cursor: pointer;' idd='"+item["_id"]+"' class='fa fa-play' onclick='playAudio(this)'></a>"]);
                }else if(item["_id"] == latest){
                    start = true;
                }
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
                if ( $(row.cells[1].children[0]).attr("first") == "false" ){
                    $(row).attr('class',"highlight");
                }
                $(row).attr('style',"text-align: center;vertical-align: middle;");
                $(row).attr('onclick','(function(elem){ elem.classList.remove("highlight"); })(this);');
            },
            responsive: true,
            autoWidth: true,
            scrollX: true,
            order: [[ 3, "desc" ]]
        });
        table.column(0).visible(false);
        updateAlerts(first_update);
    }else{
        var newXhr = $.getJSON( "/api/alerts/?file=none&limit=1")
        .done(function(json) {
            if (json[0]["_id"] != table.rows( { order: "index" } ).data().reverse()[0][0]){//$(table.rows( { order: "index" } ).data().reverse()[0][0])[0].innerText) {
                updateAlerts(first_update);
            }

        })
        .fail(function(err) {
                alert(err.responseText);
                window.location.replace("/pages/login.html");
        });
    }
}

function updateUserStatus() {

    // Initialise a DataTable object
    let userTable = $('#Users').DataTable();

    // Fetch json file containing user data, but omitting passwords
    let userList = $.getJSON("/listusers?password=none")
        .done(function (list) {
            while (list.length > 0) {
                let item = list.pop();
                // If current time is less than 5 min (300000 ms) from last seen time, then it counts as ONLINE.
                let isOnline = Date.now() - new Date(item["lastSeen"]) < 300000;
                userTable.row.add([
                    item["username"],
                    isOnline ? "online" : "offline",
                    item["lastSeen"]
                ]);
            }
            userTable.draw(false);
        })
        // In case the .done branch fails
        .fail(function (err) {
            alert(err.responseText);
            window.location.replace("/pages/login.html");
        });
}

function documentReady(){
    checkForAlerts(true);
    updateUserStatus();
    setInterval(function(){
        checkForAlerts(false);
        }, 15000); //check for new alerts every 15 seconds

}
