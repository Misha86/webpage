$(function () {
    function fade(caret, comments){
        caret.find('.caret').toggleClass("caret-toggle");
        comments.fadeToggle();
    }

    $('body').on('click', '.message', function(event){
        var targetData = event.currentTarget.getAttribute('data-id');
        var comments = $("#comments-for-message-id-" + targetData);
        var caret = $(this);
        fade(caret, comments);
        console.log(targetData);
    });

    $('body').on('click', '.comment', function(event){
        var targetData = event.currentTarget.getAttribute('data-id');
        var comments = $("#comments-for-comment-id-" + targetData);
        var caret = $(this);
        fade(caret, comments)
        console.log(targetData);
    });

    $("#message-list").on('click', '.js-create-comment', function (event) {
        event.preventDefault();
        var messageId = $(event.target).attr("data-id");
        var commentId = $(event.target).attr("data-comment-id");
        var url = $(event.target).attr("data-form");
        console.log("url: ", url);
        console.log('messageId: ', messageId);
        console.log('commentId: ', commentId)
        $.ajax({
            url: url,
            data: {
                id : messageId
            },
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-comment").modal("show");
            },
            success: function (data) {
                $("#modal-comment .modal-content").html(data.html_form);
                $(".modal-content").attr('data-comment-id', '');
                $(".modal-content").attr({'data-id': messageId, 'data-comment-id': commentId});
            }
        });
    });

    $("#message-list").on("submit", ".js-book-comment-form", function (event) {
        event.preventDefault();
        var form = $(this);
        var dataId = $(".modal-content")
        var messageId = dataId.attr('data-id');
        var commentId = dataId.attr('data-comment-id');
        console.log(messageId)
        console.log('comment: ', commentId)
        $.ajax({
            url: form.attr("action"),
            type: form.attr("method"),
            data: form.serialize() + "&id=" + messageId + "&comment-id=" + commentId,
            dataType: 'json',
            success: function (data) {
                //console.log(data)
                if (data.form_is_valid) {
                    $("#modal-comment").modal("hide");
                    $("#comments-for-message-id-"+ messageId).html(data.html_comments);
                    $("#comments-for-comment-id-"+ commentId).show()
                    $("div[data-id='" + commentId + "']").find(".caret").toggleClass("caret-toggle");
                    if (commentId == false) {
                        $("#comments-for-message-id-"+ messageId).show();
                        var caretChange = $("div[data-id='" + messageId + "']");
                        var commentCount = caretChange.next().first().find("p>em").first();
                        if (caretChange.find("blockquote span").length == 0) {
                            caretChange.find("blockquote").prepend("<span class='caret caret-toggle'></span>");
                            commentCount.text("1");
                        } else {
                            var newText = parseInt(commentCount.text()) + 1;
                            commentCount.text(newText);
                            console.log(caretChange.next().first().find("p>em").first().text());
                        }
                        if (caretChange.find(".caret-toggle").css("transform")) {
                            caretChange.find(".caret").toggleClass("caret-toggle");
                        }
                    }
                } else {
                    $("#modal-comment .modal-content").html(data.html_form);
                }
            }
        });
    });
});