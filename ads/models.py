from django.db import models

from manager.utils import get_choices


class SidebarBanner(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    image = models.ImageField(verbose_name='Изображение')
    link = models.URLField(verbose_name='Ссылка')
    reference_app = models.CharField(max_length=50, choices=get_choices(), verbose_name='Приложение', blank=True)
    enabled = models.BooleanField(verbose_name='Активный', default=True)
    clicked = models.IntegerField(verbose_name='Переходов', default=0)

    class Meta:
        verbose_name = 'Боковой баннер'
        verbose_name_plural = 'Боковые баннеры'

    def __str__(self):
        return self.title
