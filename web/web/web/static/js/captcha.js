/*
 * The implementation of captcha module
 */
var g_captcha_form = '';

function initCaptcha(form_id) {
    g_captcha_form = form_id;
}

/**
 * 
 * @param {string} ret google recaptcha response.
 */
function googleCallback(ret){
    document.getElementById("id_google_recaptcha").value = ret;
};

/*
 * Callback for tencent captcha
 */
function tencent_captcha_callback(res) {
    if(res.ret === 0) { // success
        $('#id_ticket').val(res.ticket);
        $('#id_randstr').val(res.randstr);
        showWaiting();
        var form = document.getElementById(g_captcha_form);
        form.submit();
    } else {
    }
}

function showCaptchaWindow() {
    var captcha_service_type = $('#id_captcha_service_type').val();
    if (captcha_service_type == 'tencent') {
        $('#TencentCaptcha').click();
        return true;
    }
    return false;
}
