// Acquiring the token is straightforward using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


$(function () {
    $('#create-message').on('submit', '#form-massage', function(event){
        event.preventDefault();
        var form = $(this);
        //console.log(form)
        $.ajax({
            url: form.attr("action"),
            type: form.attr("method"),
            data: form.serialize(),
            dataType: 'json',

            success: successForCreate,

            error : error
        });

    });

    var messageList = $("#message-list")

    messageList.on('click', '.js-update-message', function (event) {
        event.preventDefault();
        var btn = $(event.target);
        //console.log(btn);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-comment").modal("show");
            },

            success: function (data) {
                console.log(data);
                $(".modal-content").html(data.html_form)
            },
            error : error
        });
    });

    messageList.on('submit', '.js-message-form', function (event) {
        event.preventDefault();
        var form = $(event.target);
        console.log(form.attr("action"));
        $.ajax({
            url: form.attr("action"),
            type: form.attr("method"),
            data: form.serialize(),
            dataType: 'json',

            success: function (data) {
                var id =form.attr('data-message-id');
                console.log(id);
                if (data.form_is_valid) {
                    $("#modal-comment").modal("hide");
                    //$(`#partial-message-${id}`).html(data.html_message);
                    $('#partial-message-' + id).html(data.html_message);
                } else {
                    $(".modal-content").html(data.html_form);
                }
            },

            error : error
        });
    });

    messageList.on('click', '.js-delete-message', function (event) {
        event.preventDefault();
        var btn = $(event.target);
        console.log(btn);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-comment").modal("show");
            },

            success: function (data) {
                console.log(data);
                $(".modal-content").html(data.html_form)
            },
            error : error
        });
    });

    messageList.on('submit', '.js-message-delete-form', function (event) {
        event.preventDefault();
        var form = $(event.target);
        console.log(form.attr("action"));
        $.ajax({
            url: form.attr("action"),
            type: form.attr("method"),
            data: form.serialize(),
            dataType: 'json',

            success: function (data) {
                console.log("message.id: ", data.html_message_id);
                if (data.form_is_valid) {
                    $("#partial-message-" + data.html_message_id).html('');
                    $("#modal-comment").modal("hide");
                }
            },

            error : error
        });
    });

    var successForCreate = function (data) {
        $("#form-massage").html(data.html_form)
        if (data.form_is_valid) {
            $("#message-list").html(data.html_messages)
        }
    };

    var error = function(xhr, errmsg, err) {
        $('#result').html("<div class='container' data-alert><h1>Oops! We have encountered an error: " + xhr.status + errmsg +
        "</h1><a href='#' class='close'>&times;</a></div>"); // add the error to the dom
        alert("Oops! We have encountered an error: " + err + " " + xhr.status + " " + errmsg )
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    };
});