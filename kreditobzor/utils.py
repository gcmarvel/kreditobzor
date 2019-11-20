from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.contrib import admin

from mfo.views import MFOHomeView
from credit.views import CreditHomeView

admin.site.unregister(Group)
admin.site.unregister(Site)


def get_homepage(request):
    if 'h' not in request.session:
        request.session['h'] = 'мфо'
        return MFOHomeView.as_view()(request)
    elif request.session['h'] == 'мфо':
        return MFOHomeView.as_view()(request)
    elif request.session['h'] == 'кредитные_карты':
        return CreditHomeView.as_view()(request)
