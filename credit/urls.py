from django.urls import path
from .views import CreditOfferView

app_name = 'credit'
urlpatterns = [
    path('организация/<str:slug>', CreditOfferView.as_view(), name='offer'),
]