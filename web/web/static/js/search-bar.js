/* Search bar js */

function initSearchBar () {
    var inputStatus = false;
    $("#id_search_icon_container").click(function () {
        if ($(this).children("span").hasClass("glyphicon-search") && inputStatus == false) {
            $(this).addClass("search_icon_container");
            $("#id_search_from").addClass("search_form");
            $("#id_search_input").val("");
            $(this).parent("li").siblings().hide();
            $("#id_search_input").fadeIn();
            $("#id_search_input").focus();
            $("#id_search_btn").fadeIn();
            $("#id_search_icon").removeClass("glyphicon-search").addClass("glyphicon-remove");
            inputStatus = true;
        } else if ($(this).children("span").hasClass("glyphicon-remove") && inputStatus == true) {
            $(this).removeClass("search_icon_container");
            $("#id_search_from").removeClass("search_form");
            $("#id_search_input").hide();
            $("#id_search_btn").hide();
            $(this).parent("li").siblings().fadeIn();
            $("#id_search_icon").removeClass("glyphicon-remove").addClass("glyphicon-search");
            $("#id_search_input").val("");
            inputStatus = false;
        }
    });
};