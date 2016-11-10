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
        initTabAccordion();
        initSubstrateWidget();
        initCheckbuttons();
        initColoredRows();
        initDisableOnSubmit();
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
            var $this = $(this);
            var oldText = $this.text();
            $this.attr('disabled', 'disabled');
            $this.text('Searching...');
            $.post('/assignment/search', $form.serialize(), function(res) {
                $target.html(res);
                $this.removeAttr('disabled');
                $this.text(oldText);
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
        $('div.image-select-widget-parent').each(function(_, parent) {
            var $parent = $(parent);

            $parent.find('input').click(function(e) {
                e.stopPropagation();
            }).change(function() {
                var $this = $(this);
                var file = $this.val().match(/[^\\]+$/)[0];
                $parent.find('.caption').text('New file: ' + file);
                $parent.find('.image-select-widget').css('opacity', 0.5)
            });

            $parent.click(function(e) {
                e.preventDefault();
                $(this).find('input').click();
            });
        });
    }

    function initTabAccordion() {
        var $form = $('#set-env-form');

        function scrollTo(selector) {
            $('html, body').animate({
                scrollTop: $(selector).offset().top
            }, 1000);
        }

        $form.on('keydown', '#id_code', function(e) {
            if (e.which === 9) { // tab key
                $('#headingTwo.collapsed').click();
                scrollTo('#headingTwo');
            }
        });

        $form.on('keydown', '.selectize-control input', function(e) {
            if (e.which === 9) { // tab key
                $('#headingThree.collapsed').click();
                scrollTo('#headingThree');
            }
        });

        $form.on('keydown', '#id_drop-surface_chop', function(e) {
            if (e.which === 9) { // tab key
                $('#headingFour.collapsed').click();
                scrollTo('#headingFour');
            }
        });

        $form.on('keydown', '#id_haul-surface_chop', function(e) {
            if (e.which === 9) { // tab key
                $('#headingFive.collapsed').click();
                scrollTo('#headingFive');
            }
        });
    }

    function initSubstrateWidget() {
        var $parent = $('.habitat-substrate-parent');
        var $left = $parent.find('.left');
        var $center = $parent.find('.center');
        var $right = $parent.find('.right');

        function recalculateTotalPercent() {
            var percents = $.map($('input[name="percent"]'), function(i) { return parseInt($(i).val()); });
            var sum = percents.reduce(function(sum, x) { return sum + x; }, 0);
            $parent.find('input[name="total-percent"]').val(sum);
        }

        function addSubstrateRow(e, substrate, value) {
            e.preventDefault();

            var remainingPercent = Math.max(0, 100 - $parent.find('input[name="total-percent"]').val());

            $.get('/substrate/', function(res) {
                var html = '<div class="substrate-row"><select class="substrate select form-control" name="substrate">';
                res.substrates.forEach(function(s) {
                    var selected = (parseInt(s.id) === parseInt(substrate)) ? ' selected="selected"' : '';
                    html += '<option value="' + s.id + '"' + selected + '>' + s.name + '</option>';
                });
                html += '</select></div>';
                $left.prepend(html);

                $center.prepend('<div class="substrate-row"><div class="input-holder">' +
                    '<input class="percent" name="percent" type="number" ' +
                        'step="1" min="1" max="100" value="' + (value ? parseInt(value) : parseInt(remainingPercent)) + '" />' +
                    '</div></div>');

                $right.prepend('<div class="substrate-row">' +
                    '<a href="#" class="split">Split</a>' +
                    '<a href="#" class="remove">Remove</a>' +
                    '</div>');

                recalculateTotalPercent();
            });
        }

        function removeSubstrateRow(e) {
            e.preventDefault();

            var index = $right.find('a.remove').index($(this));
            $left.find('.substrate-row').slice(index, index + 1).remove();
            $center.find('.substrate-row').slice(index, index + 1).remove();
            $right.find('.substrate-row').slice(index, index + 1).remove();
            recalculateTotalPercent();
        }

        function splitModal(e) {
            e.preventDefault();

            var $originalThis = $(this);
            var index = $right.find('a.split').index($originalThis);
            var parentId = $left.find('select.substrate').slice(index, index + 1).val();
            var parentPercent = $center.find('input[type="number"]').slice(index, index + 1).val();
            var $splitModal = $('div.split-modal');
            var position = $(this).position().top + 30 + 'px';

            if ($splitModal.length) {
                return $splitModal.remove();
            }

            $.get('/substrate/', { parent_id: parentId }, function(res) {
                var $subLeft, $subCenter, $subRight, modalHtml, messageHtml;

                if (!res.substrates.length) {
                    messageHtml = '<div class="message-modal clear">' +
                        '<p class="no-children-message">' +
                            'This substrate has no children; unable to split' +
                        '</p></div>';
                    $parent.append(messageHtml);
                    $parent.find('.message-modal')
                        .css('top', position)
                        .delay(1500)
                        .fadeOut(300, function() { $(this).remove(); });
                    return false;
                }

                function getModalPercentSum() {
                    var $inputs = $parent.find('.split-modal .center input.percent');
                    var percents = $.map($inputs, function(i) { return parseInt($(i).val()); });
                    return percents.reduce(function(sum, x) { return sum + x; }, 0);
                }

                function recalculateModalPercent() {
                    $parent.find('.split-modal .center input.total').val(getModalPercentSum());
                }

                function showSubError(message) {
                    $splitModal.find('.buttons span.sub-error')
                        .text(message)
                        .fadeIn(500)
                        .delay(1500)
                        .fadeOut(500, function() { $(this).text(''); });
                }

                modalHtml = '<div class="split-modal clear">' +
                    '<div class="left">' +
                        '<div class="substrate-row">' +
                            '<select class="substrate select form-control">';
                res.substrates.forEach(function(s) {
                    modalHtml += '<option value="' + s.id + '">' + s.name + '</option>';
                });
                modalHtml += '</select></div>';
                modalHtml += '<div class="substrate-row"><button class="btn btn-primary btn-fp add-substrate">+</button>' +
                    '<span class="total">Total</span>' +
                    '</div></div>';

                modalHtml += '<div class="center">' +
                        '<div class="substrate-row">' +
                            '<div class="input-holder">' +
                                '<input class="percent" type="number" value="' + parentPercent + '" step="1" min="1" max="100" />' +
                            '</div>' +
                        '</div>' +
                        '<div class="substrate-row">' +
                            '<div class="input-holder"><input class="total" type="number" readonly="readonly" /></div>' +
                        '</div>' +
                    '</div>';

                modalHtml += '<div class="right">' +
                        '<div class="substrate-row">' +
                            '<a href="#" class="modal-remove">Remove</a>' +
                        '</div>' +
                        '<div class="substrate-row">' +
                            '<span class="help-text">Details must total ' + parentPercent + '%</span>' +
                        '</div>' +
                    '</div>';

                modalHtml += '<div class="buttons">' +
                        '<span class="sub-error"></span>' +
                        '<button class="btn btn-default btn-fp sub-cancel">Cancel</button>' +
                        '<button class="btn btn-primary btn-fp sub-ok">OK</button>' +
                    '</div></div>';

                $parent.append(modalHtml);
                $splitModal = $($splitModal.selector);
                $splitModal.css('top', position);

                $subLeft = $splitModal.find('.left');
                $subCenter = $splitModal.find('.center');
                $subRight = $splitModal.find('.right');

                $splitModal.on('click', '> .left button.add-substrate', function(e) {
                    e.preventDefault();

                    var remainingPercent = Math.max(0, parentPercent - $subCenter.find('input.percent').val());

                    var leftHTML = '<div class="substrate-row"><select class="substrate select form-control">';
                    res.substrates.forEach(function(s) {
                        leftHTML += '<option value="' + s.id + '">' + s.name + '</option>';
                    });
                    leftHTML += '</select></div>';
                    $subLeft.prepend(leftHTML);

                    $subCenter.prepend('<div class="substrate-row">' +
                        '<div class="input-holder">' +
                            '<input class="percent" type="number" value="' + remainingPercent + '" step="1" min="1" max="100" />' +
                    '</div></div>');

                    $subRight.prepend('<div class="substrate-row">' +
                        '<a href="#" class="modal-remove">Remove</a>' +
                    '</div>');

                    recalculateModalPercent();
                });

                $splitModal.on('click', '> .right a.modal-remove', function(e) {
                    e.preventDefault();
                    var index = $subRight.find('a.modal-remove').index($(this));
                    $subLeft.find('.substrate-row').slice(index, index + 1).remove();
                    $subCenter.find('.substrate-row').slice(index, index + 1).remove();
                    $subRight.find('.substrate-row').slice(index, index + 1).remove();
                });

                $splitModal.on('click', '> .buttons button.sub-cancel', function(e) {
                    e.preventDefault();
                    return $splitModal.remove();
                });

                $splitModal.on('click', '> .buttons button.sub-ok', function(e) {
                    e.preventDefault();
                    var $substrates, subVals, $percents, checkRange;

                    $splitModal.find('.buttons span.sub-error').hide().clearQueue();

                    // allowed range check
                    $percents = $subCenter.find('input.percent');
                    checkRange = function (p) {
                        return parseInt($(p).val()) > 100 || parseInt($(p).val()) < 1
                    };
                    if ($.grep($percents, checkRange).length) {
                        showSubError('Substrate value must be between 1 and 100');
                        return false;
                    }

                    // check for dupe substrates
                    $substrates = $subLeft.find('select.substrate');
                    subVals = $.map($substrates, function (s) {
                        return $(s).val();
                    });
                    if (subVals.length !== $.unique(subVals).length) {
                        showSubError('Must not have duplicate substrates');
                        return false;
                    }

                    // check parent percent match
                    if (parseInt($subCenter.find('input.total').val()) != parentPercent) {
                        showSubError('Substrates must total ' + parentPercent + '%');
                        return false;
                    }

                    // split on the parent
                    $splitModal.hide();
                    removeSubstrateRow.call($originalThis.siblings('a.remove'), new Event('remove row'));
                    $substrates.each(function(i, sub) {
                        addSubstrateRow(new Event('add row'), $(sub).val(), $percents.slice(i, i+1).val());
                    });
                    $splitModal.remove();
                });

                $splitModal.on('change', 'input.percent', recalculateModalPercent);

                recalculateModalPercent();
            });
        }

        $parent.find('> .left button.add-substrate').click(addSubstrateRow);

        $parent.on('change', 'input[name="percent"]', recalculateTotalPercent);
        $parent.on('click', 'a.split', splitModal);
        $parent.on('click', 'a.remove', removeSubstrateRow);
    }

    function initCheckbuttons() {
        var url, data;
        $('.checkbutton').click(function(e) {
            if (e.target === this) {
                url = $(this).data('url');
                data = {checked: !$(this).find('input[type="checkbox"]').is(':checked')};
                $.get(url, data);
            }
        });
    }

    function initColoredRows() {
        var palette = colorbrewer.Set1[9];
        var pallIndex = 0;
        var $colorRowContainer = $('.color-rows');
        var diffCell = parseInt($colorRowContainer.data('diff-cell'));
        var diffDict = {};
        var rows = $colorRowContainer.find('table tbody tr.first-event');
        var css = 'content: ""; display: inline-block; height: 5px; width: 5px; border: 5px solid black; ' +
            'border-radius: 5px; margin-right: 5px;';
        rows.each(function(i, row) {
            var cell = $(row).find('td')[diffCell];
            var diffKey = cell.innerText;
            if (diffDict[diffKey] === undefined) {
                document.styleSheets[0].addRule(
                    '.color-rows table tbody tr td[data-pall-index="' + pallIndex + '"]:before',
                    css + 'border-color: ' + palette[pallIndex] + ';'
                );
                diffDict[diffKey] = pallIndex;
                pallIndex +=1 ;
            }
            $(cell).attr('data-pall-index', diffDict[diffKey]);
        });
    }

    function initDisableOnSubmit() {
        // $('input[type="submit"]').click(function() {
        //     $('input[type="submit"]').attr('disabled', 'disabled');
        // });
    }
})(jQuery);
