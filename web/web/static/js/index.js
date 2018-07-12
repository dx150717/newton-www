var FAIL = 0
var SUCCESS = 1
var UNAUTH = 2
var SIGN_ERROR = 3
var INVALID_PARAMS = 4
var MAINTAIN = 5
var UPGRADE = 6
// load messages
function loadCurrentMessage()
{
	var language = document.cookie.split("language=")[1];
	if(language == null || language == undefined){
		language = navigator.language;
	}
	if (language && language.indexOf('zh') >= 0) {
		language = 'zh_CN';
	} else {
		language = 'en';
	}
	jQuery.i18n.properties({
	    name:'Messages', 
	    path:'/static/js/', 
	    mode: 'both',
	    language: language,
	    async: true,
	    callback: function() {
	    }
	});
}
loadCurrentMessage();
// load language javascript
function initLanguage(){
	var language = document.cookie.split("language=")[1];
	if(language == null || language == undefined){
		language = navigator.language;
	}
	if(language!=null && language!=undefined && language.startsWith("zh")){
		$.getScript(zhMessages);
	}
}
initLanguage();

$(function () {
	var bottomNavToggle = function (event) {
		$(event.target).next().slideToggle(300, function () {
			$(this).prev().toggleClass('changed');
		});
	};
	if (window.innerWidth <= 768) {
		$('#nav-footer').find('h4').on('click', bottomNavToggle);
	}
	$(window).resize(function () {
		if (window.innerWidth <= 768) {
			$('#nav-footer').find('h4').off('click', bottomNavToggle).on('click', bottomNavToggle).each(function () {
				$(this).removeClass('changed');
				$(this).next().hide();
			});
		} else {
			$('#nav-footer').find('h4').off('click', bottomNavToggle).each(function () {
				$(this).next().show();
			});
		}
	});
	var bottomNavToggle = function (event) {
	};
	$(window).resize(function () {
		if (window.innerWidth <= 768) {
			hide();
		} else {
			show();
		}
	});
	var show = function () {
		$('#nav-footer').find('h4').off('click', bottomNavToggle).each(function () {
			$(this).next().show();
		});
	}
	var hide = function () {
		$('#nav-footer').find('h4').off('click', bottomNavToggle).on('click', bottomNavToggle).each(function () {
			$(this).removeClass('changed');
			$(this).next().hide();
		});
	}
	if (window.innerWidth <= 768) {
		hide();
	}
});

/**
 * Set page language with language code.
 * 
 * @param language { String } language code
 */
function setLanguage(language) {
	var expires = "";
	var days = 365;
	var name = 'language';
	var value = language;
	if (days) {
		var date = new Date();
		date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
		expires = "; expires=" + date.toUTCString();
	}
	document.cookie = name + "=" + value + expires + "; path=/";
	var locationHref = window.location.pathname;
	window.location.reload();
	if(locationHref.startsWith("\/blog")){
		location.replace("/blog/");
	}
	if(locationHref.startsWith("\/announcement")){
		location.replace("/announcement/");
	}
	// load the nessary resource file
	loadCurrentMessage();
}

// language's dropdown menu.
var windowWidth = window.innerWidth;
var dropdownFlag = true;
if (windowWidth < 768) {
	dropdownFlag = false;
} else {
	dropdownFlag = true;
}
//setDropdownListener(dropdownFlag);
$(window).resize(function () {
	if (window.innerWidth < 768) {
		if (dropdownFlag) {
			dropdownFlag = false;
			var bottomNavToggle = function (event) {
				$(event.target).next().slideToggle(300, function () {
					$(this).prev().toggleClass('changed');
				});
			};
			$('#nav-footer').find('h4').on('click', bottomNavToggle);
		}
		
		
	} else {
		if (!dropdownFlag) {
			dropdownFlag = true;
			//setDropdownListener(dropdownFlag);
		}
	};
});

/**
 * If pc screen, add 'mouseenter' and 'mouseleave listener for dropdown menu, and remove
 * it on mobile screen.
 * 
 * @param {boolean} isFlag mobile screen is false, pc screen is true.
 */
function setDropdownListener(isFlag) {
	if (isFlag) {
		$(".dropdown")[0].addEventListener("mouseenter", openDropdown);
		$(".dropdown")[0].addEventListener("mouseleave", closeDropdown);
	} else {
		$(".dropdown")[0].removeEventListener("mouseenter", openDropdown);
		$(".dropdown")[0].removeEventListener("mouseleave", closeDropdown);
	}
}
function openDropdown() {
	$(".dropdown").addClass("open");
}
function closeDropdown() {
	$(".dropdown").removeClass("open");
}
function changeToggle() {
	if($("#drop-panel").hasClass("collapsing")){
		return;
	}
	if ($('body').hasClass('fsn')) {
		$('body').removeClass('fsn');
	} else {
		$('body').addClass('fsn');
	}
}

