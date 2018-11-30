/* Events list js */

function initCalendar() {

    var events_data;
    $.ajax({
        url: "/events/datelist/",
        type: "GET",
        setTimeout: 15000,
        async : false,
        success: function(response) {
            if (response.error_code) {
                events_data = response.result;
            }
        }
    });

    console.log("events_data: " + events_data)

    $('#calendar').fullCalendar({
        defaultView: 'month',
        height: 'auto',
        header: {
                  left: '',
                  center: 'prev title next',
                  right: ''
                },
        displayEventTime:true,
        displayEventEnd:true,
        weekMode:"liquid",
        aspectRatio:2,
        allDaySlot:false,
        timeFormat: 'HH:mm',
        locale:'zh-cn',
        events: events_data,
        eventClick: function(event) {
            console.log("event: " + event.url)
            if (event.url) {
              window.href.location(event.url);
              return false;
            }
        }
    })
};
