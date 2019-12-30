from django.shortcuts import reverse
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Offer(models.Model):
    active = models.BooleanField(default=True)
    slug = models.SlugField(allow_unicode=True, unique=True, verbose_name='URL')
    title = models.CharField(max_length=100, verbose_name='Название')
    image = models.ImageField(verbose_name='Логотип')
    description = models.TextField(max_length=4000, verbose_name='Описание')
    default_position = models.IntegerField(verbose_name='Дефолтная позиция')
    link = models.URLField(verbose_name='Ссылка')
    limit = models.IntegerField(verbose_name='Кредитный лимит')
    maintenance = models.IntegerField(verbose_name='Обслуживание')
    min_rate = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Ставка')
    special_offer = models.BooleanField(verbose_name='Специальное предложение')
    cashback = models.IntegerField(verbose_name='Кэшбэк', default=0)
    high_approval_rate = models.BooleanField(verbose_name='Высокий % одобрения')
    issue_cost = models.CharField(max_length=20, verbose_name='Открытие')
    courier = models.BooleanField(verbose_name='Доставка курьером')
    documents = models.CharField(max_length=50, verbose_name='Документы')
    history_rating = models.IntegerField(verbose_name='Кредитный рейтинг')
    advantage1 = models.CharField(max_length=200, blank=True, null=True, verbose_name='Преимущество 1')
    advantage2 = models.CharField(max_length=200, blank=True, null=True, verbose_name='Преимущество 2')
    advantage3 = models.CharField(max_length=200, blank=True, null=True, verbose_name='Преимущество 3')
    advantage4 = models.CharField(max_length=200, blank=True, null=True, verbose_name='Преимущество 4')
    legal_info = models.TextField(max_length=2000, verbose_name='Юридическая информация')
    promoted = models.BooleanField(verbose_name='Продвигаемое')
    rating = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='rating', default=0)
    count = models.IntegerField(verbose_name='Количество отзывов', default=0)
    clicked = models.IntegerField(verbose_name='Переходов', default=0)
    addition = models.TextField(max_length=4000, verbose_name='Дополнительный текст', blank=True, null=True)

    class Meta:
        ordering = ('default_position',)
        verbose_name = 'Оффер'
        verbose_name_plural = 'Офферы'

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('credit:offer', args=[str(self.slug)])


class Comment(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='comments', verbose_name='Оффер')
    author = models.CharField(max_length=50, verbose_name='Автор')
    date_created = models.DateTimeField(default=timezone.now, verbose_name='Дата написания')
    text = models.TextField(max_length=4000, verbose_name='Комментарий')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='Оценка')

    class Meta:
        ordering = ('-date_created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.offer.title + ' - ' + self.author


class UnverifiedComment(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='unverified_comments', verbose_name='Оффер')
    author = models.CharField(max_length=50, verbose_name='Автор')
    date_created = models.DateTimeField(default=timezone.now, verbose_name='Дата написания')
    text = models.TextField(max_length=4000, verbose_name='Комментарий')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='Оценка')
    ip = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=1000)

    class Meta:
        ordering = ('-date_created',)
        verbose_name = 'Непроверенный комментарий'
        verbose_name_plural = 'Непроверенные комментарии'

    def __str__(self):
        return self.offer.title + ' - ' + self.author


class StashedComment(models.Model):
    author = models.CharField(max_length=50, verbose_name='Автор')
    date_created = models.DateTimeField(default=timezone.now, verbose_name='Дата написания')
    text = models.TextField(max_length=4000, verbose_name='Комментарий')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='Оценка')

    class Meta:
        ordering = ('-date_created',)
        verbose_name = 'Комментарий из пула'
        verbose_name_plural = 'Комментарии из пула'

    def __str__(self):
        return self.date_created.strftime("%Y-%m-%d %H:%M:%S") + ' - ' + self.author


