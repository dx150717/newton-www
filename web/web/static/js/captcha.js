/*
 * The implementation of captcha module
 */

$('#id_captcha_image, #id_captcha_tip').click(function(event){
  $('#id_captcha_image').attr('src', '/ishuman/image/?' + Math.random());
});
