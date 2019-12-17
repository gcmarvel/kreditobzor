from urllib.parse import urlparse

from django.db import models
from django.utils import timezone


class TeaserClick (models.Model):
    link = models.URLField(verbose_name='Сссылка')
    banner = models.CharField(max_length=100, verbose_name='Баннер')
    ip = models.GenericIPAddressField(verbose_name='IP')
    useragent = models.CharField(max_length=250, verbose_name='User agent')
    timestamp = models.DateTimeField(default=timezone.now, verbose_name='Время')
    referer = models.CharField(max_length=500, verbose_name='Реферер')
    cookie_counter = models.IntegerField(verbose_name='Переходов по куки')

    class Meta:
        ordering = ('-timestamp',)
        verbose_name = 'Тизерный клик'
        verbose_name_plural = 'Тизерные клики'

    def __str__(self):
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S") + ' ' + urlparse(self.referer)[1]
