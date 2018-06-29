/**
 * tokenexhange.js for valid kyc form.
 */
$.validator.addMethod('filesize', function (value, element, param) {
    return this.optional(element) || (element.files[0].size <= param)
}, 'File size must be less than {0}');

var fileRuleWithoutRequired = {extension:'jpg,jpeg,png', filesize: 5*1024*1024};
var fileRuleWithRequired = {required: true, extension:'jpg,jpeg,png', filesize: 5*1024*1024};

$("#id_individual_form").submit(function(event){
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
        first_name: {required: true, minlength: 1, maxlength: 100},
        last_name: {required: true, minlength: 1, maxlength:100},
        id_type: {required: true},
        id_number: {required: true, minlength:1},
        id_card: fileRuleWithRequired,
        country: {required: true},
        city: {required: true},
        location:{required: true, minlength:1, maxlength:200},
        cellphone_group_0: {required: true, minlength:1, maxlength:4},
        cellphone_group_1: {required: true, minlength:1, maxlength:20},
        personal_profile_attachment: fileRuleWithoutRequired,
        your_community_screenshots1: fileRuleWithoutRequired,
        your_community_screenshots2: fileRuleWithoutRequired,
        your_community_screenshots3: fileRuleWithoutRequired,
        how_to_contribute: {required: true, maxlength:1000},
        done_for_newton_attachment: fileRuleWithoutRequired,
        what_is_newton: {minlength:1, maxlength:1000},
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
        //error.appendTo(element.parent());
    }
});

/**
 * js for valid organization kyc
 */
$("#id_organization_form").submit(function(event){
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
        orgnization_name: {required: true},
        orgnization_code: {required: true},
        orgnization_certificate1: fileRuleWithRequired,
        orgnization_certificate2: fileRuleWithoutRequired,
        first_name: {required: true, minlength: 1, maxlength: 100},
        last_name: {required: true, minlength: 1, maxlength:100},
        country: {required: true},
        cellphone_group_0: {required: true, minlength:1, maxlength:4},
        cellphone_group_1: {required: true, minlength:1, maxlength:20},
        personal_profile: {required: true},
        personal_profile_attachment: fileRuleWithoutRequired,
        what_is_newton: {required:true, minlength:1, maxlength:1000},
        done_for_newton: {required:true},
        done_for_newton_attachment: fileRuleWithoutRequired
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
            maxlength: $.validator.format( "Please enter no more than 1000 characters." )}
    },

    errorPlacement: function(error,element) {
        //error.appendTo(element.parent());
    }
});


function openNode(){
    $("#id_which_node").removeClass('hide');
    $("#id_how_node").removeClass('hide');
}
function closeNode(){
    $("#id_which_node").addClass('hide');
    $("#id_how_node").addClass('hide');
}

/**
 * js for valid organization kyc
 */
$("#id_fill_amount_form").submit(function(event){
    event.preventDefault();
    var form = this;
    if (!$(form).valid()) {
        return false;
    }
    var url = $(form).attr('action');
    var expect_btc = $('#id_expect_btc').val();
    var data = {};
    data.expect_btc = expect_btc;
    showWaiting();
    $.ajax({
            url: url,
            timeout: 15000,
            type: 'post',
            data: data,
            success: function(response){
              dismiss();
              if (isSuccess(response)) {
                  var result = getData(response);
                  location.href = result['redirect_url'];
              } else {
                showFail(getErrorMessage(response));
              }
            },
            error: function(request, status){
              dismiss();
              if(status == 'timeout'){
                showFail("Time Out");
              }
            }
          });
}).validate({
    ignore: [],
    errorElement: "div",
    errorClass: "alert alert-danger",
    rules: {
        expect_btc: {number: true, required: true}
    },
    errorPlacement: function(error,element) {
        //error.appendTo(element.parent());
    }
});

/**
 * KYC terms
 */
var checkboxes = $(".accept")
function check(){
    for(var i = 0; i < checkboxes.length; i++){
        var status = checkboxes[i].checked
        if (status === false){
            $("#gotokyc-btn")[0].setAttribute("disabled", true)
            return;
        } 
        if (i == (checkboxes.length-1)){
            $("#gotokyc-btn")[0].removeAttribute("disabled")
        }
    }
}
function gotokyc(){
    showWaiting();
    location.href = ("/tokenexchange/individual/post/");
}
function changeCheckStatus() {
    checkboxes[0].checked = !checkboxes[0].checked;
    check();
}
