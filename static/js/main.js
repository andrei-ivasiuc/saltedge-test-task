$(document).ready(function(){
    window.is_mobile = false;
    window.is_mobile_prev = false;
    window.setInterval(update_events_list, 1000);

    /**
     * Save data about event into DB
     * @param action
     * @param body
     */
    function register_event(action, body){
        $.ajax({
            url: '/api/events',
            type: 'post',
            data: {action: action, body: body}
        });
    }

    /**
     * Update list of events once a second
     * For production would have used smth like socket.io
     */
    function update_events_list(){
        $.ajax({
            url: '/api/events',
            type: 'get',
            dataType: 'json',
            success: function(res){
                render_events(res);
            }
        });

        $.ajax({
            url: '/api/events/stats',
            type: 'get',
            dataType: 'json',
            success: function(res){
                render_stats(res);
            }
        });
    }

    /**
     * Renders server response for events to DOM
     * @param events
     */
    function render_events(events){
        var event_element = $("<li>");
        var events_list = $('.events');
        var event_action_element = $("<strong>");
        var event_date_element = $("<span>");
        events_list.empty();
        $.each(events, function(i, event){
            var element = event_element.clone();
            var date_element = event_date_element.clone();
            var action_element = event_action_element.clone();
            element.text(event['body']);
            date_element.text(event.created);
            action_element.text(event.action);
            element.prepend(action_element);
            element.append(date_element);
            events_list.append(element);
        });
    }

    /**
     * Renders server response for stats to DOM
     * @param stats
     */
    function render_stats(stats) {
        for(var action in stats){
            $('[data-action-stats="'+action+'"]').text(stats[action]);
        }
    }

    $('.feature').on('mouseenter', function(e){
        var target = $(this).attr('data-target');
        $('.slider').attr('data-slide', target);
        $('.slide').removeClass('active');
        $('#'+target).addClass('active');
        register_event('change', $(this).attr('data-action-body'));
    });

    $(window).on('resize', function (e) {
        var screen_width = $(this).width();
        var event_body = "";
        if(screen_width < 1024){
            window.is_mobile = true;
            event_body = "Viewport changed to mobile";
        }else{
            window.is_mobile = false;
            event_body = "Viewport changed to desktop";
        }
        if(window.is_mobile_prev !== window.is_mobile){
            register_event('resize', event_body);
        }
        window.is_mobile_prev = window.is_mobile;
    });

    $('.mobile-menu-trigger').on('click', function (e) {
        var parent = $(this).closest('.main-menu');
        parent.toggleClass('active');
    });
});