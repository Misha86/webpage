var fadeToggleComments = function (event){
    var targetData = event.currentTarget.getAttribute('data-id');
    var commentsSelector;
    if (event.currentTarget.getAttribute('class').split(' ')[0] == 'message'){
        commentsSelector = "#comments-for-message-id-";
    } else {
        commentsSelector = "#comments-for-comment-id-";
    }
    var comments = $(commentsSelector + targetData);
    var caret = $(this);
    caret.find('.caret').toggleClass("caret-toggle");
    comments.fadeToggle();
};

var selectorBody = $('body');

selectorBody.on('click', '.message', fadeToggleComments);
selectorBody.on('click', '.comment', fadeToggleComments);

var successCommentCreate = function(objectName, objectId, dataComment, dataCount){
    var commentIdSelector = $("#comments-for-" + objectName + "-id-" + objectId);
    var caretCountAdd = commentIdSelector.siblings("div[data-id='" + objectId + "']");

    commentIdSelector.prepend(dataComment);
    commentIdSelector.show();
    commentIdSelector.parents().show();

    if (objectName == 'message') {
        caretCountAdd.next('div').find('p>em').first().text(dataCount);
    } else {
        caretCountAdd.find('p>em').text(dataCount);}

    if (dataCount == '1' && caretCountAdd.find('p:first').find('span.caret').length == 0) {
        caretCountAdd.find('p:first').prepend("<span class='caret caret-toggle'></span>");}

    if (caretCountAdd.find(".caret-toggle").css("transform")) {
        caretCountAdd.find(".caret").toggleClass("caret-toggle");}
};

var successCommentDelete = function (data, commentId, messageId) {
    var commentIdSelector = $(".comment-" + commentId);
    if (data.message_comments_count >= 0) {
        var commentMessage = $(".message[data-id='" + messageId + "']" );
        if (data.message_comments_count == '0') {
            commentMessage.find("blockquote>p>span").remove();
        }
        commentMessage.next('div').find('p>em').first().text(data.message_comments_count);

    } else {
        var commentParent = $(".comment[data-id='" + data.comment_parent_id + "']" );
        commentParent.find('p>em').first().text(data.comment_comments_count);
        if (data.comment_comments_count == 0) {
            commentParent.find('p>span').remove();
        }
    }
    commentIdSelector.remove();
};


var error = function (xhr, errmsg, err) {
    alert("Oops! We have encountered an error: " + err + " " + xhr.status + " " + errmsg)
    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
}


$(function () {
    var selectorBody = $("body");

    var loadForm = function (event) {
        event.preventDefault();
        var messageId = $(event.target).attr("data-id");
        var commentId = $(event.target).attr("data-comment-id");
        var url = $(event.target).attr("data-form");
        console.log("url: ", url);
        console.log('messageId: ', messageId);
        console.log('commentId: ', commentId);
        $.ajax({
            url: url,
            data: {
                id: messageId
            },
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-comment").modal("show");
            },
            success: function (data) {
                var modalContent = $(".modal-content");
                $("#modal-comment .modal-content").html(data.html_form);
                modalContent.attr('data-comment-id', '');
                modalContent.attr({'data-id': messageId, 'data-comment-id': commentId});
            }

        })
    };

    var saveForm = function (event) {
        event.preventDefault();
        var form = $(this);
        var dataId = $(".modal-content")
        var messageId = dataId.attr('data-id');
        var commentId = dataId.attr('data-comment-id');
        console.log('messageId: ', messageId);
        console.log('commentId: ', commentId);
        $.ajax({
            url: form.attr("action"),
            type: form.attr("method"),
            data: form.serialize() + "&id=" + messageId + "&comment-id=" + commentId,
            dataType: 'json',
            success: function(data){
                if (data.form_is_valid) {
                    $("#modal-comment").modal("hide");
                    $("div[data-id='" + commentId + "']").find(".caret").toggleClass("caret-toggle");
                    if (data.comment_create) {
                        if (commentId == false) {
                            successCommentCreate('message', messageId, data.html_comments, data.message_comments_count);
                        }
                        else {
                            successCommentCreate('comment', commentId, data.html_comments, data.comment_comments_count);
                        }
                        console.log(data.comment_create);
                    }
                    else if (data.comment_update) {
                        $(".comment-" + commentId).replaceWith(data.html_comments);
                        console.log(data.comment_update);
                    }
                    else {
                        successCommentDelete(data, commentId, messageId);
                    }
                }
                else {
                    $("#modal-comment .modal-content").html(data.html_form)
                }
            },
            error: error
        })
    };

    selectorBody.on('click', '.js-create-comment', loadForm);
    selectorBody.on("submit", ".js-comment-form", saveForm);

    selectorBody.on('click', '.js-update-comment', loadForm);

    selectorBody.on('click', '.js-delete-comment', loadForm);
    selectorBody.on("submit", ".js-comment-delete-form", saveForm);
});




