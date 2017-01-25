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



var successMessageCreate = function (data) {
    $("#form-massage").html(data.html_form)
    if (data.form_is_valid) {
        $("#message-list").html(data.html_messages)
    }
    if (data.html_messages_django) {
        var messagesDjango = $("#messages_django");
        messagesDjango.html(data.html_messages_django);
        messagesDjango.find("div[class^='has-']").fadeOut(3500)
    }
};

var error = function(xhr, errmsg, err) {
    $('#result').html("<div class='container' data-alert><h1>Oops! We have encountered an error: " + xhr.status + errmsg +
    "</h1><a href='#' class='close'>&times;</a></div>"); // add the error to the dom
    alert("Oops! We have encountered an error: " + err + " " + xhr.status + " " + errmsg )
    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
};


var addDjangoMessage = function(data, selector){
    var attr = selector.prev().attr('class');

    if (attr == "has-error" || attr =="has-success") {
        selector.prev().replaceWith(data.html_messages_django);
    } else {
        selector.before(data.html_messages_django);
    } selector.prev().fadeOut(3500);

};


// ajax pagination
$("#message-list").on('click', ".pagination li a", function(event){
    event.preventDefault();
    var page = $(this);
    $.ajax({
        async: true,
        url:  "/list/" + page.attr("href"),
        type: 'get',
        dataType: 'json',

        success: function (data) {
            console.log(page.text())
            $("#message-list").html(data.html_messages);
        },

        error: error
    });
});


$(function () {
    $('#create-message').on('submit', '#form-massage', function(event){
        event.preventDefault();
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            type: form.attr("method"),
            data: form.serialize(),
            dataType: 'json',

            success: successMessageCreate,

            error : error
        });

    });

    var selectorBody = $("body");

    var loadForm = function (event) {
        event.preventDefault();
        var btn = $(event.target);
        var id = btn.attr("data-id");
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            //beforeSend: function () {
            //    $("#modal-comment").modal("show");
            //},
            success: function (data) {
                if (data.html_messages_django) {
                    var messagesDjango = $("#partial-message-" + id);

                    addDjangoMessage(data, messagesDjango)

                } else {
                    $("#modal-comment").modal("show");
                    $(".modal-content").html(data.html_form)
                }
            },
            error : error
        });
    };

    var saveForm = function (event) {
        event.preventDefault();
        var form = $(event.target);
        var activePage = $("ul>li.active>a").text();
        $.ajax({
            url: form.attr("action")+'?page='+ activePage,
            type: form.attr("method"),
            data: form.serialize(),
            dataType: 'json',

            success: function (data) {
                var id =form.attr('data-message-id');
                if (data.form_is_valid || data.message_delete) {
                    $("#modal-comment").modal("hide");
                    // chandge message into site
                    if (data.message_delete) {
                        // for delete message
                        $("#message-list").html(data.html_messages);
                    } else {
                        // for update message
                        $('#partial-message-' + id).replaceWith(data.html_message);
                    }

                    // add message from django
                    if (data.html_messages_django) {
                        var messagesDjango;
                        if (data.message_delete ){
                            // selector for django message after delete message
                            messagesDjango = $(".navbar>div.container>div>h3");
                        } else {
                            // dselector for django message when success update message or error
                            messagesDjango = $("#partial-message-" + id);
                        }

                        addDjangoMessage(data, messagesDjango)
                    }

                } else {
                    // show form when method GET or form is invalid
                    $(".modal-content").html(data.html_form);
                }
            },

            error : error
        });
    };

    selectorBody.on('click', '.js-update-message', loadForm);
    selectorBody.on('submit', '.js-message-form', saveForm);

    selectorBody.on('click', '.js-delete-message', loadForm);
    selectorBody.on('submit', '.js-message-delete-form', saveForm);
});
