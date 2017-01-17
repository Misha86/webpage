from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from message.forms import MessageForm
from message.models import Message
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from social.apps.django_app.default.models import UserSocialAuth


def enter_page(request):
    return render(request, 'base.html')


def messages_list(request):
    user = request.user

    try:
        linkedin_login = user.social_auth.get(provider='linkedin-oauth2')
    except (UserSocialAuth.DoesNotExist, AttributeError):
        linkedin_login = None

    form = MessageForm()
    messages_list = Message.objects.all().order_by('-date')
    data = dict()
    paginator = Paginator(messages_list, 2)
    page = request.GET.get('page')
    try:
        messages = paginator.page(page)
        # print(articles.page_range)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        messages = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        messages = paginator.page(paginator.num_pages)

    context = {
        'title': 'Повідомлення',
        'form': form,
        'messages': messages,
        'paginator': paginator,
        'linkedin_login': linkedin_login,
        }

    if request.is_ajax():
        data['html_messages'] = render_to_string('partial_messages_list.html',
                                                 {'messages': messages},
                                                 request=request)

        data['html_page'] = render_to_string('partial_massage_pages.html',
                                             {'messages': messages,
                                              'paginator': paginator},
                                             request=request)
        return JsonResponse(data)

    return render(request, 'messages.html', context)


def message_create(request):
    data = dict()
    form = MessageForm()

    if request.is_ajax() and request.method == 'POST' and request.user.is_authenticated():
        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.save()

            form = MessageForm()
            messages = Message.objects.all().order_by('-date')
            data['html_messages'] = render_to_string('partial_messages_list.html',
                                                     {"messages": messages},
                                                     request=request)
            data['form_is_valid'] = True

        else:
            data['form_is_valid'] = False

    data['html_form'] = render_to_string('partial_message_form.html',
                                         {'form': form},
                                         request=request)
    return JsonResponse(data)


def message_update(request, id=None):
    data = dict()
    message = get_object_or_404(Message, id=id)

    if request.is_ajax() and request.method == 'POST' and request.user == message.user:
        form = MessageForm(request.POST, instance=message)

        if form.is_valid():
            message = form.save()

            data['html_message'] = render_to_string('partial_message.html',
                                                    {"message": message},
                                                    request=request)
            data['form_is_valid'] = True

        else:
            data['form_is_valid'] = False

    else:
        form = MessageForm(instance=message)

    data['html_form'] = render_to_string('partial_message_update.html',
                                         {'form': form},
                                         request=request)
    return JsonResponse(data)


def message_delete(request, id=None):
    message = get_object_or_404(Message, id=id)
    data = dict()
    if request.is_ajax() and request.method == 'POST' and request.user == message.user:
        data['html_message_id'] = message.id
        message.delete()
        data['form_is_valid'] = True

    else:
        context = {'message': message}
        data['html_form'] = render_to_string('partial_message_delete.html',
                                             context, request=request)
    return JsonResponse(data)


# from social.apps.django_app.default.models import UserSocialAuth
# def test(request):
#     user = request.user
#     social_user = user.social_auth.get(provider='linkedin-oauth2')
#     return render(request, "test.html", {'content': social_user})






















