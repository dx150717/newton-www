function slideChangeSection(maxIndex, defaultIndex, sectionId){
	var $items=$(sectionId + " .slider-item-list div.slider-item");
	var $buttons=$(sectionId + " .slider-button-list li");
	var index=defaultIndex;

	$buttons.eq(index).addClass("numsover");
	$buttons.eq(index).siblings().removeClass("numsover");
	$items.eq(index).show();

	$buttons.mouseover(function(){
		$(this).addClass("numsover").siblings().removeClass("numsover");
		index=$buttons.index(this);
		$items.eq(index).removeClass("to-left").removeClass("to-right").fadeIn();
		$items.eq(index).siblings(".slider-item").hide();
	}).mouseout(function(){isStop=false});

	$(sectionId + " .slider-section .slider-item").on("swipeleft",function(){
		index++;
		if(index >= maxIndex) {
			index=0;
		}
		$buttons.eq(index).addClass("numsover").siblings().removeClass("numsover");
		$items.eq(index).addClass("to-left").show();
		$items.eq(index).siblings(".slider-item").removeClass("to-left").removeClass("to-right").hide();
	});
	$(sectionId + " .slider-section .slider-item").on("swiperight",function(){
		index--;
		if (index <= -1) {
			index = maxIndex - 1;
		};
		$buttons.eq(index).addClass("numsover").siblings().removeClass("numsover");
		$items.eq(index).addClass("to-right").show();
		$items.eq(index).siblings(".slider-item").removeClass("to-left").removeClass("to-right").hide();
	});
}

function slideFeature (maxIndex, defaultIndex, sectionId) {
    slideChangeSection(maxIndex, defaultIndex, sectionId);
};

function slideNotice (maxIndex, defaultIndex, sectionId) {
    slideChangeSection(maxIndex, defaultIndex, sectionId);
};

function slideIndustry (maxIndex, defaultIndex, sectionId) {
    slideChangeSection(maxIndex, defaultIndex, sectionId);
};

function slideProtocol (maxIndex, defaultIndex, sectionId) {
    slideChangeSection(maxIndex, defaultIndex, sectionId);
};

function slidePartners (maxIndex, defaultIndex, sectionId) {
    slideChangeSection(maxIndex, defaultIndex, sectionId);
};

function slideEventsPassed (maxIndex, defaultIndex, sectionId) {
    slideChangeSection(maxIndex, defaultIndex, sectionId);
};

function slideEventsJun (maxIndex, defaultIndex, sectionId) {
    slideChangeSection(maxIndex, defaultIndex, sectionId);
};

function slideEventsAug (maxIndex, defaultIndex, sectionId) {
    slideChangeSection(maxIndex, defaultIndex, sectionId);
};

function slideEventsNov (maxIndex, defaultIndex, sectionId) {
    slideChangeSection(maxIndex, defaultIndex, sectionId);
};

function slideEventsDec (maxIndex, defaultIndex, sectionId) {
    slideChangeSection(maxIndex, defaultIndex, sectionId);
};

function slideEventsComing (maxIndex, defaultIndex, sectionId) {
    slideChangeSection(maxIndex, defaultIndex, sectionId);
};

$(document).ready(function(e) {
	var windowWidth = $(window).width();
    $("a").attr("data-ajax","false");
	if (windowWidth < 768) {
        slideFeature(3, 0, "#feature");
        slideNotice(3, 2, "#token-exchange-notice-section");
        slideIndustry(6, 0, "#index-industry");
        slideProtocol(4, 0, "#protocal-section");
        slidePartners(7, 0, "#partners");
        slideEventsPassed(6, 0, "#id_events_list_passed");
        slideEventsJun(2, 0, "#id_events_list_2018_6");
        slideEventsAug(2, 0, "#id_events_list_2018_8");
        slideEventsNov(4, 0, "#id_events_list_2018_11");
        slideEventsDec(3, 0, "#id_events_list_2018_12");
        slideEventsComing(5, 0, "#id_events_list_coming");
	}
});