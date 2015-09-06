
var finprint = finprint || {};  //namespace if necessary...

(function($) {
    "use strict";

    $(document).ready(function(){
        $('.list-group-item').on('click', function(e){
            var $item = $(e.currentTarget);
            $item.parent().children().removeClass('active');
            $item.addClass('active');

            var pk = $item.attr("data-pk-id");
            $.get('/api/trips/' + pk, function(data){
               $('#trip_detail_panel').empty()
                       .append($('<h4>' + data.name + '</h4><dl><dt>Start Date:</dt><dd>' + data.start_date
                               + '</dd><dt>End Date:</dt><dd>' + data.end_date
                               + '</dd><dt>Location:</dt><dd>' + data.location
                               + '</dd><dt>Team:</dt><dd>' + data.team
                               + '</dd><dt>Boat:</dt><dd>' + data.boat));
            });
        });

        var $list = $('.list-group').children();
        if ($list.size() > 0) {
            $list[0].click();
        }  else {
            $('#trip_detail_panel').hide();
        }
    });

})(jQuery);
