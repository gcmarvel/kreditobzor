from django.urls import path
from .views import NewsDetailView, ArticlesDetailView

app_name = 'news'
urlpatterns = [
    path('новость/<int:pk>', NewsDetailView.as_view(), name='news_detail'),
    path('статья/<int:pk>', ArticlesDetailView.as_view(), name='article_detail'),
]