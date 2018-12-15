/* counter js */

function initCounter () {
    var nowDate = new Date();
    var endDate = new Date(2018, 11, 18, 08, 00, 00);
    var timeDelta = endDate - nowDate;
    var intervalId;

    function computeCounter(timeDelta) {
        if (timeDelta < 0) {
            timeDelta = 0;
            window.clearInterval(intervalId);
        }
        var days = Math.floor(timeDelta / (60 * 60 * 24 * 1000));
        var leftHours = timeDelta % (60 * 60 * 24 * 1000);
        var hours = Math.floor(leftHours / (60 * 60 * 1000));
        var leftMinutes = leftHours % (60 * 60 * 1000);
        var minutes = Math.floor(leftMinutes / (60 * 1000));
        var leftSeconds = leftMinutes % (60 * 1000);
        var seconds = Math.floor(leftSeconds / 1000);
        $("#id_counter_days").text(days);
        $("#id_counter_hours").text(completeTimerDigit(hours));
        $("#id_counter_minutes").text(completeTimerDigit(minutes));
        $("#id_counter_seconds").text(completeTimerDigit(seconds));
    };

    function completeTimerDigit (number) {
        number = String(number);
        if(number.length < 2){
            number = "0" + number;
        };
        return number;
    };

    computeCounter(timeDelta);

    intervalId = window.setInterval(function() {
        timeDelta = timeDelta - 1000;
        console.log(timeDelta);
        computeCounter(timeDelta);
    }, 1000, timeDelta);
};

initCounter();