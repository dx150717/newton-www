/**
 * register.js for valid register form and get response from google api.
 */
var SUCCESS_TIP = '<span class="glyphicon glyphicon-ok-circle alert-success" aria-hidden="true"></span>';

/**
 * 
 * @param {string} ret google recaptcha response.
 */
function googleCallback(ret){
    document.getElementById("id-google-recaptcha").value = ret;
};
/**
 * register.js for valid register form.
 */
$("#register-form").submit(function(event){
    event.preventDefault();
    var form = this;
    var code = $("#id_code").val()
    if (!$(form).valid()) {
        return false;
    }
    $.ajax({
        url:'/ishuman/check/?code=' + code,
        type: 'post',
        data: {},
        success: function(ret){
            if (ret.error_code === FAIL) {
                console.log("remove class")
                $("#id_register_code_error").removeClass("hide");
                $("#id_register_code_error").attr("style", "display:!important block");
                return false;
            } else {
                form.submit();
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
        code: {required: true}
    },
    errorPlacement: function(error,element) {
        error.appendTo(element.parent());
    }
});

/**
 * valid set password form.
 */
$("#set-password-form").submit(function(event){
    event.preventDefault();
    var form = this;
    if (!$(form).valid()) {
        return false;
    }
    form.submit()
}).validate({
    ignore: [],
    errorElement: "div",
    errorClass: "alert alert-danger",
    rules: {
        password: {required: true, minlength:6, maxlength:16, password:true},
        repassword: {required: true, minlength: 6, maxlength:16, equalTo:"#id_password", password:true},
    },
    errorPlacement: function(error,element) {
        error.appendTo(element.parent());
    }
});

/**
 * set gtoken
 */
$("#set-gtoken-form").submit(function(event){
    event.preventDefault();
    var form = this;
    if (!$(form).valid()) {
        return false;
    }
    form.submit()
}).validate({
    ignore: [],
    errorElement: "div",
    errorClass: "alert alert-danger",
    rules: {
        gtoken_code: {required: true, minlength:4},
    },
    errorPlacement: function(error,element) {
        error.appendTo(element.parent());
    }
});

$('#register_captcha_code').click(function(event){
    event.preventDefault();
    $(this).attr("src", "/ishuman/image/?" + Math.random());
    $("#id_register_code_error").addClass("hide");
});
