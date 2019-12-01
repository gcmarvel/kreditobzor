from django.urls import path, include
from . import views

from django.views.generic import TemplateView

urlpatterns = [
    path('', views.manager, name='manager'),
    path('mfo/accept/<int:comment_id>-<str:app>', views.accept_comment, name='accept-comment'),
    path('mfo/delete/<int:comment_id>-<str:app>', views.delete_comment, name='delete-comment'),
    path('mfo/edit/<int:comment_id>-<str:app>', views.edit_comment, name='edit-comment'),
    path('send_push', views.send_push),
    path('webpush/', include('webpush.urls')),
    path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/x-javascript')),
]