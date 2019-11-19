from django.shortcuts import reverse
from django.contrib.sitemaps import Sitemap
from mfo.models import Offer as MFOOffer
from credit.models import Offer as CreditOffer
from news.models import News, Article


class StaticSitemap(Sitemap):

    def items(self):
        return ['home', ]

    def location(self, item):
        return reverse(item)


class MFOSitemap(Sitemap):

    def items(self):
        return MFOOffer.objects.all()


class CreditSitemap(Sitemap):

    def items(self):
        return CreditOffer.objects.all()


class NewsSitemap(Sitemap):

    def items(self):
        return News.objects.all()


class ArticleSitemap(Sitemap):

    def items(self):
        return Article.objects.all()
