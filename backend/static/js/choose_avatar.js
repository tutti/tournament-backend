(function($) {
    $(document).ready(function() {

        var avatar_info = $(".avatar-info");
        var input = $("#avatar-input");

        avatar_info.click(function(e) {
            avatar_info.removeClass("selected");
            var box = $(e.delegateTarget);
            box.addClass("selected");
            input.val(box.attr("data-avatar-id"));
        });

    });
})(jQuery);