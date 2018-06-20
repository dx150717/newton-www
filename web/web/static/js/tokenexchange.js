/**
 * tokenexhange.js for valid kyc form.
 */
$("#id_individual_form").submit(function(event){
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
        id_type: {required: true},
        id_number: {required: true, minlength:1},
        id_card: {required: true, extension:true, checkPicSize:true},
        country: {required: true},
        city: {required: true},
        location:{required: true, minlength:1, maxlength:200},
        cellphone_group_0: {required: true, minlength:1, maxlength:4},
        cellphone_group_1: {required: true, minlength:1, maxlength:20},
        personal_profile: {required: true},
        how_to_contribute: {required: true, maxlength:1000},
        what_is_newton: {required:true, minlength:1, maxlength:1000},
        emergency_contact_first_name: {required:true, minlength:1, maxlength:100},
        emergency_contact_last_name: {required:true, minlength:1, maxlength:100},
        cellphone_of_emergency_contact_0: {required:true, minlength:1, maxlength:4},
        cellphone_of_emergency_contact_1: {required:true, minlength:1, maxlength:20},
        emergency_country: {required: true},
        emergency_city: {required: true},
        emergency_location: {required: true},
        emergency_relationship: {required:true}
    },
    messages: {
        first_name: {required: "This field is required.",
            minlength: $.validator.format( "Please enter at least 1 characters." ),
            maxlength: $.validator.format( "Please enter no more than 100 characters." )},
        last_name: {required: "This field is required.",
            minlength: $.validator.format( "Please enter at least 1 characters." ),
            maxlength: $.validator.format( "Please enter no more than 100 characters." )},
        country: {required: "This field is required."},
            id_number: {required: "This field is required.",
            minlength: $.validator.format( "Please enter at least 1 characters." )},
        id_card: {required: "This field is required."},
        cellphone_group_0: {required: "This field is required.",
            minlength: $.validator.format( "Please enter at least 1 characters." ),
            maxlength: $.validator.format( "Please enter no more than 4 characters." ),
            number: "Please enter a valid number."},
        cellphone_group_1: {required: "This field is required.",
            minlength: $.validator.format( "Please enter at least 1 characters." ),
            maxlength: $.validator.format( "Please enter no more than 20 characters." ),
            number: "Please enter a valid number."},
        location:{required: "This field is required.",
            minlength: $.validator.format( "Please enter at least 1 characters." ),
            maxlength: $.validator.format( "Please enter no more than 200 characters." )},
        how_to_contribute: {required: "This field is required.",
            maxlength: $.validator.format( "Please enter no more than 1000 characters." )},
        what_is_newton: {required: "This field is required.",
            minlength: $.validator.format( "Please enter at least 1 characters." ),
            maxlength: $.validator.format( "Please enter no more than 1000 characters." )},
        emergency_contact_first_name: {required: "This field is required.",
            minlength: $.validator.format( "Please enter at least 1 characters." ),
            maxlength: $.validator.format( "Please enter no more than 100 characters." )},
        emergency_contact_last_name: {required: "This field is required.",
            minlength: $.validator.format( "Please enter at least 1 characters." ),
            maxlength: $.validator.format( "Please enter no more than 100 characters." )},
        cellphone_of_emergency_contact_0: {required: "This field is required.",
            minlength: $.validator.format( "Please enter at least 1 characters." ),
            maxlength: $.validator.format( "Please enter no more than 4 characters." ),
            number: "Please enter a valid number."},
        cellphone_of_emergency_contact_1: {required: "This field is required.",
            minlength: $.validator.format( "Please enter at least 1 characters." ),
            maxlength: $.validator.format( "Please enter no more than 20 characters." ),
            number: "Please enter a valid number."},
        relationships_with_emergency_contacts: {required: "This field is required."}
    },

    errorPlacement: function(error,element) {
        error.appendTo(element.parent());
    }
});

function openNode(){
    $("#which-node").removeClass('hide');
    $("#how-node").removeClass('hide');
}
function closeNode(){
    $("#which-node").addClass('hide');
    $("#how-node").addClass('hide');
}