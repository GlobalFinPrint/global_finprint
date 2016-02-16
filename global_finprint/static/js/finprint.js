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
            var detail_obj = unknownType();
            if (type === "trip") {
                detail_obj = Trip();
            } else if (type === "set") {
                detail_obj = Set();
            } else if (type === "observation") {
                detail_obj = Observation();
            }
            else {
                detail_obj = unknownType();
            }
            detail_obj.get(pk, function(){
                detail_obj.display($('#detail_panel'));
            });

        });

        var $list = $('.list-group').children();
        if ($list.size() > 0) {
            $list[0].click();
        } else {
            $('#detail_panel').hide();
        }

        $('table.set-table').find('a.show-env, a.hide-env').click(function(e) {
            e.preventDefault();
            $(this).hide()
                .siblings().toggle().end()
                .closest('table.set-table')
                    .find('tr.set-' + $(this).data('set')).toggle();
        });

        $('div.assign-form #id_affiliation').change(function(e) {
          var $affiliation = $(e.target);
          var $annotator = $('div.assign-form #id_annotator');
          $.get('/assignment/list/', { affiliation: $affiliation.val() }, function(res) {
            $annotator.empty().append(res.annotators.map(function (a) {
              return "<option value='" + a.id + "'>" + a.user + "</option>";
            }).join('\n')).prepend('<option value="" selected="selected">---------</option>');
          });
        });

        initAdjustAnnotator();
        initAssignButtons();
    });

    function getCSRF() {
        var cookies = document.cookie.split(';');
        var i;
        for (i=0; i<cookies.length; i++) {
            if (cookies[i].trim().startsWith('csrftoken=')) {
                return cookies[i].trim().split('=')[1];
            }
        }
    }

    function initAssignButtons() {
      var $form = $('form.video-annotator-trip-select');
      $form.submit(function() { return false; });

      $form.find('a.manual-assign').click(function(e) {
        e.preventDefault();
        var id = $form.find('#id_trip').val();
        if (id) {
          window.location.href = '/assignment/' + id;
        }
      });

      $form.find('a.auto-assign').click(function(e) {
        e.preventDefault();
        var id = $form.find('#id_trip').val();
        if (id) {
          window.location.href = '/assignment/auto/' + id;
        }
      });
    }

    function initAdjustAnnotator() {
        $('table.video-annotator-table a.adjust-annotator').on('click', function(e) {
            var $target = $(e.target);
            var id = $target.data('id');
            var name = $target.data('name');
            var $listItem = $target.closest('li');
            var $vaSpan = $target.siblings('span.va');
            var $statusSpan = $vaSpan.find('span.status');
            var url, cb;

            e.preventDefault();

            if ($target.hasClass('remove')) {
                url = '/assignment/remove/';
                cb = function() { $listItem.remove(); };

            } else if ($target.hasClass('disable')) {
                url = '/assignment/disable/';
                cb = function() {
                    $vaSpan.addClass('disabled');
                    $statusSpan.text('Disabled');
                    $target
                        .removeClass('disable')
                        .addClass('enable')
                        .text('Enable');
                };

            } else if ($target.hasClass('enable')) {
                url = '/assignment/enable/';
                cb = function() {
                    $vaSpan.removeClass('disabled');
                    $statusSpan.text('In progress');
                    $target
                        .removeClass('enable')
                        .addClass('disable')
                        .text('Disable');
                }

            } else {
                return false;
            }

            if ($target.hasClass('remove') && !confirm('Are you sure you wish to remove ' + name + '?')) {
                return false;
            }

            $.ajax({
                url: url,
                type: 'post',
                data: { id: id },
                beforeSend: function(xhr) {
                    xhr.setRequestHeader('X-CSRFToken', getCSRF());
                }
            }).done(cb);
        });
    }

    function unknownType(container){
        var $containerEl = container;

        var get = function(id) {
        };
        var display = function($containerEl){
                $containerEl.empty()
                        .append($('<h4>Unknown Type</h4>'));
        };
        return {"get": get,
                "display": display};
    }


    function Trip(){
        var _fields = {"name": "",
                        "start_date": null,
                        "end_date": null,
                        "location": null,
                        "team": "",
                        "boat": "",
                        "pk": null};

        var get = function(id, callback){
            var cb =callback;
            $.get('/api/trips/' + id, function (data) {
                $.extend(true, _fields, data);
                if (cb){
                    cb();
                }
            });
        };

        var display = function($containerEl){
            $containerEl.empty()
                    .append($('<h4>' + name + '</h4><dl><dt>Start Date:</dt><dd>' + _fields.start_date +
                            '</dd><dt>End Date:</dt><dd>' + _fields.end_date +
                            '</dd><dt>Location:</dt><dd>' + _fields.location +
                            '</dd><dt>Team:</dt><dd>' + _fields.team +
                            '</dd><dt>Boat:</dt><dd>' + _fields.boat + '</dd></dl>'));

        };

        return {"name": _fields.name,
                "start_date": _fields.start_date,
                "end_date": _fields.end_date,
                "location": _fields.location,
                "team": _fields.team,
                "boat": _fields.boat,
                "pk": _fields.pk,
                "get": get,
                "display": display};
    }


    function Set(){
        var _fields = {"drop_time": null, "collection_time": null, "time_bait_gone": null, "equipment":"", "depth": "", "reef": "", "pk":0};

        var get = function(id, cb){
            $.get('/api/sets/' + id, function (data) {
                $.extend(true, _fields, data);
                if (cb){
                    cb();
                }
            });
        };

        var display = function($containerEl){
            $containerEl.empty()
                        .append($('<h4>' + moment(_fields.drop_time).format("dddd, MMMM Do YYYY, h:mm a") +
                                '</h4><dl><dt>drop time:</dt><dd>' + moment(_fields.drop_time).format("H:mm:ss") +
                                '</dd><dt>Collection Time</dt><dd>' + moment(_fields.collection_time).format("H:mm:ss") +
                                '</dd><dt>Bait Gone</dt><dd> '+ moment(_fields.time_bait_gone).format("H:mm:ss") +
                                '</dd><dt>Equipment</dt><dd> ' + _fields.equipment +
                                '</dd><dt>Depth</dt><dd> ' + _fields.depth +
                                '</dd><dt>Reef</dt><dd> ' + _fields.reef + '</dd></dl>'));

        };

        return {"drop_time": _fields.drop_time,
                "collection_time": _fields.collection_time,
                "time_bait_gone": _fields.time_bait_gone,
                "equipment": _fields.equipment,
                "depth": _fields.depth,
                "reef": _fields.reef,
                "pk": _fields.pk,
                "get": get,
                "display": display};
    }

    function Observation(){
        var _fields = {
            "drop_time": null,
            "collection_time": null,
            "time_bait_gone": null,
            "equipment":"",
            "depth": "",
            "reef": "",
            "pk":0
        };

        var get = function(id, cb){
            $.get('/api/observations/' + id, function (data) {
                $.extend(true, _fields, data);
                if (cb){
                    cb();
                }
            });
        };

        var display = function($containerEl){
            $containerEl.empty()
                        .append($('<h4>' + moment(_fields.drop_time).format("dddd, MMMM Do YYYY, h:mm a") +
                                '</h4><dl><dt>drop time:</dt><dd>' + moment(_fields.drop_time).format("H:mm:ss") +
                                '</dd><dt>Collection Time</dt><dd>' + moment(_fields.collection_time).format("H:mm:ss") +
                                '</dd><dt>Bait Gone</dt><dd> '+ moment(_fields.time_bait_gone).format("H:mm:ss") +
                                '</dd><dt>Equipment</dt><dd> ' + _fields.equipment +
                                '</dd><dt>Depth</dt><dd> ' + _fields.depth +
                                '</dd><dt>Reef</dt><dd> ' + _fields.reef + '</dd></dl>'));

        };

        return {"drop_time": _fields.drop_time,
                "collection_time": _fields.collection_time,
                "time_bait_gone": _fields.time_bait_gone,
                "equipment": _fields.equipment,
                "depth": _fields.depth,
                "reef": _fields.reef,
                "pk": _fields.pk,
                "get": get,
                "display": display};
    }

})(jQuery);
