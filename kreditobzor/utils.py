from mfo.views import MFOHomeView
from credit.views import CreditHomeView


def get_homepage(request):
    if 'h' not in request.session:
        request.session['h'] = 'мфо'
        return MFOHomeView.as_view()(request)
    elif request.session['h'] == 'мфо':
        return MFOHomeView.as_view()(request)
    elif request.session['h'] == 'кредитные_карты':
        return CreditHomeView.as_view()(request)
