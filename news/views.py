from django.views.generic import ListView, DetailView

from manager.utils import get_app_offer
from .models import News, Article
from ads.models import SidebarBanner


class NewsView(ListView):
    model = News
    context_object_name = 'news'
    template_name = 'news.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Новости'
        return context


class ArticlesView(ListView):
    model = Article
    context_object_name = 'news'
    template_name = 'news.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Статьи'
        return context


class NewsDetailView(DetailView):
    model = News
    context_object_name = 'article'
    template_name = 'article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebanners'] = SidebarBanner.objects.filter(reference_app=self.object.reference_app).filter(enabled=True)
        context['promoted_offers'] = get_app_offer(self.object.reference_app).objects.filter(promoted=True)
        return context


class ArticlesDetailView(DetailView):
    model = Article
    context_object_name = 'article'
    template_name = 'article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebanners'] = SidebarBanner.objects.filter(reference_app=self.object.reference_app).filter(enabled=True)
        context['promoted_offers'] = get_app_offer(self.object.reference_app).objects.filter(promoted=True)
        return context
