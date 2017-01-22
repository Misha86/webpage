from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class CommentManager(models.Manager):
    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id, parent=None)
        return qs


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="comments", verbose_name=_("Автор коментаря"),
                             on_delete=models.CASCADE, default=1)
    # slug = models.SlugField(verbose_name=_("Ім`я коментаря транслітом"), blank='', unique=)
    text = models.TextField(verbose_name=_('Текст коментаря'), max_length=500)
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата створення"))
    update = models.DateTimeField(auto_now=True, verbose_name=_("Дата оновлення"))

    parent = models.ForeignKey('self', null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = CommentManager()

    class Meta:
        ordering = ['-date', ]
        db_table = "comments"
        verbose_name = _("Коментар")
        verbose_name_plural = _("Коментарі")

    def __str__(self):
        return str(self.id)

    def children(self):
        instance = self
        return Comment.objects.filter(parent=instance)

    def has_parent_children(self):
        instance = self
        return hasattr(instance.parent, 'children')