/* Search bar js */

function initSearchBar () {
    var inputStatus = false;
    $("#id_search_icon_container").click(function () {
        if ($(this).children("span").hasClass("glyphicon-search") && inputStatus == false) {
            $("#id_search_input").val("");
            $(this).parent("li").siblings().hide();
            $("#id_search_input").fadeIn();
            $("#id_search_btn").fadeIn();
            $("#id_search_icon").removeClass("glyphicon-search").addClass("glyphicon-remove");
            inputStatus = true;
        } else if ($(this).children("span").hasClass("glyphicon-remove") && inputStatus == true) {
            $("#id_search_input").fadeOut();
            $("#id_search_btn").fadeOut();
            $(this).parent("li").siblings().fadeIn();
            $("#id_search_icon").removeClass("glyphicon-remove").addClass("glyphicon-search");
            $("#id_search_input").val("");
            inputStatus = false;
        }
    });
};