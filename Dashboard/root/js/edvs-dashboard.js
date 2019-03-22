/**
 * Copyright (C) 2019  Team 17
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published
 * by the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

try {
    var tableRef = document.getElementById('alertTable').getElementsByTagName('tbody')[0];
} catch (e) {
}

var table;
var alertList = [""];
const maxAlerts = 100;
var alertPage = (document.getElementById('alertTable') != null);
let barGraphData = [0, 0, 0, 0, 0, 0];

// Setting page appearances
$('#accordionSidebar').load('element_sidebar.html');
$('#topBar').load('element_topbar.html');
$('#footer').load('element_footer.html');

if ($(window).width() < 960) {
    $("body").toggleClass("sidebar-toggled");
    $(".sidebar").toggleClass("toggled");
    if ($(".sidebar").hasClass("toggled")) {
        $('.sidebar .collapse').collapse('hide');
    }
}


function escapeHtml(unsafe) {
    return decodeURI(unsafe)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


function playAudio(elem) {
    if (elem.audio !== undefined) {

        if ($(elem).hasClass('fa-play')) {
            $(elem).removeClass('fa-play');
            $(elem).addClass('fa-pause');
            elem.audio.play();
        } else {
            $(elem).removeClass('fa-pause');
            $(elem).addClass('fa-play');
            elem.audio.pause();
        }

    } else {
        var jqxhr = $.getJSON("/api/alerts/" + elem.getAttribute("idd"))
            .done(function (json) {
                elem.audio = new Audio("data:audio/wav;base64," + json["file"]);
                elem.audio.onended = function () {
                    $(elem).removeClass('fa-pause');
                    $(elem).addClass('fa-play');
                };
                $(elem).removeClass('fa-play');
                $(elem).addClass('fa-pause');
                elem.audio.play();
            })
            .fail(function (err) {
                alert(err.responseText);
                window.location.replace("/login");
            });

    }
}


function updateAlerts(first_update) {
    var jqxhr = $.getJSON("/api/alerts/?file=none&limit=" + maxAlerts)
        .done(function (json) {
            var start = first_update;

            latest = alertList[0]["_id"];
            alertList = [...json];
            while (json.length > 0) {
                var item = json.pop();
                now = new Date(Date.now());
                thisweekstart = new Date(now);
                thisweekstart.setDate(thisweekstart.getDate() - thisweekstart.getDay());
                thisweekstart.setMilliseconds(0);
                thisweekstart.setSeconds(0);
                thisweekstart.setMinutes(0);
                thisweekstart.setHours(0);
                createdat = new Date(item["createdAt"]);
                if (createdat.getFullYear() * 12 + createdat.getMonth() === now.getFullYear() * 12 + now.getMonth() - 1) {
                    barGraphData[0]++;
                }
                if (createdat.getFullYear() * 12 + createdat.getMonth() === now.getFullYear() * 12 + now.getMonth()) {
                    barGraphData[1]++;
                }
                if (createdat < thisweekstart && createdat > thisweekstart - 604800000) {
                    barGraphData[2]++;
                }
                if (createdat > thisweekstart) {
                    barGraphData[3]++;
                }
                if (createdat > thisweekstart && (createdat.getDate() === (now.getDate() - 1))) {
                    barGraphData[4]++;
                }
                if (createdat > thisweekstart && (createdat.getDate() === now.getDate())) {
                    barGraphData[5]++;
                }


                if (alertPage) {
                    if (start) {
                        table.row.add([item["_id"],
                            "<pre>" + escapeHtml(item["content"]) + "</pre>",
                            "<p viewed='" + escapeHtml(item["viewed"]) + "'>" + escapeHtml(item["location"]) + "</p>",
                            new Date(item["createdAt"]),
                            "<a style='font-size: 100%;cursor: pointer;' idd='" + item["_id"] + "' class='fa fa-play' onclick='playAudio(this)'></a>"]);
                    } else if (item["_id"] == latest) {
                        start = true;
                    }
                } else {
                    if (!item["viewed"]) {
                        document.getElementById('alertsSidebarButton').style.color = 'tomato';
                        document.getElementById('alertsSidebarButton').classList.add('blink');
                    }
                }
            }
            if (alertPage) {
                table.draw();
            }

            if (window.location.pathname === "/") {
                var ctx = document.getElementById('myAreaChart').getContext('2d');
                var myChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: ['Last month', 'This month', 'Last week', 'This week', 'Yesterday', 'Today'],
                        datasets: [{
                            label: '# of Alerts',
                            data: [barGraphData[0], barGraphData[1], barGraphData[2], barGraphData[3], barGraphData[4], barGraphData[5]],
                            backgroundColor: [
                                'rgba(255, 99, 132, 0.2)',
                                'rgba(54, 162, 235, 0.2)',
                                'rgba(255, 206, 86, 0.2)',
                                'rgba(75, 192, 192, 0.2)',
                                'rgba(153, 102, 255, 0.2)',
                                'rgba(255, 159, 64, 0.2)'
                            ],
                            borderColor: [
                                'rgba(255, 99, 132, 1)',
                                'rgba(54, 162, 235, 1)',
                                'rgba(255, 206, 86, 1)',
                                'rgba(75, 192, 192, 1)',
                                'rgba(153, 102, 255, 1)',
                                'rgba(255, 159, 64, 1)'
                            ],
                            borderWidth: 1
                        }]
                    }
                });
                var ctx2 = document.getElementById('myDonutChart').getContext('2d');
                var myDoughnutChart = new Chart(ctx2, {
                    type: 'doughnut',
                    data: {
                        labels: ['Last month', 'This month', 'Last week', 'This week', 'Yesterday', 'Today'],
                        datasets: [{
                            label: '# of Alerts',
                            data: [barGraphData[0], barGraphData[1], barGraphData[2], barGraphData[3], barGraphData[4], barGraphData[5]],
                            backgroundColor: [
                                'rgba(255, 99, 132, 0.2)',
                                'rgba(54, 162, 235, 0.2)',
                                'rgba(255, 206, 86, 0.2)',
                                'rgba(75, 192, 192, 0.2)',
                                'rgba(153, 102, 255, 0.2)',
                                'rgba(255, 159, 64, 0.2)'
                            ],
                            borderColor: [
                                'rgba(255, 99, 132, 1)',
                                'rgba(54, 162, 235, 1)',
                                'rgba(255, 206, 86, 1)',
                                'rgba(75, 192, 192, 1)',
                                'rgba(153, 102, 255, 1)',
                                'rgba(255, 159, 64, 1)'
                            ],
                            borderWidth: 1
                        }]
                    }
                });
            }
        })
        .fail(function (err) {
            alert(err.responseText);
            window.location.replace("/login");
        });

}

//change this will not work when operating at alert limit (change to get newest alert and compare ids)
function checkForAlerts(first_update) {
    if (first_update) {
        if (alertPage) {
            table = $('#alertTable').DataTable({
                "createdRow": function (row, data, dataIndex) {
                    if ($(row.cells[1].children[0]).attr("viewed") == "false") {
                        $(row).attr('class', "highlight");
                    }
                    $(row).attr('onclick', '(function(elem){ elem.classList.remove("highlight"); })(this);');
                },
                responsive: true,
                autoWidth: true,
                scrollX: true,
                order: [[3, "desc"]]
            });
            table.column(0).visible(false);
        }
        updateAlerts(first_update);
    } else {
        var newXhr = $.getJSON("/api/alerts/?file=none&limit=1")
            .done(function (json) {

                if ((alertList != [""]) && (json[0]["_id"] != alertList[0]["_id"])) {
                    // if(!alertPage) {
                    //     document.getElementById('alertsSidebarButton').style.color = 'tomato';
                    //     document.getElementById('alertsSidebarButton').classList.add('blink');
                    // }
                    updateAlerts(first_update);
                }

            })
            .fail(function (err) {
                alert(err.responseText);
                window.location.replace("/login");
            });
    }
}

function documentReady() {

    checkForAlerts(true);
    setInterval(() => {
        checkForAlerts(false);
    }, 5000); //check for new alerts every 5 seconds

}

function updateDeviceTable() {

    // Still checks alerts in background
    documentReady();

    // Initialise a DataTable object
    let deviceTable = $('#deviceTable').DataTable({
        order: [[3, "desc"]]
    });
    deviceTable.column(0).visible(false);

    // Fetch JSON file containing user data, but omitting passwords
    let userList = $.getJSON("/listdevices")
        .done((list) => {
            while (list.length > 0) {
                let item = list.pop();
                // If current time is less than 5 min (300000 ms) from last seen time, then it counts as ONLINE.
                let isOnline = Date.now() - new Date(item["lastSeen"]) < 300000;
                deviceTable.row.add([
                    item['_id'],
                    item["username"],
                    isOnline ? "online" : "offline",
                    new Date(item["lastSeen"])
                ]);
            }
            deviceTable.draw(false);
        })
        // In case the .done branch fails
        .fail(function (err) {
            alert(err.responseText);
            window.location.replace("/login");
        });
}

function updateUserTable() {
    // Still checks alerts in background
    documentReady();

    // Initialise a DataTable object
    let userTable = $('#userTable').DataTable({
        order: [[2, "desc"]]
    });
    userTable.column(0).visible(false);

    // Fetch JSON file containing user data, but omitting passwords
    let userList = $.getJSON("/listusers")
        .done((list) => {
            while (list.length > 0) {
                let item = list.pop();
                if (item["authlevel"] != 1) {
                    userTable.row.add([
                        item['_id'],
                        item["username"],
                        new Date(item["lastSeen"])
                    ]);
                }
            }
            userTable.draw(false);
        })
        // In case the .done branch fails
        .fail(function (err) {
            alert(err.responseText);
            window.location.replace("/login");
        });

}

