// subscribe email list
var emailReg = new RegExp("^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$");
var ERROR_TIP = '<span class="glyphicon glyphicon-remove-circle alert-danger" aria-hidden="true"></span>';
var SUCCESS_TIP = '<span class="glyphicon glyphicon-ok-circle alert-success" aria-hidden="true"></span>';

$('#subscription_form').submit(function(event){
	event.preventDefault();
	var form = this;
	var email_address = $(form).find("input[type='text']").val();
	if(email_address.length > 0) {
		if(emailReg.test(email_address)) {
			$('.recaptcha-modal').modal();
			$('#id_captcha_container').html('<image class="text-center" id="id_code_image" src="/ishuman/image/?' + Math.random() + '"/>');
			$('#id_code_image').click(function(event){
				event.preventDefault();
				$(this).attr("src", "/ishuman/image/?" + Math.random());
			});
			$('#id_validator_status').html('');
			$('#id_code').val('');
			$('#id_code').keyup(function(event){
				var node = this;
				var value = $(node).val();
				if (value.length == 5) {
					$.ajax({
						url:'/ishuman/check/?code=' + value,
						type: 'post',
						data: {},
						success: function(ret){
							if (ret.error_code === FAIL) {
								$('#id_validator_status').html(ERROR_TIP);
								$('#id_code_image').click();
								$('#id_code').val('');
							} else {
								$('#id_validator_status').html(SUCCESS_TIP);
								subscriptionConfirm();
							}
						},
						complete: function(request, status) {
						}
					});
				} else {
					if (value.length < 5) {
						$('#id_validator_status').html('');
					} else {
						$('#id_validator_status').html(ERROR_TIP);
					}
				}
			});
		}
	}
});

function subscriptionConfirm() {
	$('.recaptcha-modal').modal('hide');
	var code = $('#id_code').val();
	var email_address = $('#subscription_form').find("input[type='text']").val();
	if(email_address.length > 0) {
		if(emailReg.test(email_address)) {
			var data = { "email_address": email_address, "code":code };
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
							// reset the input
							$('#subscription_form').find("input[type='text']").val('');
						} else {
							var content = "Subscribed Failed!";
							var alertType = "alert-danger";
							showSubscriptionResult(content, alertType);
						}
					}
				},
				complete: function(request, status) {
					dismiss();
					if(status == 'timeout') {
						var content = "Time out!";
						var alertType = "alert-danger";
						showSubscriptionResult(content, alertType);
					}
				}
			});
		} else {
			var content = "Invalid Email Address!";
			var alertType = "alert-danger";
			showSubscriptionResult(content, alertType);
		}
	} else {
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