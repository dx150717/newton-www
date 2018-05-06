var email;
var password;
var auth_token;
var next;
var google_response;

$("#normal").addClass("display-none");

function googleCallback(ret){
  google_response = ret;
};

function hiddenError(){
  $("#error-content").empty();
  $(".ajax-error").addClass("hidden");
}

$('#login_form').submit(function(event){
  event.preventDefault();
  var data = {};
  email = $("input[name='email']").val();
  password = $("input[name='password']").val();
  next = $("input[name='next']").val();
  data.email = email;
  data.password = password;
  data['g-recaptcha-response'] = google_response;
  $.post("/login/post/", data, function (ret) {
    if (ret.error_message) {
      if($(".ajax-error").hasClass("hidden")){
        $("#error-content").append(ret.error_message);
        $(".ajax-error").removeClass("hidden");
      }
      return;
    }
    if (ret.result) {
      $('#code-modal').modal('show');
      auth_token = ret.result.auth_token;
    };
  });
}).validate({
  ignore: [],
  errorElement: "div",
  errorClass: "alert alert-danger",
  rules: {
    email: {required: true, email:true},
    password: {required: true, minlength: 6}
  },
  errorPlacement: function(error,element) {
    return true;
  }
});

$("#gtoken-submit-button").click(function () {
  var gtoken_code = $("input[name='gtoken']").val();
  data = {};
  data.gtoken_code = gtoken_code;
  data.email = email;
  data.password = password;
  data.auth_token = auth_token;
  var next = $("input[name='next']").val();
  $.post("/login/post-google-authenticator/", data, function (ret) {
    if (ret.error_message) {
      $("#error-content").append(ret.error_message);
      $(".ajax-error").removeClass("hidden");
      return;
    }
    if (ret.result) {
      var next = ret.result.msg;
      location.href = next;
    }
  });
});

