/**
 * login.js for valid login form and get response from google api.
 */

/**
 * 
 * @param {string} ret google recaptcha response.
 */

/**
 * valid login form and ajax post params for login.
 */
initCaptcha('id_login_form');
$('#id_login_form').submit(function(event){
  event.preventDefault();
  var data = {};
  var form = this;
  var email = $("input[name='email']").val();
  var password = $("input[name='password']").val();
  var next = $("input[name='next']").val();
  var code = $("#id_captcha_code").val()
  if (!$(form).valid()) {
    return false;
  }
  if (showCaptchaWindow()) {
      return false;
  }
  showWaiting();
  form.submit();
}).validate({
  ignore: [],
  errorElement: "div",
  errorClass: "alert alert-danger",
  rules: {
    email: {required: true, email:true},
    password: {required: true, minlength: 6, maxlength:16},
    code: {required: true}
  },
  errorPlacement: function(error,element) {
    error.appendTo(element.parent());  
  }
});

/**
 * valid google-auth form
 */
$("#id_google_auth_form").submit(function(event){
  event.preventDefault();
  var gtoken_code = $("input[name='gtoken']").val();
  data = {};
  data.gtoken_code = gtoken_code;
  data.email = document.getElementById("id_email").value;
  data.password = document.getElementById("id_password").value;
  data.auth_token = auth_token;
  var next = $("input[name='next']").val();
  data.next = next;
  var form = this;
  if (!$(form).valid()) {
    return false;
  }
  $.post("/login/post-google-authenticator/",
          data,
          function (response) {
            dismiss();
            if (isSuccess(response)) {
              var result = getData(response);
              var next = result.msg;
              location.href = next;
            } else {
              showFail(getErrorMessage(response));
            }
          });
}).validate({
  ignore: [],
  errorElement: "div",
  errorClass: "alert alert-danger",
  rules: {
    gtoken: {required: true, minlength: 4}
  },
  errorPlacement: function(error,element) {
    error.appendTo(element.parent()); 
    return true;
  }
});
