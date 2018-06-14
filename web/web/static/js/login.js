/**
 * login.js for valid login form and get response from google api.
 */

/**
 * 
 * @param {string} ret google recaptcha response.
 */
function googleCallback(ret){
  document.getElementById("id-google-recaptcha").value = ret;
};

/**
 * valid login form and ajax post params for login.
 */
$('#login_form').submit(function(event){
  event.preventDefault();
  var data = {};
  var form = this;
  var email = $("input[name='email']").val();
  var password = $("input[name='password']").val();
  var next = $("input[name='next']").val();
  var code = $("#id_code").val()
  if (!$(form).valid()) {
    return false;
  }
  showWaiting();
  $.ajax({
    url:'/ishuman/check/?code=' + code,
    type: 'post',
    data: {},
    success: function(ret){
        if (ret.error_code === FAIL) {
            $("#id_login_code_error").removeClass("hide");
            $("#id_login_code_error").attr("style", "display:!important block");
            return false;
        } else {
          data.email = email;
          data.password = password;
          data.code = code;
          $.ajax({
            url:'/login/post/',
            timeout: 15000,
            type: 'post',
            data: data,
            success: function(response){
              dismiss();
              if (isSuccess(response)) {
                $('#code-modal').modal('show');
                var result = getData(response);
                auth_token = result.auth_token;             
              } else {
                showFail(getErrorMessage(response));
              }
            },
            complete: function(request, status){
              if(status == 'timeout'){
                dismiss();
                showFail("Time Out");
              }
            }
          })
        }
    },
    complete: function(request, status) {
    }
  });
  
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
$("#google-auth-form").submit(function(event){
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


$('#login_captcha_code').click(function(event){
  event.preventDefault();
  $(this).attr("src", "/ishuman/image/?" + Math.random());
  $("#id_login_code_error").addClass("hide");
});
