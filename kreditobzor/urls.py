from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from .utils import get_homepage as homepage
from.sitemaps import StaticSitemap, MFOSitemap, CreditSitemap, NewsSitemap, ArticleSitemap
from news.views import NewsView, ArticlesView
from manager.utils import referrer_count

sitemaps = {
    'static': StaticSitemap,
    'mfo': MFOSitemap,
    'credit': CreditSitemap,
    'news': NewsSitemap,
    'articles': ArticleSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('', homepage, name='home'),
    path('онлайн_займы/', include('mfo.urls', namespace='mfo')),
    path('кредитные_карты/', include('credit.urls')),
    path('новости/', NewsView.as_view(), name='news'),
    path('статьи/', ArticlesView.as_view(), name='articles'),
    path('новости_и_статьи/', include('news.urls')),
    path('реклама/', include('ads.urls')),
    path('manager/', include('manager.urls')),
    path('оформить/<str:app_name>/<int:pk>/', referrer_count, name='ref_count'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('webpush/', include('webpush.urls')),
    path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/x-javascript')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
