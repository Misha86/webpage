from __future__ import unicode_literals

from django.conf.urls import url
from comment.views import (comment_create,
                           )

app_name = 'comment'

urlpatterns = [
    url(r'^create/$', comment_create, name='create'),
    # url(r'^create/$', comment_create, name='create'),
    # url(r'^list/$', messages_list, name='list'),
    # url(r'^create/$', message_create, name='create'),
    ]
