from __future__ import unicode_literals

from django.conf.urls import url
from comment.views import (comment_create,
                           comment_update,
                           comment_delete)

app_name = 'comment'

urlpatterns = [
    url(r'^create/$', comment_create, name='create'),
    url(r'^(?P<id>\d+)/update/$', comment_update, name='update'),
    url(r'^(?P<id>\d+)/delete/$', comment_delete, name='delete'),
]
