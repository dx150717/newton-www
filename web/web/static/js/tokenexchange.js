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
        first_name: {required: true, minlength: 1, maxlength: 32},
        last_name: {required: true, minlength: 1, maxlength:32},
        id_type: {required: true},
        id_number: {required: true, minlength:5, maxlength:64},
        id_card: fileRuleWithRequired,
        country: {required: true},
        city: {required: true, maxlength:64},
        location:{required: true, minlength:1, maxlength:128},
        cellphone_group_0: {required: true, minlength:1, maxlength:4},
        cellphone_group_1: {required: true, minlength:1, maxlength:20},
        personal_profile: {maxlength:2048},
        personal_profile_attachment: fileRuleWithoutRequired,
        telegram: {maxlength: 64},
        twitter: {maxlength: 64},
        facebook: {maxlength: 64},
        wechat: {maxlength: 64},
        other_social_account: {maxlength: 64},
        what_is_newton: {maxlength: 2048},
        done_for_newton: {maxlength:2048},
        done_for_newton_attachment: fileRuleWithoutRequired,
        establish_node_plan: {maxlength: 2048},
        emergency_contact_first_name: {required:true, minlength:1, maxlength:32},
        emergency_contact_last_name: {required:true, minlength:1, maxlength:32},
        cellphone_of_emergency_contact_0: {required:true, minlength:1, maxlength:4},
        cellphone_of_emergency_contact_1: {required:true, minlength:1, maxlength:20},
        emergency_country: {required: true},
        emergency_city: {required: true, maxlength:64},
        emergency_location: {required: true, maxlength:128},
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
        orgnization_name: {
            required: true, 
            minlength:1, 
            maxlength: 128
        },
        orgnization_code: {
            required: true,
            minlength:1,
            maxlength: 64
        },
        orgnization_certificate1: fileRuleWithRequired,
        orgnization_certificate2: fileRuleWithoutRequired,
        first_name: {
            required: true,
            minlength: 1,
            maxlength: 32
        },
        last_name: {required: true,
            minlength: 1,
            maxlength: 32
        },
        country: {required: true},
        cellphone_group_0: {
            required: true,
            minlength:1,
            maxlength:4
        },
        cellphone_group_1: {
            required: true,
            minlength:1,
            maxlength:20
        },
        personal_profile: {
            required: true,
            maxlength: 2048
        },
        personal_profile_attachment: fileRuleWithoutRequired,
        twitter: {maxlength: 64},
        facebook: {maxlength: 64},
        wechat_platform_name: {maxlength: 64},
        other_social_account: {maxlength: 64},
        what_is_newton: {
            required:true,
            minlength:1,
            maxlength:2048
        },
        done_for_newton: {
            required:true,
            minlength:1,
            maxlength:2048
        },
        done_for_newton_attachment: fileRuleWithoutRequired,
        establish_node_plan: {maxlength:2048}
    },
    messages: {
        orgnization_name: {
            required: "This field is required.",
            minlength: $.validator.format( "Please enter at least 1 characters." ),
            maxlength: $.validator.format( "Please enter no more than 128 characters." )
        },
        orgnization_code: {
            required: "This field is required.",
            minlength: $.validator.format( "Please enter at least 1 characters." ),
            maxlength: $.validator.format( "Please enter no more than 128 characters." )
        },
        first_name: {
            required: "This field is required.",
            minlength: $.validator.format( "Please enter at least 1 characters." ),
            maxlength: $.validator.format( "Please enter no more than 128 characters." )
        },
        last_name: {
            required: "This field is required.",
            minlength: $.validator.format( "Please enter at least 1 characters." ),
            maxlength: $.validator.format( "Please enter no more than 128 characters." )
        },
        country: {
            required: "This field is required."
        },
        id_number: {
            required: "This field is required.",
            minlength: $.validator.format( "Please enter at least 1 characters." )
        },
        cellphone_group_0: {
            required: "This field is required.",
            minlength: $.validator.format( "Please enter at least 1 characters." ),
            maxlength: $.validator.format( "Please enter no more than 4 characters." ),
            number: "Please enter a valid number."
        },
        cellphone_group_1: {
            required: "This field is required.",
            minlength: $.validator.format( "Please enter at least 1 characters." ),
            maxlength: $.validator.format( "Please enter no more than 20 characters." ),
            number: "Please enter a valid number."
        },
        personal_profile: {
            required: "This field is required.",
            maxlength: $.validator.format( "Please enter no more than 2048 characters." )
        },
        location:{
            required: "This field is required.",
            minlength: $.validator.format( "Please enter at least 1 characters." ),
            maxlength: $.validator.format( "Please enter no more than 200 characters." )
        },
        what_is_newton: {
            required: "This field is required.",
            minlength: $.validator.format( "Please enter at least 1 characters." ),
            maxlength: $.validator.format( "Please enter no more than 2048 characters." )
        },
        done_for_newton: {
            required: "This field is required.",
            minlength: $.validator.format( "Please enter at least 1 characters." ),
            maxlength: $.validator.format( "Please enter no more than 2048 characters." )
        },
        establish_node_plan: {
            maxlength: $.validator.format( "Please enter no more than 2048 characters." )
        }
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