$(document).ready(function ($) {
	$('.page-scroll').on('click', function (event) {
		var $anchor = $(this);
		$('html, body').stop().animate({
			scrollTop: $($anchor.attr('href')).offset().top
		}, 700, 'easeInOutExpo');
		event.preventDefault();
	});


	// collapsed menu close on click
	$(document).on('click', '.navbar-collapse.in', function (e) {
		if ($(e.target).is('a')) {
			$(this).collapse('hide');
		}
	});
});

// gtag 
window.dataLayer = window.dataLayer || [];
function gtag() { dataLayer.push(arguments); }
gtag('js', new Date());
gtag('config', 'UA-116218760-1');

// global progress
function initGlobalToolkit()
{
  $('#id_loading').nsProgress({img_path: '/static/images/libs/nsprogress'});
}

function showLoading()
{
  initGlobalToolkit();
  var msg = $.i18n.prop('msg_loading');
  $('#id_loading').nsProgress('showWithStatusAndMaskType', msg, 'black');
}

function showWaiting()
{
  initGlobalToolkit();
  var msg = $.i18n.prop('msg_processing');
  $('#id_loading').nsProgress('showWithStatusAndMaskType', msg, 'black');
}

function showSuccess(msg)
{
  initGlobalToolkit();
  if (!msg) {
    msg = $.i18n.prop('msg_operation_success');
  }
  $('#id_loading').nsProgress('showSuccessWithStatusAndMaskType', msg, 'black');
  dismissDelay();
}

function showFail(msg)
{
  initGlobalToolkit();
  $('#id_loading').nsProgress('showErrorWithStatusAndMaskType', msg, 'black');
  dismissDelay();
}

function showNetworkError(msg)
{
	var msg = $.i18n.prop('msg_network_error');
	showFail(msg);
}

function dismiss()
{
	$('#id_loading').nsProgress('dismiss');
}

function dismissDelay()
{
	var task = setTimeout(function(){
		$('#id_loading').nsProgress('dismiss');
	}, 3000);
}
var SUCCESS = 1;

function isSuccess(json)
{
  var error_code = json.error_code;
  if (error_code == SUCCESS) {
    return true;
  }
  return false;
}

function getData(json)
{
  return json.result;
}

function getErrorMessage(json)
{
  return json.error_message;
}


function gotoTop(min_height){
    $("#gotoTop").click(
        function(){$('html,body').animate({scrollTop:0},700);
    }).hover(
        function(){$(this).addClass("hover");},
        function(){$(this).removeClass("hover");
    });
    min_height ? min_height = min_height : min_height = 800;
    $(window).scroll(function(){
        var s = $(window).scrollTop();
        if( s > min_height){
            $("#gotoTop").fadeIn(100);
        }else{
            $("#gotoTop").fadeOut(200);
        };
    });
};
gotoTop();

$(window).scroll(function(){
	var height
	var s = $(window).scrollTop();
	if (s>0){
		$(".NavBg").addClass("navFixed");
	}else{
		$(".NavBg").removeClass("navFixed");
		};
});


//Verify User Login Status
$(window).ready(function(){
    var data_dict = {};
    data_dict[HOME_SESSION_KEY] = homeSessionID
    $.ajax({
        url : NEWTON_HOME_URL + "/nauth/session/",
        type : "GET",
        data : data_dict,
        dataType : "JSON",
        success : function(data){
            var user_status = isSuccess(data);
            if (user_status){
                $("#id_user_dropdown").show();
                $("#id_register_item").hide();
                $("#id_login_item").hide();
                $("#id_center_phone_display").show();
                $("#id_logout_phone_display").show();
                $("#id_register_phone_display").hide();
                $("#id_login_phone_display").hide();
                $("#id_register_phone_display").removeClass("visible-xs-block");
                $("#id_login_phone_display").removeClass("visible-xs-block");
            }else{
                $("#id_user_dropdown").hide();
                $("#id_register_item").show();
                $("#id_login_item").show();
                $("#id_center_phone_display").hide();
                $("#id_center_phone_display").removeClass("visible-xs-block");
                $("#id_logout_phone_display").removeClass("visible-xs-block");
                $("#id_logout_phone_display").hide();
                $("#id_register_phone_display").show();
                $("#id_login_phone_display").show();
            };
            }
    });
    });
