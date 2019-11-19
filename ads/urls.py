from django.urls import path
from .views import sidebaner_count

app_name = 'ads'
urlpatterns = [
    path('боковой_баннер/<int:pk>', sidebaner_count, name='sidebanner_count'),
]