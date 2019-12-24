from urllib.parse import urlparse

from django.db import models
from django.utils import timezone


class TeaserClick (models.Model):
    link = models.URLField(verbose_name='Ссылка')
    banner = models.CharField(max_length=100, verbose_name='Баннер')
    ip = models.GenericIPAddressField(verbose_name='IP')
    useragent = models.CharField(max_length=250, verbose_name='User agent')
    timestamp = models.DateTimeField(default=timezone.now, verbose_name='Время')
    referer = models.CharField(max_length=500, verbose_name='Реферер')
    cookie_counter = models.IntegerField(verbose_name='Переходов по куки')
    geo = models.CharField(max_length=100, default='Нет информации', verbose_name='ГЕО')
    age = models.CharField(max_length=100, default='Нет информации', verbose_name='Возраст')
    gender = models.CharField(max_length=100, default='Нет информации ', verbose_name='Пол')
    search = models.CharField(max_length=1000, default='Нет информации ', verbose_name='Поисковая фраза')

    class Meta:
        ordering = ('-timestamp',)
        verbose_name = 'Тизерный клик'
        verbose_name_plural = 'Тизерные клики'

    def __str__(self):
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S") + ' ' + urlparse(self.referer)[1]


class TeaserLead (models.Model):
    timestamp = models.DateTimeField(default=timezone.now, verbose_name='Время')
    offer = models.CharField(max_length=100, verbose_name='Оффер')
    banner = models.CharField(max_length=1000, verbose_name='Идентификатор')
    ip = models.GenericIPAddressField(verbose_name='IP')

    class Meta:
        ordering = ('-timestamp',)
        verbose_name = 'Тизерный лид'
        verbose_name_plural = 'Тизерные лиды'

    def __str__(self):
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S") + ' ' + self.offer
