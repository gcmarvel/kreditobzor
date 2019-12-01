from django.shortcuts import reverse
from django.db import models

from manager.utils import get_choices


class Article(models.Model):
    title = models.CharField(max_length=2000, verbose_name='Заголовок')
    image = models.ImageField(verbose_name='Изображение')
    text = models.TextField(verbose_name='Текст')
    reference_app = models.CharField(max_length=50, choices=get_choices(), verbose_name='Приложение')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:article_detail', args=[str(self.pk)])


class News(models.Model):
    title = models.CharField(max_length=2000, verbose_name='Заголовок')
    image = models.ImageField(verbose_name='Изображение')
    text = models.TextField(verbose_name='Текст')
    reference_app = models.CharField(max_length=50, choices=get_choices(), verbose_name='Приложение')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:news_detail', args=[str(self.pk)])


class Paragraph(models.Model):
    image = models.ImageField(verbose_name='Изображение')
    text = models.TextField(verbose_name='Текст')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')

    class Meta:
        verbose_name = 'Параграф'
        verbose_name_plural = 'Параграфы'
