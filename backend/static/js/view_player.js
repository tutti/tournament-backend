(function($) {

    $(document).ready(function() {
        var tooltip = $("#tooltip");
        tooltip.head = $("#tooltip-head");
        tooltip.body = $("#tooltip-body");

        function show_tooltip(e) {
            var element = $(e.target);
            var position = element.position();
            console.log(position);
            tooltip.css("left", parseInt(position.left)+40);
            tooltip.css("top", parseInt(position.top));
            tooltip.head.text(element.attr("data-tooltip-head"));
            tooltip.body.text(element.attr("data-tooltip-body"));
            tooltip.show();
        }

        function hide_tooltip() {
            tooltip.hide();
        }

        $(".award-image").hover(show_tooltip, hide_tooltip);
    });

})(jQuery);