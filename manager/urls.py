from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.manager, name='manager'),
    path('mfo/accept/<int:comment_id>-<str:app>', views.accept_comment, name='accept-comment'),
    path('mfo/delete/<int:comment_id>-<str:app>', views.delete_comment, name='delete-comment'),
    path('mfo/edit/<int:comment_id>-<str:app>', views.edit_comment, name='edit-comment'),
    path('webpush/', include('webpush.urls')),
    path('send_push', views.send_push, name='push'),
]