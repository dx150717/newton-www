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

    var eventsListMonthly = $(".events-list-monthly");
    var startEventId = eventsListMonthly[0].id;
    var endEventId = eventsListMonthly[eventsListMonthly.length - 1].id;

    $("#id_prev_month").click(function() {
        $("#id_coming_events").removeClass("active");
        $("#id_passed_events").removeClass("active");
        $("#id_passed_events_mobile").removeClass("active");
        var currentMonthYear = $("#id_current_month").text().split(" ");
        var month = currentMonthYear[0];
        var year = currentMonthYear[1];
        var monthIndex = monthArray.indexOf(month);
        var monthIndexChange;

        console.log("#id_events_list_" + year + "_" + monthIndex.toString())
        console.log(startEventId)

        if ("#id_events_list_" + year + "_" + monthIndex.toString() == startEventId) {
            return;
        };
        if (!(monthIndex==1)) {
            monthIndexChange = monthIndex - 1;
        } else {
            monthIndexChange = 12;
            monthChange = "December";
            year = (parseInt(year) - 1).toString();
        };
        var showDom = $("#id_events_list_" + year + "_" + monthIndexChange.toString());
        while(showDom.length == 0) {
            monthIndexChange = monthIndexChange - 1;
            showDom = $("#id_events_list_" + year + "_" + monthIndexChange.toString());
        };
        monthChange = monthArray[monthIndexChange];
        $("#id_current_month").text(monthChange + " " + year);
        showDom.show().siblings("div.events-list").hide();
    });
    $("#id_prev_month_mobile").click(function() {
        $("#id_coming_events_mobile").removeClass("active");
        $("#id_passed_events_mobile").removeClass("active");
        var currentMonthYear = $("#id_current_month_mobile").text().split(" ");
        var month = currentMonthYear[0];
        var year = currentMonthYear[1];
        var monthIndex = monthArray.indexOf(month);
        var monthIndexChange;
        if (monthIndex==5 && year=="2018") {
            return;
        };
        if (!(monthIndex==1)) {
            monthIndexChange = monthIndex - 1;
        } else {
            monthIndexChange = 12;
            monthChange = "December";
            year = (parseInt(year) - 1).toString();
        };
        var showDom = $("#id_events_list_" + year + "_" + monthIndexChange.toString());
        while(showDom.length == 0) {
            monthIndexChange = monthIndexChange - 1;
            showDom = $("#id_events_list_" + year + "_" + monthIndexChange.toString());
        };
        monthChange = monthArray[monthIndexChange];
        $("#id_current_month_mobile").text(monthChange + " " + year);
        $("#id_events_list_" + year + "_" + monthIndexChange + "_mobile".toString()).show().siblings("div.events-list").hide();
    });

    $("#id_next_month").click(function() {
        $("#id_coming_events").removeClass("active");
        $("#id_passed_events").removeClass("active");
        $("#id_passed_events_mobile").removeClass("active");
        var currentMonthYear = $("#id_current_month").text().split(" ");
        var month = currentMonthYear[0];
        var year = currentMonthYear[1];
        var monthIndex = monthArray.indexOf(month);
        var monthIndexChange;
        if (monthIndex==12) {
            return;
        };
        if (!(monthIndex==12)) {
            monthIndexChange = monthIndex + 1;
        } else {
            monthIndexChange = 1;
            monthChange = "January";
            year = (parseInt(year) + 1).toString();
        };
        var showDom = $("#id_events_list_" + year + "_" + monthIndexChange.toString());
        while(showDom.length == 0) {
            monthIndexChange = monthIndexChange + 1;
            showDom = $("#id_events_list_" + year + "_" + monthIndexChange.toString());
        };
        monthChange = monthArray[monthIndexChange];
        $("#id_current_month").text(monthChange + " " + year);
        $("#id_events_list_" + year + "_" + monthIndexChange.toString()).show().siblings("div.events-list").hide();
    });
    $("#id_next_month_mobile").click(function() {
        $("#id_coming_events_mobile").removeClass("active");
        $("#id_passed_events_mobile").removeClass("active");
        var currentMonthYear = $("#id_current_month_mobile").text().split(" ");
        var month = currentMonthYear[0];
        var year = currentMonthYear[1];
        var monthIndex = monthArray.indexOf(month);
        var monthIndexChange;
        if (monthIndex==12) {
            return;
        };
        if (!(monthIndex==12)) {
            monthIndexChange = monthIndex + 1;
        } else {
            monthIndexChange = 1;
            monthChange = "January";
            year = (parseInt(year) + 1).toString();
        };
        var showDom = $("#id_events_list_" + year + "_" + monthIndexChange.toString());
        while(showDom.length == 0) {
            monthIndexChange = monthIndexChange + 1;
            showDom = $("#id_events_list_" + year + "_" + monthIndexChange.toString());
        };
        monthChange = monthArray[monthIndexChange];
        $("#id_current_month_mobile").text(monthChange + " " + year);
        $("#id_events_list_" + year + "_" + monthIndexChange + "_mobile".toString()).show().siblings("div.events-list").hide();
    });


    $("#id_passed_events_mobile").click(function() {
        $(this).addClass("active");
        $("#id_coming_events_mobile").removeClass("active");
        $("#id_events_list_passed_mobile").show().siblings("div.events-list").hide();
    });

    $("#id_passed_events").click(function() {
        $(this).addClass("active");
        $("#id_coming_events").removeClass("active");
        $("#id_events_list_passed").show().siblings("div.events-list").hide();
    });

    $("#id_coming_events").click(function() {
        $(this).addClass("active");
        $("#id_passed_events").removeClass("active");
        $("#id_passed_events_mobile").removeClass("active");
        $("#id_events_list_coming").show().siblings("div.events-list").hide();
    });

    $("#id_coming_events_mobile").click(function() {
        $(this).addClass("active");
        $("#id_passed_events").removeClass("active");
        $("#id_passed_events_mobile").removeClass("active");
        $("#id_events_list_coming_mobile").show().siblings("div.events-list").hide();
    });
};

initEvents();