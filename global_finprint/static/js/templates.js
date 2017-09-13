var Templates = {
    eventView: '<div class="event" style="left:calc(<%= left %> - 6px);"></div>',

    observationView: '<div class="observation group-<%= group %>" style="left:calc(<%= left %> - 10px);" tabindex="0">' +
            '<%= label %>' +
            '<div class="observation-popover clear <%= leftRightAligned %>-aligned" style="<%= popoverPosition %>">' +
                '<div class="row">' +
                    '<b class="observation-title"><%= animal %></b>' +
                '</div>' +

                '<div class="row">' +
                // '<table><tbody>' +
                //     '<tr>' +
                //         '<td class="data-label">Organism</td>' +
                //         '<td class="data"><%= animal %></td>' +
                //     '</tr>' +
                //     '<tr>' +
                //         '<td class="data-label">Obs. note</td>' +
                //         '<td class="data"><%= comment %></td>' +
                //     '</tr>' +
                //     '<tr>' +
                //         '<td class="data-label">Duration</td>' +
                //         '<td class="data"><%= duration %></td>' +
                //     '</tr>' +
                // '</tbody></table>' +

                // '<div class="panel-group" id="accordion" role="tablist" aria-multiselectable="true">' +
                //     '<div class="panel panel-default">' +
                //         '<div class="panel-heading" role="tab" id="headingOne">' +
                //         '<h4 class="panel-title">' +
                //             '<a role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseOne" aria-expanded="true" aria-controls="collapseOne">' +
                //                 '<div><%= pretty_time %></div>' +
                //             '</a>' +
                //         '</h4>' +
                //     '</div>' +
                //     '<div id="collapseOne" class="panel-collapse collapse in" role="tabpanel" aria-labelledby="headingOne">' +
                //         '<div class="panel-body">' +

                            '<div class="left">' +
                                '<% if (initial_event.image_url) { %>' +
                                    '<div class="event-thumbnail" data-img-url="<%= initial_event.image_url%>" data-image-name="<%= animal %>">' +
                                        '<img class="image-icon" src="/static/images/loading_spinner.gif" data-src="<%= initial_event.image_url%>" style="width:100%">'+
                                        '<div class="extent" style="<%= initial_event.extent_css %>">&nbsp;</div>'+
                                        '<% if (initial_event.clip_url) { %>' +
                                          ' <span class="video-icon" value="<%= initial_event.clip_url%>">&#9658;</span>' +
                                        '<% } %>'+
                                    '</div>' +
                                '<% } else { %>' +
                                    '<div class="event-thumbnail empty"></div>' +
                                '<% } %>' +

                                '<% if (status_id == 4 || !status_id) { %>' +
                                '<div class="selector<%= selected ? " selected" : "" %>">' +
                                    '<span class="checkmark glyphicon glyphicon-ok"></span>' +
                                    '<div class="empty-selection">&nbsp;</div>' +
                                '</div>' +
                                '<% } %>' +

                            '</div>' +
                            '<div class="right">' +
                                '<table><tbody>' +
                                    '<tr>' +
                                        '<td class="data-label">Event time</td>' +
                                        '<td class="data"><%= pretty_time %></td>' +
                                    '</tr>' +
                                    '<tr>' +
                                        '<td class="data-label">Image notes</td>' +
                                        '<td class="data"><%= initial_event.note %></td>' +
                                    '</tr>' +
                                    '<tr>' +
                                        '<td class="data-label">Tags</td>' +
                                        '<td class="data"><%= initial_event.attribute_names.join(", ") %></td>' +
                                    '</tr>' +
                                    '<tr>' +
                                        '<td class="data-label">Measures</td>' +
                                        '<td class="data"><%= initial_event.measurables.join(", ") %></td>' +
                                    '</tr>' +
                                '</tbody></table>' +
                            '</div>' +

                //         '</div>' +
                //     '</div>' +
                // '</div>' +
                '</div>' +
                '<div class="close">&times;</div>' +
            '</div>' +
        '</div>'
};
