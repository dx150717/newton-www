/**
 * setting.js for setting module
 */
var SUCCESS_TIP = '<span class="glyphicon glyphicon-ok-circle alert-success" aria-hidden="true"></span>';

/**
 * set gtoken
 */
$("#id_set_gtoken_form").submit(function(event){
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
