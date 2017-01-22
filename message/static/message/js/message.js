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
};

var errorMessage = function(xhr, errmsg, err) {
    $('#result').html("<div class='container' data-alert><h1>Oops! We have encountered an error: " + xhr.status + errmsg +
    "</h1><a href='#' class='close'>&times;</a></div>"); // add the error to the dom
    alert("Oops! We have encountered an error: " + err + " " + xhr.status + " " + errmsg )
    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
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

            error : errorMessage
        });

    });

    var selectorBody = $("body");

    var loadForm = function (event) {
        event.preventDefault();
        var btn = $(event.target);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-comment").modal("show");
            },
            success: function (data) {
                $(".modal-content").html(data.html_form)
            },
            error : errorMessage
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
                if (data.form_is_valid) {
                    $("#modal-comment").modal("hide");
                    if (data.comment_delete) {
                        $("#message-list").html(data.html_messages);
                    } else {
                        $('#partial-message-' + id).replaceWith(data.html_message);
                    }
                } else {
                    $(".modal-content").html(data.html_form);
                }
            },

            error : errorMessage
        });
    };

    selectorBody.on('click', '.js-update-message', loadForm);
    selectorBody.on('submit', '.js-message-form', saveForm);

    selectorBody.on('click', '.js-delete-message', loadForm);
    selectorBody.on('submit', '.js-message-delete-form', saveForm);
});
