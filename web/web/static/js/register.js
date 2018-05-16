/**
 * register.js for valid register form and get response from google api.
 */

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
    if (!$(form).valid()) {
        return false;
    }
    form.submit()
}).validate({
    ignore: [],
    errorElement: "div",
    errorClass: "alert alert-danger",
    rules: {
        email: {required: true, email:true}
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