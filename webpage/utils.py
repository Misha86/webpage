from __future__ import unicode_literals
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages as messages_django
from functools import wraps
from django.template.loader import render_to_string


def check_user(model, error_message, func_save):
    def wrapper(func):
        @wraps(func)
        def inner(request, id=None, *args, **kwargs):
            class_model = ContentType.objects.get(model=model)
            instance = get_object_or_404(class_model.model_class(), id=id)
            if request.user == instance.user:
                return func(request, instance, id=None)
            else:
                messages_django.error(request, error_message, extra_tags='error')
                return func_save(request)
        return inner
    return wrapper


def render_django_message(request, data):
    message_for_django = messages_django.get_messages(request)
    if message_for_django:
        data['html_messages_django'] = render_to_string('messages_django.html',
                                                        {'message_for_django': message_for_django},
                                                        request=request)
    return data