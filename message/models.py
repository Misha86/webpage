from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment


class Message(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="messages", verbose_name=_("Автор повідомлення"),
                             on_delete=models.CASCADE)
    text = models.TextField(verbose_name=_('Текст повідомлення'), max_length=500)
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата створення"))
    update = models.DateTimeField(auto_now=True, verbose_name=_("Дата оновлення"))
    # slug = models.SlugField(verbose_name=_("Ім`я повідомлення транслітом"), blank='', unique='')
    comments = GenericRelation(Comment)

    class Meta:
        db_table = "messages"
        verbose_name = _("Повідомлення")
        verbose_name_plural = _("Повідомлення")

    def __str__(self):
        return 'Клас: {}, id: {}'.format(self.__class__.__name__, self.id)

    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    def comments(self):
        qs = Comment.objects.filter_by_instance(self)
        return qs
