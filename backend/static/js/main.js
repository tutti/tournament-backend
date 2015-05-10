(function($) {

    $(document).ready(function() {
        $("#menu .submenu .extend-menu").click(function(e) {
            e.preventDefault();
            var menu = $(e.target).parent();
            if (menu.hasClass("menu-expanded")) {
                menu.removeClass("menu-expanded");
            } else {
                menu.addClass("menu-expanded");
            }
        });
    });

})(jQuery);