function googleCallback(ret){
  document.getElementById("id-google-recaptcha").value = ret;
};

$('#login_form').submit(function(event){
  event.preventDefault();
  var data = {};
  var form = this;
  var email = $("input[name='email']").val();
  var password = $("input[name='password']").val();
  var next = $("input[name='next']").val();
  
  if (!$(form).valid()) {
    return false;
  }
  data.email = email;
  data.password = password;
  data['g-recaptcha-response'] = $("input[name='google-recaptcha-name']").val();
  
  showWaiting();
  $.post("/login/post/",
          data,
          function (response) {
            dismiss();
            if (isSuccess(response)) {
              $('#code-modal').modal('show');
              var result = getData(response);
              auth_token = result.auth_token;             
            } else {
              showFail(getErrorMessage(response));
            }
          });
}).validate({
  ignore: [],
  errorElement: "div",
  errorClass: "alert alert-danger",
  rules: {
    email: {required: true, email:true},
    password: {required: true, minlength: 4}
  },
  errorPlacement: function(error,element) {
    return true;
  }
});

$("#gtoken-submit-button").click(function () {
  var gtoken_code = $("input[name='gtoken']").val();
  data = {};
  data.gtoken_code = gtoken_code;
  data.email = document.getElementById("id_email").value;
  data.password = document.getElementById("id_password").value;
  data.auth_token = auth_token;
  var next = $("input[name='next']").val();
  showWaiting();
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
});
