from django.shortcuts import render, redirect, get_object_or_404
from comment.forms import CommentForm
from message.models import Message
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from django.http import JsonResponse
from comment.models import Comment


def save_comment_form(request, data, form, template):
    if request.method == 'POST':
        if form.is_valid():
            if data.get('comment_create', ''):
                massage_id = request.POST.get('id')
                comment_id = request.POST.get('comment-id', '')

                message = get_object_or_404(Message, id=massage_id)

                message_comments_count = len(message.comments()) + 1

                comment = form.save(commit=False)
                comment.content_type = message.get_content_type()
                comment.object_id = message.id
                comment.user = request.user

                if comment_id:
                    instance = Comment.objects.get(id=int(comment_id))
                    comment.parent = instance
                    instance_comments_count = len(instance.children()) + 1

                    data['comment_comments_count'] = instance_comments_count

                comment.save()

                data['message_comments_count'] = message_comments_count

            elif data.get('comment_update', ''):
                comment = form.save()

            data['html_comments'] = render_to_string('partial_comment.html',
                                                     {"comment": comment},
                                                     request=request)
            data['form_is_valid'] = True

        else:
            data['form_is_valid'] = False

    context = {'form': form}

    data['html_form'] = render_to_string(template, context, request=request)

    return JsonResponse(data)


def comment_create(request):
    data = dict()

    data['comment_create'] = 'create'

    if request.is_ajax() and request.method == 'POST' and request.user.is_authenticated():
        form = CommentForm({'text': request.POST.get('text', ''),
                            'csrfmiddlewaretoken': request.POST.get('csrfmiddlewaretoken', '')})
    else:
        form = CommentForm()

    return save_comment_form(request, data, form, 'partial_comment_form.html')


def comment_update(request, id=None):
    data = dict()
    comment = get_object_or_404(Comment, id=id)

    data['comment_update'] = 'update'

    if request.is_ajax() and request.method == 'POST' and request.user == comment.user:
        form = CommentForm(request.POST, instance=comment)

    else:
        form = CommentForm(instance=comment)

    return save_comment_form(request, data, form, 'partial_comment_update.html')


def comment_delete(request, id=None):
    data = dict()
    comment = get_object_or_404(Comment, id=id)

    if request.is_ajax() and request.method == 'POST' and request.user == comment.user:
        massage_id = request.POST.get('id')

        if comment.has_parent_children():
            parent = comment.parent
            parent_comments_count = parent.children().count() - 1
            data['comment_comments_count'] = parent_comments_count
            data['comment_parent_id'] = parent.id

        else:
            message = get_object_or_404(Message, id=massage_id)
            message_comments_count = len(message.comments()) - 1
            data['message_comments_count'] = message_comments_count

        comment.delete()
        data['form_is_valid'] = True

    else:
        context = {'comment': comment}
        data['html_form'] = render_to_string('partial_comment_delete.html',
                                             context, request=request)
    return JsonResponse(data)


# def comment_create(request):
#     data = dict()
#
#     data['comment_create'] = 'create'
#
#     if request.is_ajax() and request.method == 'POST' and request.user.is_authenticated():
#         form = CommentForm({'text': request.POST.get('text', ''),
#                             'csrfmiddlewaretoken': request.POST.get('csrfmiddlewaretoken', '')})
#
#         if form.is_valid():
#             massage_id = request.POST.get('id')
#             comment_id = request.POST.get('comment-id', '')
#
#             message = get_object_or_404(Message, id=massage_id)
#
#             message_comments_count = len(message.comments()) + 1
#
#             comment = form.save(commit=False)
#             comment.content_type = message.get_content_type()
#             comment.object_id = message.id
#             comment.user = request.user
#
#             if comment_id:
#                 instance = Comment.objects.get(id=int(comment_id))
#                 comment.parent = instance
#                 instance_comments_count = len(instance.children()) + 1
#
#                 data['comment_comments_count'] = instance_comments_count
#
#             comment.save()
#
#             data['form_is_valid'] = True
#
#             data['message_comments_count'] = message_comments_count
#
#             data['html_comments'] = render_to_string('partial_comment.html',
#                                                      {'comment': comment},
#                                                      request=request)
#
#         else:
#             data['form_is_valid'] = False
#     else:
#         form = CommentForm()
#
#     context = {'form': form}
#
#     data['html_form'] = render_to_string('partial_comment_form.html',
#                                          context,
#                                          request=request)
#     return JsonResponse(data)
#
#
# def comment_update(request, id=None):
#     data = dict()
#     comment = get_object_or_404(Comment, id=id)
#
#     data['comment_update'] = 'update'
#
#     if request.is_ajax() and request.method == 'POST' and request.user == comment.user:
#         form = CommentForm(request.POST, instance=comment)
#
#         if form.is_valid():
#             comment = form.save()
#
#             data['html_comments'] = render_to_string('partial_comment.html',
#                                                      {"comment": comment},
#                                                      request=request)
#             data['form_is_valid'] = True
#
#         else:
#             data['form_is_valid'] = False
#
#     else:
#         form = CommentForm(instance=comment)
#
#     data['html_form'] = render_to_string('partial_comment_update.html',
#                                          {'form': form,
#                                          'comment': comment},
#                                          request=request)
#     return JsonResponse(data)
#
#
# def comment_delete(request, id=None):
#     data = dict()
#     comment = get_object_or_404(Comment, id=id)
#
#     if request.is_ajax() and request.method == 'POST' and request.user == comment.user:
#         massage_id = request.POST.get('id')
#
#         if comment.has_parent_children():
#             parent = comment.parent
#             parent_comments_count = parent.children().count() - 1
#             data['comment_comments_count'] = parent_comments_count
#             data['comment_parent_id'] = parent.id
#
#         else:
#             message = get_object_or_404(Message, id=massage_id)
#             message_comments_count = len(message.comments()) - 1
#             data['message_comments_count'] = message_comments_count
#
#         comment.delete()
#         data['form_is_valid'] = True
#
#     else:
#         context = {'comment': comment}
#         data['html_form'] = render_to_string('partial_comment_delete.html',
#                                              context, request=request)
#     return JsonResponse(data)
