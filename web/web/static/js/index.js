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

