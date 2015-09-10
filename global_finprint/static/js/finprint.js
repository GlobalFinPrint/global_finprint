var finprint = finprint || {};  //namespace if necessary...

(function ($) {
    "use strict";

    $(document).ready(function () {
        $('.list-group-item').on('click', function (e) {
            var $item = $(e.currentTarget);
            $item.parent().children().removeClass('active');
            $item.addClass('active');

            var pk = $item.attr("data-pk-id");
            var type = $item.attr("data-type");
            var detail_type = unknownType($('#detail_panel'));
            if (type === "trip") {
                detail_type = tripDetails($('#detail_panel'), pk);
            } else if (type === "set") {
                detail_type = setDetails($('#detail_panel'), pk);
            }
            detail_type.get();
        });

        var $list = $('.list-group').children();
        if ($list.size() > 0) {
            $list[0].click();
        } else {
            $('#detail_panel').hide();
        }
    });


    function unknownType(container){
        var $containerEl = container;

        var get = function(){
                $containerEl.empty()
                        .append($('<h4>Unknown Type</h4>'));
        };
        return {"get": get};
    }

    function tripDetails(container, pk){
        var id = pk;
        var $containerEl = container;
        var get = function(){
            $.get('/api/trips/' + id, function (data) {
                $containerEl.empty()
                        .append($('<h4>' + data.name + '</h4><dl><dt>Start Date:</dt><dd>' + data.start_date +
                                '</dd><dt>End Date:</dt><dd>' + data.end_date +
                                '</dd><dt>Location:</dt><dd>' + data.location +
                                '</dd><dt>Team:</dt><dd>' + data.team +
                                '</dd><dt>Boat:</dt><dd>' + data.boat + '</dd></dl>'));
            });
        };
        return {"get": get};
    }

    function setDetails(container, pk){
        var id = pk;
        var $containerEl = container;
        var get = function(){
            $.get('/api/sets/' + id, function (data) {
                $containerEl.empty()
                        .append($('<h4>' + moment(data.drop_time).format("dddd, MMMM Do YYYY, h:mm a") +
                                '</h4><dl><dt>drop time:</dt><dd>' + moment(data.drop_time).format("H:mm:ss") +
                                '</dd><dt>Collection Time</dt><dd>' + moment(data.collection_time).format("H:mm:ss") +
                                '</dd><dt>Bait Gone</dt><dd> '+ moment(data.time_bait_gone).format("H:mm:ss") +
                                '</dd><dt>Equipment</dt><dd> ' + data.equipment +
                                '</dd><dt>Depth</dt><dd> ' + data.depth +
                                '</dd><dt>Reef</dt><dd> ' + data.reef + '</dd></dl>'));

            });
        };
        return {"get": get};
    }

})(jQuery);
