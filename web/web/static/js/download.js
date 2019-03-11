var u = navigator.userAgent;
var isAndroid = u.indexOf('Android') > -1 || u.indexOf('Adr') > -1;
var isiOS = !!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/);

if (isAndroid) {
  $('#id_android_btn').show();
} else if (isiOS) {
  $('#id_ios_btn').show();
  $('#id_note').show();
} else {
  $('#id_android_btn,#id_ios_btn').addClass('small-btn');
  $('#id_android_btn').show();
  $('#id_ios_btn').show();
}
$('[data-toggle="popover"]').popover();
