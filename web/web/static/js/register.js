/**
 * register.js for valid register form and get response from google api.
 */
var SUCCESS_TIP = '<span class="glyphicon glyphicon-ok-circle alert-success" aria-hidden="true"></span>';

/**
 * register.js for valid register form.
 */
$("#id_register_form").submit(function(event){
    event.preventDefault();
    var form = this;
    var code = $("#id_captcha_code").val()
    if (!$(form).valid()) {
        return false;
    }
    showWaiting();
    $.ajax({
        url:'/ishuman/check/?code=' + code,
        type: 'post',
        data: {},
        success: function(ret){
            dismiss();
            if (ret.error_code === FAIL) {
                $("#id_register_code_error").removeClass("hide");
                $("#id_register_code_error").attr("style", "display:!important block");
                $('#id_captcha_image').click();
                $("#id_captcha_code").val('')
                return false;
            } else {
                form.submit();
            }
        },
        error: function(request, status) {
            dismiss();
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
$("#id_set_password_form").submit(function(event){
    event.preventDefault();
    var form = this;
    if (!$(form).valid()) {
        return false;
    }
    showWaiting();
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
