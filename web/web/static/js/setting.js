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
    var data = {};
    if (!$(form).valid()) {
        return false;
    }
    var gtoken_code = $('#id_gtoken_code').val();
    var redirect_url = $('#id_redirect_url').val();
    data.gtoken_code = gtoken_code;
    data.redirect_url = redirect_url;
    showWaiting();
    $.ajax({
        url:'/setting/gtoken/post/',
        type: 'post',
        data: data,
        success: function(response){
              dismiss();
              if (isSuccess(response)) {
                var result = getData(response);
                location.href = result['redirect_url'];
              } else {
                $('#id_gtoken_code').val('');
                showFail(getErrorMessage(response));
              }
        },
        error: function(request, status) {
            dismiss();
            showFail(getErrorMessage(response));
        }
    });
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
/**
 * Link google authenticator
 */
$('#id_authenticator_tab a').click(function (e) {
    e.preventDefault()
    $(this).tab('show')
});
$('.next-button').click(function(event){
    event.preventDefault();
    var index = parseInt($(this).attr('index')) + 1;
    var targetTab = '#id_page_' + index;
    $('#id_authenticator_tab a[href="' + targetTab + '"]').tab('show');
});