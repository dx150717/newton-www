/**
 * reset.js for valid reset form.
 */

 /**
  * valid reset email
  */
$("#reset-email-form").submit(function(event){
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
        return true;
    }
});

/**
 * valid reset password form.
 */
$("#reset-password-form").submit(function(event){
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
        password: {required: true, minlength:4},
        repassword: {required: true, minlength: 4},
    },
    errorPlacement: function(error,element) {
      return true;
    }
});