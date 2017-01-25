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


var successCommentCreate = function(objectName, objectId, data){
    var commentsCount;
    var commentIdSelector = $("#comments-for-" + objectName + "-id-" + objectId);
    var caretCountAdd = commentIdSelector.siblings("div[data-id='" + objectId + "']");

    commentIdSelector.prepend(data.html_comments);
    commentIdSelector.show();
    commentIdSelector.parents().show();

    if (objectName == 'message') {
        caretCountAdd.next('div').find('p>em').first().text(data.message_comments_count);
        commentsCount = data.message_comments_count;
    } else {
        caretCountAdd.find('p>em').text(data.comment_comments_count);
        commentsCount = data.comment_comments_count;
    }

    if (commentsCount == '1' && caretCountAdd.find('p:first').find('span.caret').length == 0) {
        caretCountAdd.find('p:first').prepend("<span class='caret caret-toggle'></span>");}

    if (caretCountAdd.find(".caret-toggle").css("transform")) {
        caretCountAdd.find(".caret").toggleClass("caret-toggle");}

    addDjangoMessage(data, commentIdSelector.find("div:first"));
};

var successCommentDelete = function (data, commentId, messageId) {
    var commentIdSelector = $(".comment-" + commentId);
    var commentParentSelector;
    if (data.message_comments_count >= 0) {
        commentParentSelector = $(".message[data-id='" + messageId + "']" );
        if (data.message_comments_count == '0') {
            commentParentSelector.find("blockquote>p>span").remove();
        }
        commentParentSelector.next('div').find('p>em').first().text(data.message_comments_count);

    } else {
        commentParentSelector = $(".comment[data-id='" + data.comment_parent_id + "']" );
        commentParentSelector.find('p>em').first().text(data.comment_comments_count);
        if (data.comment_comments_count == 0) {
            commentParentSelector.find('p>span').remove();
        }
    }
    commentIdSelector.remove();
    addDjangoMessage(data, commentParentSelector);
};


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
            //beforeSend: function () {
            //    $("#modal-comment").modal("show");
            //},
            success: function (data) {
                console.log(data)
                if (data.html_messages_django) {
                    var messagesDjango;
                    if (commentId) {
                        messagesDjango = $(".comment-" + commentId);
                    } else {
                        messagesDjango = $("#partial-message-" + messageId);
                    }
                    console.log(data.html_messages_django);

                    addDjangoMessage(data, messagesDjango);

                } else {
                    $("#modal-comment").modal("show");
                    var modalContent = $(".modal-content");
                    modalContent.html(data.html_form);
                    modalContent.attr('data-comment-id', '');
                    modalContent.attr({'data-id': messageId, 'data-comment-id': commentId});
                }
            },
            error: error

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
                            successCommentCreate('message', messageId, data);
                        }
                        else {
                            successCommentCreate('comment', commentId, data);
                        }
                        console.log(data.comment_create);
                    }
                    else if (data.comment_update) {
                        var partialComment = $(".comment-" + commentId);

                        addDjangoMessage(data, partialComment);

                        partialComment.replaceWith(data.html_comments);
                        console.log(data.comment_update);
                    }
                    else {
                        successCommentDelete(data, commentId, messageId);
                    }
                    console.log(data.html_messages_django);
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




