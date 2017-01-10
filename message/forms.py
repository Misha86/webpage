from __future__ import unicode_literals

from django import forms
from message.models import Message
from django.utils.translation import ugettext_lazy as _


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ['text', ]

        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4,
                                          'placeholder': _("введіть текст повідомлення")}),
            }
        labels = {'text': ''}