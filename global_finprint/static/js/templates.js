var Templates = {
    eventView: '<div class="event" style="left:calc(<%= left %> - 6px);"></div>',
    observationView: '<div class="observation group-<%= group %>" style="left:calc(<%= left %> - 10px);" tabindex="0">' +
            '<%= label %>' +
            '<div class="observation-popover clear <%= leftRightAligned %>-aligned" style="<%= popoverPosition %>">' +
                '<div class="left">' +
                    '<div><%= pretty_time %></div>' +

                    '<% if (initial_event.image_url) { %>' +
                        '<div class="event-thumbnail" style="background-image:url(<%= initial_event.image_url %>)">' +
                            '<div class="extent" style="<%= initial_event.extent_css %>">&nbsp;</div>' +
                        '</div>' +
                    '<% } else { %>' +
                        '<div class="event-thumbnail empty"></div>' +
                    '<% } %>' +

                    '<% if (assignment.status == 4) { %>' +
                    '<div class="selector<%= selected ? " selected" : "" %>">' +
                        '<span class="checkmark glyphicon glyphicon-ok"></span>' +
                        '<div class="empty-selection">&nbsp;</div>' +
                    '</div>' +
                    '<% } %>' +

                '</div>' +
                '<div class="right">' +
                    '<table><tbody>' +
                        '<tr>' +
                            '<td class="data-label">Organism</td>' +
                            '<td class="data"><%= animal %></td>' +
                        '</tr>' +
                        '<tr>' +
                            '<td class="data-label">Obs. note</td>' +
                            '<td class="data"><%= comment %></td>' +
                        '</tr>' +
                        '<tr>' +
                            '<td class="data-label">Duration</td>' +
                            '<td class="data"><%= duration %></td>' +
                        '</tr>' +
                        '<tr>' +
                            '<td class="data-label">Image notes</td>' +
                            '<td class="data"><%= initial_event.note %></td>' +
                        '</tr>' +
                        '<tr>' +
                            '<td class="data-label">Tags</td>' +
                            '<td class="data"><%= initial_event.attribute_names.join(", ") %></td>' +
                        '</tr>' +
                    '</tbody></table>' +
                '</div>' +
                '<div class="close">&times;</div>' +
            '</div>' +
        '</div>'
};
