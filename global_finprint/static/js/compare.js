$(function () {
    // Event view
    // handles rendering event tick onto the assignment timeline
    var EventView = Backbone.View.extend({
        template: _.template(Templates.eventView),
        render: function () {
            var templateData = _.extend({
                left: this.model.getTimePercent() + '%'
            }, this.model.attributes);
            this.setElement(this.template(templateData));
            this.model.getAssignment().find('.timeline').append(this.el);
        }
    });


    // Event model
    // logic and data for events
    var Event = Backbone.Model.extend({
        initialize: function () {
            this.view = new EventView({model: this});
        },
        getAssignment: function () {
            return this.collection.observation.getAssignment();
        },
        getTimePercent: function () {
            return this.get('event_time') / this.getAssignment().data('length') * 100;
        }
    });


    // Events collection
    // holder for event array
    var Events = Backbone.Collection.extend({
        model: Event,
        comparator: 'event_time'
    });


    // Observation view
    // handles rendering an observation tick onto the assignment timeline
    var ObservationView = Backbone.View.extend({
        events: {
            'click': 'togglePopover',
            'click .observation-popover .close': 'closePopover',
            'click .observation-popover .selector': 'selectObservation',
            'click .event-thumbnail:not(".empty")': 'showFullImage',
            'click .event-thumbnail .video-icon:not(".empty")': 'showFullClip',
            'keydown': 'onKeypress',
            'mouseover': 'onMouseOver',
            'mouseout': 'onMouseOut'
        },
        template: _.template(Templates.observationView),
        render: function () {
            var timePercent = this.model.getTimePercent();
            var popoverPosition = (timePercent > 50 ? 'right' : 'left') + ': calc(' + timePercent + '%' +
                (timePercent > 50 ? ' - 28px' : ' - 11px') + ');';
            var templateData = _.extend({
                left: timePercent + '%',
                popoverPosition: popoverPosition,
                leftRightAligned: timePercent > 50 ? 'right' : 'left',
                label: this.getLabel(),
                status_id: this.model.getAssignmentStatus()
            }, this.model.attributes);
            this.setElement(this.template(templateData));
            this.model.getAssignment().find('.timeline').append(this.el);
            this.model.events.forEach(function (event) {
                event.view.render();
            });
            this.initOnWindowLoad();
        },
        openPopover: function () {
            this.$el.addClass('selected').focus();
            this.activateEvents();
        },
        closePopover: function () {
            this.$el.removeClass('selected').blur();
            if (!this.$el.is(':hover')) {
                this.deactivateEvents();
            }
        },
        togglePopover: function (e) {
            if (e === undefined || e.target == this.el) {
                $('.event').removeClass('activated');
                $('.observation').not(this.el).removeClass('selected').blur();
                if (this.$el.hasClass('selected')) {
                    this.closePopover();
                } else {
                    this.openPopover();
                }
            }
        },
        selectObservation: function () {
            this.$el.find('.observation-popover .selector').toggleClass('selected');
            this.model.toggleSelected();
        },
        showFullImage: function (e) {
            var $modal = $('#full-image-modal')
            e.preventDefault();
            e.stopPropagation();
            var $currentTarget = $(e.currentTarget);
            var url = $currentTarget.data('img-url');
            var $image =$currentTarget.find('.image-icon');
            var img_temp= '<img width="500" height="500" style="padding-left:2.5em;padding-right:2.5em" src='+url+'>';
            $modal.find('.event-image').html(img_temp)
            $modal
                .find('.event-image')
                .attr('style', $image.attr('style'))
                .end()
                .find('.extent')
                .attr('style', this.model.get('initial_event').extent_css)
                .end()
                .modal('show');
        },
        showFullClip: function (event) {
            event.preventDefault();
            event.stopPropagation();
            var $target = $(event.target).closest('.event-thumbnail .video-icon');
            var url = $target[0].getAttribute("value")
            var video_temp= '<video width="500" height="500" controls>'+
                         '<source src='+url+' type="video/mp4"> </video>';
            $('#full-clip-modal').find('.event-clip').html(video_temp);
            $('#full-clip-modal').find('.event-clip')
                .attr('style', $target.attr('style'))
                .end()
                .modal('show');

        },
        onKeypress: function (e) {
            if (e.which === 37) { // left
                this.closePopover();
                this.model.previousModel().view.openPopover();
            } else if (e.which === 39) { // right
                this.closePopover();
                this.model.nextModel().view.openPopover();
            } else if (e.which === 27) { // escape
                this.closePopover();
                this.$el.closest('.row').focus();
            } else if (e.which === 32) { // space
                this.selectObservation();
            }
        },
        getLabel: function () {
            return this.model.has('original') ? this.model.get('original').collection.label : '';
        },
        onMouseOver: function () {
            this.activateEvents();
        },
        onMouseOut: function () {
            if (!this.$el.hasClass('selected')) {
                this.deactivateEvents();
            }
        },
        activateEvents: function () {
            this.model.events.map(function (eventModel) {
                eventModel.view.$el.addClass('activated');
            });
        },
        deactivateEvents: function () {
            this.model.events.map(function (eventModel) {
                eventModel.view.$el.removeClass('activated');
            });
        },
        initOnWindowLoad: function () {
              this.checkPropImage();
       },
       checkPropImage : function () {
                var self = this;
                $('img.image-icon:not(.loaded)').each(function () {
                    var currImg = $(this);
                    var src = currImg.data('src');
                    if (!src) return;

                    var img = new Image();
                    img.onload = function () {
                        // code to set the src on success
                        currImg.addClass('loaded');
                        var video = currImg.siblings('.video-icon');
                        self.checkPropVideo(video);
                    };
                    img.onerror = function () {
                        // doesn't exist or error loading
                        console.log('no image');
                        currImg.attr('src', '/static/images/default-image.jpg');
                    };
                    setTimeout(function () {
                            img.src = src; // fires off loading of image
                            currImg.attr('src', src);
                    }, 0);
                });
        },
       checkPropVideo: function (video_span) {
                    var curr_icon = video_span;
                    var url = curr_icon.attr('value');
                    if (!url) return;

                    var video = document.createElement('VIDEO');
                    if (video.canPlayType("video/mp4")) {
                        video.setAttribute("src",url);
                     }

                    video.onloadedmetadata = function() {
                          console.log("Meta data for video loaded");
                    };
                    video.onerror = function () {
                        // doesn't exist or error loading
                        console.log('no video');
                        curr_icon.attr('style', 'display:none');
                    };
                    setTimeout(function () {
                           // curr_icon.attr('style', 'display:true');
                    }, 0);

       }
       });


    // Observation model
    // logic and data for observations
    var Observation = Backbone.Model.extend({
        defaults: {
            animal: 'None <i>(Of Interest)</i>',
            selected: false,
            group: 'int'
        },
        constructor: function (attributes) {
            this.events = new Events;
            this.events.reset(attributes.events);
            this.events.observation = this;
            this.view = new ObservationView({model: this});
            Backbone.Model.apply(this, arguments);
        },
        getAssignment: function () {
            return this.collection.view.$el;
        },
        getTimePercent: function () {
            return this.get('time') / this.getAssignment().data('length') * 100;
        },
        getMaster: function () {
            return this.collection.master;
        },
        getAssignmentStatus: function () {
            return this.collection.status_id;
        },
        nextModel: function () {
            return this.collection.nextModel(this);
        },
        previousModel: function () {
            return this.collection.previousModel(this);
        },
        toggleSelected: function () {
            this.set('selected', !this.get('selected'));
            if (this.get('selected')) {
                this.getMaster().addObservation(this);
            } else {
                this.getMaster().removeObservation(this);
            }
        },
        select: function () {
            if (!this.get('selected')) {
                this.set('selected', true);
                this.view.$el.find('.observation-popover .selector').addClass('selected');
                this.getMaster().addObservation(this);
            }
        }
    });

    // Assignment (observation collection)
    // fetches and holds observation array
    var Assignment = Backbone.Collection.extend({
        model: Observation,
        comparator: 'time',
        initialize: function (models, options) {
            this.view = options.view;
            this.url = '/assignment/detail/' + options.id;
            this.master = options.master;
            this.label = options.label;
            this.status_id = options.status_id;
        },
        parse: function (json) {
            return json.observations;
        },
        nextModel: function (currentModel) {
            if (currentModel === this.last()) {
                return this.first();
            } else {
                return this.at(this.indexOf(currentModel) + 1);
            }
        },
        previousModel: function (currentModel) {
            if (currentModel === this.first()) {
                return this.last();
            } else {
                return this.at(this.indexOf(currentModel) - 1);
            }
        }
    });


    // Assignment view
    // handles fetching observation data and rendering for a single assignment
    var AssignmentView = Backbone.View.extend({
        events: {
            'click .timeline-holder': 'timelineHighlight',
            'click button.select-all': 'selectAll',
            'keydown': 'onKeypress'
        },
        initialize: function (options) {
            var self = this;
            this.loadingPromise = $.Deferred();
            this.collection = new Assignment([], {
                id: this.$el.data('assignment-id'),
                view: this,
                master: options.masterView.collection,
                label: this.$el.data('label'),
                status_id: this.$el.data('status-id')
            });
            this.collection.fetch().then(function () {
                self.render();
                self.$el.find('.busy-indicator').fadeOut();
                self.loadingPromise.resolve();
            });
        },
        render: function () {
            this.$el.find('.timeline').empty();
            this.collection.forEach(function (observation) {
                observation.view.render();
            });
        },
        timelineHighlight: function (e) {
            // don't do anything if we are already highlighted or not "reviewed"
            if (this.$el.find('.timeline-holder').hasClass('highlighted')
                    || this.collection.status_id !== 4) {
                return;
            }

            // un-highlight other timelines and highlight us
            $('.timeline-holder').removeClass('highlighted');
            this.$el.find('.timeline-holder').addClass('highlighted');

            // if we click directly on the timeline then bring up the first observation popover (if available)
            if ($(e.target).is('.timeline-holder, .timeline')) {
                $('.event').removeClass('activated');
                $('.observation').removeClass('selected').blur();
                if (this.collection.length > 0) {
                    this.collection.first().view.openPopover();
                } else {
                    this.$el.focus();
                }
            }
        },
        selectAll: function () {
            this.collection.each(function (observation) {
                observation.select();
            });
        },
        onKeypress: function (e) {
            var $prev, $next;
            if (e.which === 38) { // up
                $prev = this.$el.prev('.master, .assignment');
                if ($prev.length) {
                    $prev.find('.timeline-holder').click();
                }
            } else if (e.which === 40) { // down
                $next = this.$el.next('.master, .assignment');
                if ($next.length) {
                    $next.find('.timeline-holder').click();
                }
            } else if (e.which === 37 || e.which === 39) { // left or right
                if (this.$el.find('.observation.selected').length === 0) {
                    this.collection.first().view.openPopover();
                }
            }
        }
    });
    // Master observation model
    // specifically for observations selected for master record
    var MasterObservation = Observation.extend({
        default: {
            selected: true
        },
        toggleSelected: function () {
            var nextModelView = this.nextModel().view;
            this.get('original').view.selectObservation();
            nextModelView.openPopover();
        }
    });


    // Master (observation collection)
    // holds selected observations for the master record
    var MasterRecord = Assignment.extend({
        model: MasterObservation,
        initialize: function (models, options) {
            this.view = options.view;
            this.url = '/assignment/master/' + options.id;
            this.project = options.project;
        },
        addObservation: function (model) {
            var attributes = model.toJSON();
            attributes.original = model;
            this.add(attributes);
            this.view.render();
        },
        removeObservation: function (model) {
            this.remove(this.get(model.get('id')));
            this.view.render();
        }
    });


    // Master view
    // displays data for the master record timeline
    var MasterView = AssignmentView.extend({
        events: {
            'click button#save-master': 'saveMaster',
            'click button#review-master': 'reviewMaster'
        },
        initialize: function (options) {
            this.loadingPromises = options.loadingPromises;
            this.collection = new MasterRecord([], {
                id: this.$el.data('set-id'),
                project: this.$el.data('project-id'),
                view: this
            });
        },
        saveMaster: function () {
            var $this = $(this);
            var $feedback = $('span#save-feedback');
            var data = {
                observation_ids: this.collection.pluck('id'),
                project: this.collection.project
            };

            $this.attr('disabled', 'disabled');

            $.post(this.collection.url, data, function (res) {
                $this.removeAttr('disabled');
                if (res.success === 'ok') {
                    $feedback
                        .removeClass('failure')
                        .addClass('success')
                        .text('Changes saved!')
                        .show()
                        .delay(1000)
                        .fadeOut();
                } else if (res.success === 'no changes') {
                    $feedback
                        .removeClass('success failure')
                        .text('No changes to save...')
                        .show()
                        .delay(1000)
                        .fadeOut();
                }

            }).error(function () {
                $this.removeAttr('disabled');
                $feedback
                    .removeClass('success')
                    .addClass('failure')
                    .text('Encountered an error saving changes; please try again later.')
                    .show()
                    .delay(1000)
                    .fadeOut();
            });
        },
        reviewMaster: function () {
            var $this = $(this);
            var $feedback = $('span#save-feedback');
            var data = {
                observation_ids: this.collection.pluck('id'),
                project: this.collection.project
            };

            $this.attr('disabled', 'disabled');

            $.post(this.collection.url, data, function (res) {
                $this.removeAttr('disabled');
                if (res.success === 'ok') {
                    $feedback
                        .removeClass('failure')
                        .addClass('success')
                        .text('Changes saved!')
                        .show()
                        .delay(1000)
                        .fadeOut();
                }
                window.location.href = $('button#review-master').attr('data-href-target');
            }).error(function () {
                $this.removeAttr('disabled');
                $feedback
                    .removeClass('success')
                    .addClass('failure')
                    .text('Encountered an error saving changes; please try again later.')
                    .show()
                    .delay(1000)
                    .fadeOut();
            });
        },
        load: function (loadingPromises) {
            var self = this;
            $.get(this.collection.url + '?project=' + this.collection.project, function (res) {
                $.when.apply($, loadingPromises).done(function () {
                    var ids = res.original_observation_ids;
                    _.each(assignmentViews, function (view) {
                        view.collection.forEach(function (model) {
                            if (ids.indexOf(model.id) !== -1) {
                                model.select();
                                self.collection.addObservation(model);
                            }
                        });
                    });
                    self.render();
                    self.$el.find('.busy-indicator').fadeOut();
                    $('button.select-all, button#save-master, button#review-master').removeAttr('disabled');
                });
            });
        }
    });


    // Don't talk to server with Backbone unless its a 'read'
    var oldSync = Backbone.sync;
    Backbone.sync = function (method) {
        if (method === 'read') {
            return oldSync.apply(this, arguments);
        }
    };


    // initialize based on data loaded onto page
    var masterView = new MasterView({el: $('.row.master')[0]});
    var assignmentViews = $('.row.assignment').map(function (_, row) {
        return new AssignmentView({el: row, masterView: masterView});
    });
    masterView.load(_.map(assignmentViews, function (view) {
        return view.loadingPromise;
    }));


    $(function () {
        var $style;
        var colors = colorbrewer.Set1[9];
        var intColor = colors.pop();
        $('head').append('<style class="legend-style"></style>');
        $style = $('style.legend-style');
        $('.compare-actions .legend .legend-item').each(function (i, li) {
            var style = '.group-' + $(li).data('group') + ' { background-color: ' + colors[i + 1] + ' !important; ';
            if (i === 4) { // for bright colors that need black text color
                style += 'color: black !important; ';
            }
            style += '}\n';
            $style.append(style);
        });
        $style.append('.group-int { background-color: ' + intColor + ' !important; }\n')
    });
});
