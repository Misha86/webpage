from django.shortcuts import render, redirect, get_object_or_404
from comment.forms import CommentForm
from message.models import Message
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from django.http import JsonResponse
from comment.models import Comment


def comment_create(request):
    data = dict()

    if request.is_ajax() and request.method == 'POST' and request.user.is_authenticated():
        form = CommentForm({'text': request.POST.get('text', ''),
                            'csrfmiddlewaretoken': request.POST.get('csrfmiddlewaretoken', '')})

        if form.is_valid():
            massage_id = request.POST.get('id')
            comment_id = request.POST.get('comment-id', '')

            message = get_object_or_404(Message, id=massage_id)

            comment = form.save(commit=False)
            comment.content_type = message.get_content_type()
            comment.object_id = message.id
            comment.user = request.user

            if comment_id:
                instance = Comment.objects.get(id=int(comment_id))
                comment.parent = instance
            comment.save()

            data['form_is_valid'] = True

            data['html_comments'] = render_to_string('partial_comments_list.html',
                                                     {'message': message},
                                                     request=request)

        else:
            data['form_is_valid'] = False
    else:
        form = CommentForm()

    context = {'form': form}

    data['html_form'] = render_to_string('partial_comment_form.html',
                                         context,
                                         request=request)
    return JsonResponse(data)

