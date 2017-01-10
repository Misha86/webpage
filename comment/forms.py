from __future__ import unicode_literals

from django import forms
from comment.models import Comment
from django.utils.translation import ugettext_lazy as _


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text', ]

        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4,
                                          'placeholder': _("введіть текст коментаря")}),
            }
        labels = {'text': ''}