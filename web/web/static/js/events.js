/* Events js */


function initEvents() {
    var monthArray = new Array();
        monthArray[1] = "January";
        monthArray[2] = "February";
        monthArray[3] = "March";
        monthArray[4] = "April";
        monthArray[5] = "May";
        monthArray[6] = "June";
        monthArray[7] = "July";
        monthArray[8] = "August";
        monthArray[9] = "September";
        monthArray[10] = "October";
        monthArray[11] = "November";
        monthArray[12] = "December";

    $("#id_prev_month").click(function() {
        var currentMonthYear = $("#id_current_month").text().split(" ");
        var month = currentMonthYear[0];
        var year = currentMonthYear[1];
        var monthIndex = monthArray.indexOf(month);
        var monthIndexChange;
        if (!(monthIndex==1)) {
            monthIndexChange = monthIndex - 1;
            monthChange = monthArray[monthIndexChange];
        } else {
            monthIndexChange = 12;
            monthChange = "December";
            year = (parseInt(year) - 1).toString();
        }
        $("#id_current_month").text(monthChange + " " + year);
        $("#id_events_list_" + year + "_" + monthIndexChange.toString()).show().siblings("div.events-list").hide();
    });

    $("#id_next_month").click(function() {
        var currentMonthYear = $("#id_current_month").text().split(" ");
        var month = currentMonthYear[0];
        var year = currentMonthYear[1];
        var monthIndex = monthArray.indexOf(month);
        var monthIndexChange;
        if (!(monthIndex==12)) {
            monthIndexChange = monthIndex + 1;
            monthChange = monthArray[monthIndexChange];
        } else {
            monthIndexChange = 1;
            monthChange = "January";
            year = (parseInt(year) + 1).toString();
        }
        $("#id_current_month").text(monthChange + " " + year);
        $("#id_events_list_" + year + "_" + monthIndexChange.toString()).show().siblings("div.events-list").hide();
    });

    $("#id_passed_events").click(function() {
        $("#id_events_list_passed").show().siblings("div.events-list").hide();
    });

    $("#id_coming_events").click(function() {
        $("#id_events_list_coming").show().siblings("div.events-list").hide();
    });
};

initEvents();