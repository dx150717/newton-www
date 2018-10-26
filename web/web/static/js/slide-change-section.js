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

	$(sectionId + " .slider-section").on("swipeleft",function(){
		index++;
		if(index >= maxIndex) {
			index=0;
		}
		$buttons.eq(index).addClass("numsover").siblings().removeClass("numsover");
		$items.eq(index).addClass("to-left").show();
		$items.eq(index).siblings(".slider-item").removeClass("to-left").removeClass("to-right").hide();
	});
	$(sectionId + " .slider-section").on("swiperight",function(){
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
}

function slideIndustry (maxIndex, defaultIndex, sectionId) {
    slideChangeSection(maxIndex, defaultIndex, sectionId);
}

function slidePartners (maxIndex, defaultIndex, sectionId) {
    slideChangeSection(maxIndex, defaultIndex, sectionId);
}

$(document).ready(function(e) {
	var windowWidth = $(window).width();
	if (windowWidth < 768) {
	    $("a").attr("data-ajax","false")
        slideFeature(3, 0, "#feature");
        slideNotice(3, 2, "#token-exchange-notice-section");
        slideIndustry(6, 0, "#index-industry");
        slideIndustry(4, 0, "#protocal-section");
        slidePartners(7, 0, "#partners")
	}
});