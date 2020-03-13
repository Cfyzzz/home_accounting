from django.utils import timezone
from django.db import models


class CashItem(models.Model):
    name = models.CharField(default="", unique=True, verbose_name=u"Название статьи", max_length=40)
    min_value = models.IntegerField(default=0, verbose_name="Минимальный порог")
    value = models.IntegerField(default=0, verbose_name=u"Значение")
    plan_value = models.IntegerField(default=0, verbose_name=u"Плановое значение")
    date = models.DateField(default=timezone.now, verbose_name="Период")
    virtual_value = models.IntegerField(default=0, verbose_name=u"Плановый приход")

    def __unicode__(self):
        return self.name

    class Mets:
        verbose_name = u"статья"
        verbose_name_plural = u"статьи"
