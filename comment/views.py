from django.shortcuts import render, redirect, get_object_or_404
from comment.forms import CommentForm
from message.models import Message
from django.template.loader import render_to_string
from django.http import JsonResponse
from comment.models import Comment

from django.contrib import messages as messages_django

from webpage.utils import check_user, render_django_message


def save_comment_form(request, form=None, template=None):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():

            # for create comment
            if not form.instance.id:
                data['comment_create'] = 'create'
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

                messages_django.success(request, "Вітаю, Ви створили коментар!", extra_tags='success')

            # for update comment
            elif form.instance.id:
                comment = form.save()

                data['comment_update'] = 'update'

                messages_django.success(request, "Ви змінили коментар!", extra_tags='success')

            data['html_comments'] = render_to_string('partial_comment.html',
                                                     {"comment": comment},
                                                     request=request)
            data['form_is_valid'] = True

        else:
            data['form_is_valid'] = False

    context = {'form': form}

    render_django_message(request, data)

    if form:
        data['html_form'] = render_to_string(template, context, request=request)

    return JsonResponse(data)


def comment_create(request):
    if request.user.is_authenticated():
        if request.is_ajax() and request.method == 'POST':
            form = CommentForm(request.POST)
        else:
            form = CommentForm()
    else:
        messages_django.error(request, "Ви не авторизовані на сайті!", extra_tags='error')
        form = None

    return save_comment_form(request, form, 'partial_comment_form.html')


args_update_del = dict(model='comment', error_message="Цей коментар створений не Вами!", func_save=save_comment_form)


@check_user(**args_update_del)
def comment_update(request, comment=None, id=None):

    if request.is_ajax() and request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
    else:
        form = CommentForm(instance=comment)
    return save_comment_form(request, form, 'partial_comment_update.html')


@check_user(**args_update_del)
def comment_delete(request, comment=None, id=None):
    data = dict()

    if request.is_ajax() and request.method == "POST":
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
        messages_django.success(request, "Коментар видалено!", extra_tags='success')

    else:
        context = {'comment': comment}
        data['html_form'] = render_to_string('partial_comment_delete.html',
                                             context, request=request)
    render_django_message(request, data)
    return JsonResponse(data)
