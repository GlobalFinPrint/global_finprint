var finprint = finprint || {};  //namespace if necessary...

(function($) {
    "use strict";

    $(function() {
        initToggleEnv();
        initAssignForm();
        initAdjustAnnotator();
        initAssignButtons();
        initAssignmentSearch();
        initAssignmentModals();
        initShowFormButtons();
        initManageStateButtons();
        initAutomaticAssignment();
        initAnnotatorPopover();
        initCollapse();
        initSelectizeWidgets();
        initImageSelectWidgets();
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

    function initToggleEnv() {
        $('table.set-table').find('a.show-env, a.hide-env').click(function(e) {
            e.preventDefault();
            $(this).hide()
                .siblings().toggle().end()
                .closest('table.set-table')
                    .find('tr.set-' + $(this).data('set')).toggle();
        });
    }

    function initAnnotatorPopover() {
        $('body').on('click', 'a[data-annotator-id][href="#"]', function(e) {
            var $this = $(this);
            var annoId = $this.data('annotator-id');
            e.preventDefault();
            $this.removeAttr('data-annotator-id');
            $.get('/user/info/' + annoId, function(res) {
                $this.popover({
                    title: res.name + ' (' + res.affiliation + ')',
                    content: res.content,
                    html: true,
                    placement: 'top'
                });
                $this.on('click', function(e) {
                    e.preventDefault();
                });
                $this.click();
            });
        });
    }

    function initAssignmentSearch() {
        var $form = $('form#assignment-search-form');
        var $target = $('tbody#assignment-target');
        var options = { allowEmptyOption: true, plugins: ['remove_button', 'restore_on_backspace'] };
        var fields = [
            '#select-trip',
            '#select-set',
            '#select-anno',
            '#select-status'
        ];

        $form.submit(false);
        fields.forEach(function(selector) {
            $form.find(selector).selectize(options);
        });
        $form.find('button#search').click(function() {
            $.post('/assignment/search', $form.serialize(), function(res) {
                $target.html(res);
            });
        });
    }

    function initAssignmentModals() {
        var $buttons = $('tbody#assignment-target');
        var $modal = $('div#assign-modal');

        $buttons.on('click', 'a.open-assign-modal', function(e) {
            e.preventDefault();
            $.get('/assignment/modal/' + $(this).data('id'), function(html) {
                $modal.find('div.modal-content').html(html);
                $modal.find('form').submit(false);
                $modal.find('#new-annotators').selectize({ plugins: ['remove_button', 'restore_on_backspace'] });
                $modal.modal('show');
            });
        });

        $modal.on('click', 'button#save-changes', function() {
            $.post('/assignment/modal/' + $(this).data('id'), $modal.find('form').serialize(), function() {
                $modal.modal('hide');
                $('form#assignment-search-form button#search').click();
            });
        });
    }

    function initShowFormButtons() {
        var showSetForm = function() {
            $('#btn-show-set-form').hide();
            $('#set-form-parent').show();
            window.location.hash = '#set-form-parent';
        };

        var showTripForm = function() {
            $('#btn-show-trip-form').hide();
            $('#trip-form-parent').show();
            window.location.hash = '#trip-form-parent';
        };

        var checkHash = function() {
            if (window.location.hash === '#set-form-parent') {
                showSetForm();
            } else if (window.location.hash === '#trip-form-parent') {
                showTripForm();
            }
        };

        window.onhashchange = checkHash;
        checkHash();

        $('#btn-show-set-form').click(showSetForm);
        $('#btn-show-trip-form').click(showTripForm);
    }

    function initManageStateButtons() {
        var $buttons = $('div.manage-state-buttons');
        var assignmentId = $buttons.data('id');

        $buttons.find('form').submit(function() {
            var action = $(this).find('input[name="action"]').val();
            if (action === 'delete' && confirm('Are you sure you wish to delete this assignment?')) {
                $.post('/assignment/manage/' + assignmentId, $(this).serialize(), function() {
                    $('.manage-content')
                        .html('<div class="row"><h3 class="text-center">Assignment deleted</h3></div>');
                });
            } else if (action !== 'delete') {
                $.post('/assignment/manage/' + assignmentId, $(this).serialize(), function() {
                    window.location.reload(true);
                });
            }
            return false;
        });
    }

    function initAutomaticAssignment() {
        var $openLink = $('#open-auto-modal');
        var $modal = $('#automatic-modal');
        var $modalForm = $modal.find('form');

        $modalForm.submit(false);

        $openLink.click(function(e) {
            e.preventDefault();
            $modal.modal('show');
        });

        $modal.find('#assign-auto').click(function() {
            $modal.find('div.modal-footer span.success-message').fadeOut().removeClass('alert-error');
            $.post('/assignment/auto', $modalForm.serialize(), function(data) {
                var $aa = data['assignments'];
                var $message = ['Processed',
                                data['video_count'],
                                'video(s).',
                                $aa['assigned'],
                                'assignment(s) made',
                                ['(', $aa['newly_assigned'], ' new).'].join('')
                               ].join(' ');
                if ($aa['assigned'] < $aa['total']){
                    $modal.find('div.modal-footer span.success-message').addClass('alert-error')
                }
                $modal.find('div.modal-footer span.success-message').text($message).fadeIn();
            });
        });
    }

    function initAssignForm() {
      var $form = $('form.video-annotator');
      var $video = $form.find('#id_video');
      var $affiliation = $form.find('#id_affiliation');
      var $annotator = $form.find('#id_annotators');

      $annotator.empty().multiselect();

      $form.find('#id_video, #id_affiliation').change(function() {
        $.get('/assignment/list/', { video: $video.val(), affiliation: $affiliation.val() }, function(res) {
          $annotator
            .find('option:not(:selected)')
              .remove().end()
            .append(res.annotators.map(function (a) {
              return "<option value='" + a.id + "'>" + a.user + "</option>";
            }));
          $annotator.multiselect('rebuild');
        });
      });
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
        var tripId = $form.find('#id_trip').val();
        var affId = $form.find('#id_affiliation').val();
        if (tripId && affId) {
          window.location.href = '/assignment/auto/' + tripId + '_' + affId;
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

    function initCollapse() {
        var $parent = $('tbody#collapse-parent');

        $parent.find('tr.first-event').on('click', function() {
            var target, rowspan;
            var alreadyToggled = $(this).hasClass('selected');

            // hide all children and deselect everything
            $parent
                .find('tr.child-row')
                    .hide()
                    .end()
                .find('tr.first-event')
                    .removeClass('selected')
                    .find('td.rowspan')
                        .removeAttr('rowspan');

            // select the current and show children (if its not already selected)
            if (!alreadyToggled) {
                target = $(this).data('target');
                rowspan = $(this).data('rowspan');
                $(this)
                    .addClass('selected')
                    .find('td.rowspan')
                        .attr('rowspan', rowspan);
                $parent.find(target).show();
            }
        });
    }

    function initSelectizeWidgets() {
        $('select[multiple="multiple"].selectize').selectize({ plugins: ['remove_button', 'restore_on_backspace'] });
    }

    function initImageSelectWidgets() {
        $('div.image-select-widget-parent input').click(function(e) {
            e.stopPropagation();
        }).change(function() {
            //TODO update UI for filename
            console.log($(this).val());
        });

        $('div.image-select-widget-parent').click(function(e) {
            e.preventDefault();
            $(this).find('input').click();
        });
    }
})(jQuery);
