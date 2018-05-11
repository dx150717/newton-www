/**
 * tokenexhange.js for valid kyc form.
 */
$("#user_kyc_form").submit(function(event){
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
        first_name: {required: true, minlength: 1, maxlength: 100},
        last_name: {required: true, minlength: 1, maxlength:100},
        country: {required: true},
        id_number: {required: true, minlength:1},
        id_card: {required: true},
        cellphone_group_0: {required: true, minlength:1, maxlength:4, number:true},
        cellphone_group_1: {required: true, minlength:1, maxlength:20, number:true},
        location:{required: true, minlength:1, maxlength:200},
        how_to_contribute: {required: true, maxlength:1000},
        what_is_newton: {required:true, minlength:1, maxlength:1000},
        emergency_contact_first_name: {required:true, minlength:1, maxlength:100},
        emergency_contact_last_name: {required:true, minlength:1, maxlength:100},
        cellphone_of_emergency_contact_0: {required:true, minlength:1, maxlength:4, number:true},
        cellphone_of_emergency_contact_1: {required:true, minlength:1, maxlength:20, number:true},
        relationships_with_emergency_contacts: {required:true},
        expect_btc:{number:true, min:1},
        expect_ela:{number:true, min:100}
    },
    errorPlacement: function(error,element) {
        error.appendTo(element.parent());
    }
});