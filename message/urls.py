from __future__ import unicode_literals

from django.conf.urls import url
from message.views import (enter_page,
                           messages_list,
                           message_create,
                           message_update,
                           message_delete)

app_name = 'message'

urlpatterns = [
    url(r'^$', enter_page, name='enter'),
    url(r'^list/$', messages_list, name='list'),
    url(r'^create/$', message_create, name='create'),
    url(r'^update/(?P<id>\d+)/$', message_update, name='update'),
    url(r'^delete/(?P<id>\d+)/$', message_delete, name='delete'),
    ]
