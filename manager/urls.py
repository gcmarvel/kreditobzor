from django.urls import path
from . import views

urlpatterns = [
    path('', views.manager, name='manager'),
    path('mfo/accept/<int:comment_id>-<str:app>', views.accept_comment, name='accept-comment'),
    path('mfo/delete/<int:comment_id>-<str:app>', views.delete_comment, name='delete-comment'),
    path('mfo/edit/<int:comment_id>-<str:app>', views.edit_comment, name='edit-comment'),
    path('send_push/', views.send_push, name='push'),
    path('subscribe', views.subscription, name='subscription'),
    path('referals', views.referals, name='referals'),
    path('comments', views.comments, name='comments'),
    path('distribute-stashed/<str:app>', views.distribute_stashed, name='distribute-stashed')
]