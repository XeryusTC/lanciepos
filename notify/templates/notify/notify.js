$(document).ready(function() {
    $.ajaxSetup({traditional: true });
    
    update(true);
    window.setInterval(update, 10000);
});

var date_names = new Array("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday");

function add_notification(text, date) {
    if (typeof add_notification.row_counter == 'undefined') {
        add_notification.row_counter = 1;
    }
    
    $("body").prepend("<div class=\"row" + add_notification.row_counter + "\"> \
        <div class=\"title\">" + date + "</div>" + text + "</div>");
    
    add_notification.row_counter = (add_notification.row_counter % 2) + 1;
}

function update(suppress) {
    if (typeof update.last_id == 'undefined') {
        update.last_id = 0;
    }
    if (typeof suppress == 'undefined') {
        suppress = false;
    }

    $.getJSON('{% url 'notify:update' %}', {'id': update.last_id}, function(data) {
        data.reverse()
        $.each(data, function(key, value) {
            pub_date = new Date(value.fields.pub_date);
            minutes = pub_date.getMinutes();
            if (minutes < 10) {
                minutes = "0" + minutes;
            }
            
            // Display
            time = date_names[pub_date.getDay()] + " " + pub_date.getHours() + ":" + minutes;
            add_notification(value.fields.content, time);

            update.last_id = value.pk;
        });
        if (data.length > 0 && !suppress) {
            $("#sound").get(0).play();
        }
    });
}
