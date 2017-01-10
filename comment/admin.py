from django.contrib import admin
from comment.models import Comment


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    fieldsets = [
        (None, {'fields': ['text', 'user', 'parent', 'content_type', 'object_id']})
    ]
    list_display = ['id', 'user', 'date', 'content_object',  'parent']


admin.site.register(Comment, CommentAdmin)
