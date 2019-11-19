from django.urls import path
from . import views

urlpatterns = [
    path('', views.manager, name='manager'),
    path('mfo/accept/<int:comment_id>-<str:app>', views.mfo_accept_comment, name='mfo-accept-comment'),
    path('mfo/delete/<int:comment_id>-<str:app>', views.mfo_delete_comment, name='mfo-delete-comment'),
]