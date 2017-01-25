from django.shortcuts import render
from message.forms import MessageForm
from message.models import Message
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from social.apps.django_app.default.models import UserSocialAuth

from django.contrib import messages as messages_django

from webpage.utils import check_user, render_django_message


def messages_page(request, data, model, count, context=None):
    list = model.objects.all().order_by('-date')
    paginator = Paginator(list, count)
    del_page = data.get('del_page', '')
    if del_page:
        page = del_page
    else:
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
    if request.is_ajax():
        data['html_messages'] = render_to_string('partial_messages_list.html',
                                                 {'messages': messages},
                                                 request=request)
        return data
    return context.update({'messages': messages})


def save_message_form(request, form=None, template_form=None):
    data = dict()

    if request.method == 'POST':
        if form.is_valid():
            if form.instance.id:
                message = form.save()
                data['html_message'] = render_to_string('partial_message.html',
                                                        {"message": message},
                                                        request=request)
                messages_django.success(request, "Вітаю, Ваше повідомлення оновлено!", extra_tags='success')
            else:
                message = form.save(commit=False)
                message.user = request.user
                message.save()

                form = MessageForm()
                messages_page(request, data, Message, 2)
                messages_django.success(request, "Вітаю, Ваше повідомлення створено!", extra_tags='success')

            data['form_is_valid'] = True

        else:
            data['form_is_valid'] = False

    render_django_message(request, data)

    if form:
        data['html_form'] = render_to_string(template_form,
                                             {'form': form},
                                             request=request)
    return JsonResponse(data)


def create_django_messages(request, data, content, message_level, tag):
    messages_django.add_message(request, message_level, content, extra_tags=tag)
    data['html_messages_django'] = render_to_string('messages_django.html',
                                                    {'message_for_django': messages_django.get_messages(request)},
                                                    request=request)
    return data


def enter_page(request):
    return render(request, 'base.html')


def messages_list(request):
    data = dict()

    user = request.user

    try:
        linkedin_login = user.social_auth.get(provider='linkedin-oauth2')
    except (UserSocialAuth.DoesNotExist, AttributeError):
        linkedin_login = None

    form = MessageForm()

    context = {
        'title': 'Повідомлення',
        'form': form,
        'linkedin_login': linkedin_login,
        }
    content = messages_page(request, data, Message, 2, context)
    if request.is_ajax():
        return JsonResponse(content)

    return render(request, 'messages.html', context)


def message_create(request):
    form = MessageForm()
    if request.user.is_authenticated():
        if request.is_ajax() and request.method == 'POST':
            form = MessageForm(request.POST)
    else:
        messages_django.error(request, "Ви не авторизовані на сайті!", extra_tags='error')

    return save_message_form(request, form, 'partial_message_form.html')


args_update_del = dict(model='message', error_message="Цей повідомлення створений не Вами!",
                       func_save=save_message_form)


@check_user(**args_update_del)
def message_update(request, message, id=None):

    if request.is_ajax() and request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
    else:
        form = MessageForm(instance=message)

    return save_message_form(request, form, 'partial_message_update.html')


@check_user(**args_update_del)
def message_delete(request, message, id=None):
    data = dict()

    if request.is_ajax() and request.method == 'POST':
        data['html_message_id'] = message.id
        message.delete()

        data['message_delete'] = True

        page = request.GET.get('page')
        data['del_page'] = page

        messages_page(request, data, Message, 2)
        messages_django.success(request, "Ваше повідомлення видалено!", extra_tags='success')
        render_django_message(request, data)

    else:
        context = {'message': message}
        data['html_form'] = render_to_string('partial_message_delete.html',
                                             context, request=request)

    return JsonResponse(data)
























