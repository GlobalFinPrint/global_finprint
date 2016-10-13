$(function() {
    // Event view
    // handles rendering event tick onto the assignment timeline
    var EventView = Backbone.View.extend({
        template: _.template(Templates.eventView),
        render: function() {
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
        initialize: function() {
            this.view = new EventView({model: this})
        },
        getAssignment: function() {
            return this.collection.observation.getAssignment();
        },
        getTimePercent: function() {
            return this.get('event_time') / this.getAssignment().data('length') * 100;
        }
    });


    // Events collection
    // holder for event array
    var Events = Backbone.Collection.extend({
        model: Event
    });


    // Observation view
    // handles rendering an observation tick onto the assignment timeline
    var ObservationView = Backbone.View.extend({
        events: {
            'click': 'togglePopover',
            'click .observation-popover .close': 'closePopover',
            'click .observation-popover .selector': 'selectObservation',
            'click .event-thumbnail': 'showFullImage',
            'keydown': 'onKeypress'
        },
        template: _.template(Templates.observationView),
        render: function() {
            var templateData = _.extend({
                    left: this.model.getTimePercent() + '%',
                    animal: 'None <i>(Of Interest)</i>'
                }, this.model.attributes);
            this.setElement(this.template(templateData));
            this.model.getAssignment().find('.timeline').append(this.el);
            this.model.events.forEach(function(event) { event.view.render(); });
        },
        closePopover: function() {
            this.$el.removeClass('selected');
        },
        togglePopover: function(e) {
            if (e === undefined || e.target == this.el) {
                $('.observation').not(this.el).removeClass('selected').blur();
                this.$el.toggleClass('selected').focus();
            }
        },
        selectObservation: function() {
            this.$el.find('.observation-popover .selector').toggleClass('selected');
            this.model.toggleSelected();
        },
        showFullImage: function() {
            //TODO refactor this into separate method for re-use
            $('#full-image-modal')
                .find('div.event-image')
                    .css('background-image', 'url(' + this.model.get('initial_event').image_url +')')
                    .find('.extent')
                        .attr('style', this.model.get('initial_event').extent_css)
                        .end()
                    .end()
                .modal('show');
        },
        onKeypress: function(e) {
            if (e.which === 37) { // left
                this.model.previousModel().view.togglePopover();
            } else if (e.which === 39) { // right
                this.model.nextModel().view.togglePopover();
            } else if (e.which === 27) { // escape
                this.closePopover();
            } else if (e.which === 32) { // space
                this.selectObservation();
            }
        }
    });


    // Observation model
    // logic and data for observations
    var Observation = Backbone.Model.extend({
        constructor: function(attributes) {
            this.events = new Events;
            this.events.reset(attributes.events);
            this.events.observation = this;
            this.view = new ObservationView({ model: this });
            Backbone.Model.apply(this, arguments);
        },
        initialize: function() {
            this.set('selected', false); //TODO check master to see if they are selected yet
        },
        getAssignment: function() {
            return this.collection.view.$el;
        },
        getTimePercent: function() {
            return this.get('time') / this.getAssignment().data('length') * 100;
        },
        getMaster: function() {
            return this.collection.master;
        },
        nextModel: function() {
            return this.collection.nextModel(this);
        },
        previousModel: function() {
            return this.collection.previousModel(this);
        },
        toggleSelected: function() {
            this.set('selected', !this.get('selected'));
            if (this.get('selected')) {
                this.getMaster().addObservation(this);
            } else {
                this.getMaster().removeObservation(this);
            }
        }
    });


    // Assignment (observation collection)
    // fetches and holds observation array
    var Assignment = Backbone.Collection.extend({
        model: Observation,
        initialize: function(models, options) {
            this.view = options.view;
            this.url = '/assignment/detail/' + options.id;
            this.master = options.master;
        },
        parse: function(json) {
            return json.observations;
        },
        nextModel: function(currentModel) {
            if (currentModel === this.last()) {
                return this.first();
            } else {
                return this.at(this.indexOf(currentModel) + 1);
            }
        },
        previousModel: function(currentModel) {
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
        initialize: function(options) {
            var self = this;
            // _.bindAll(this, 'render');
            this.collection = new Assignment([], {
                id: this.$el.data('assignment-id'),
                view: this,
                master: options.masterView.collection
            });
            this.collection.fetch().then(function() {
                self.render();
                $('#busy-indicator').hide();
            });
        },
        render: function() {
            this.$el.find('.timeline').empty();
            this.collection.forEach(function(observation) { observation.view.render(); });
        }
    });


    // Master observation model
    // specifically for observations selected for master record
    var MasterObservation = Observation.extend({
        initialize: function() {
            this.set('selected', true);
        },
        toggleSelected: function() {
            this.get('original').view.selectObservation();
        }
    });


    // Master (observation collection)
    // holds selected observations for the master record
    var MasterRecord = Assignment.extend({
        model: MasterObservation,
        initialize: function(models, options) {
            this.view = options.view;
        },
        addObservation: function(model) {
            var attributes = model.toJSON();
            attributes.original = model;
            this.add(attributes);
            this.view.render();
        },
        removeObservation: function(model) {
            this.remove(this.get(model.get('id')));
            this.view.render();
        }
    });


    // Master view
    // displays data for the master record timeline
    var MasterView = AssignmentView.extend({
        initialize: function() {
            //TODO initialize with models in the master record
            this.collection = new MasterRecord([], {view: this});
        }
    });


    // Don't talk to server unless its a read
    var oldSync = Backbone.sync;
    Backbone.sync = function(method) {
        if (method === 'read') {
            return oldSync.apply(this, arguments);
        }
    };


    // initialize based on data loaded onto page
    var masterView = new MasterView({el: $('.row.master')[0]});
    $('.row.assignment').each(function(_, row) { new AssignmentView({el: row, masterView: masterView}); });


    // hook up save button
    $('#save-master').click(function() {
        var ids = masterView.collection.pluck('id');
        console.log(ids); //TODO actually save this to the server
    });
});
