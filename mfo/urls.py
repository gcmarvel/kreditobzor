from django.urls import path
from .views import MFOOfferView

app_name = 'mfo'
urlpatterns = [
    path('организация/<str:slug>', MFOOfferView.as_view(), name='offer'),
]