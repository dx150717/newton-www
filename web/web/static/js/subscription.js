function googleCallback(ret){
    subscriptionConfirm(ret);
};

// subscribe email list
var FAIL = 0
var SUCCESS = 1
var UNAUTH = 2
var SIGN_ERROR = 3
var INVALID_PARAMS = 4
var MAINTAIN = 5
var UPGRADE = 6
var emailReg = new RegExp("^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$");

function subscriptionConfirm(googleResponse) {
    $(".close").click();
	var recaptcha = googleResponse;
	if (!recaptcha){
		var content = "no recaptcha";
		var alertType = "alert-danger";
		showSubscriptionResult(content, alertType);
		return;
	};
	var email_address = $("input[type='text']").val();
	if(email_address.length > 0){
		if(emailReg.test(email_address)){
			var data = { "email_address": email_address, "g-recaptcha-response":recaptcha };
			showWaiting();
			$.ajax({
				url:'/subscribe/',
				timeout: 15000,
				type: 'post',
				data: data,
				success: function(ret){
					if (ret.error_code === FAIL) {
						var content = ret.error_message;
						var alertType = "alert-danger";
						showSubscriptionResult(content, alertType);
					} else {
						if (ret.result) {
							var content = ret.result.msg;
							var alertType = "alert-success";
							showSubscriptionResult(content, alertType);
						}else{
							var content = "Subscribed Failed!";
							var alertType = "alert-danger";
							showSubscriptionResult(content, alertType);
						}
					}
				},
				complete: function(request, status){
					dismiss();
					if(status == 'timeout'){
						var content = "Time out!";
						var alertType = "alert-danger";
						showSubscriptionResult(content, alertType);
					}
				}
			});
		}else{
			var content = "Invalid Email Address!";
			var alertType = "alert-danger";
			showSubscriptionResult(content, alertType);
		}
	}else{
		var content = "Please Input Email Address!";
		var alertType = "alert-danger";
		showSubscriptionResult(content, alertType);
	}
}

/**
 * Show the subscription's result with parameters.
 * 
 * @param content { String } alert content for show in page
 * @param alertType { String } eg: alert-success, alert-danger 
 */
function showSubscriptionResult(content, alertType) {
	$("#subscribe .raw").addClass("subscription-height");
	var t1 = "<div class='alert " + alertType + " alert-dismissible' role='alert'>";
	var t2 = "<button type='button' class='close tf10' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button>";
    var t3 = "<strong>" + content + "</strong></div>";
	var t = t1 + t2 + t3;
	$("#dialog").append(t);
	setTimeout(() => {
		$(".close").click();
		$(".raw").removeClass("subscription-height")
	}, 3000);
}