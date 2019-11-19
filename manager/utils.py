from django.conf import settings
from django.http import HttpResponseRedirect

from mfo.models import Offer as MFOOffer
from credit.models import Offer as CreditOffer


def get_rating(offer):
    rating = 0
    rating_list = []
    for comment in offer.comments.all():
        rating_list.append(comment.rating)
    if rating_list != []:
        rating = "%.2f" % ((sum(rating_list) / len(rating_list)) * 2)
    return float(rating)


def get_count(offer):
    count = len(offer.comments.all())
    return count


def get_choices():
    choices = ()
    for app in settings.APP_LIST:
        inner_tuple = (app, app)
        choices += (inner_tuple, )
    return choices


def get_app_offer(app_name):
    if app_name == 'мфо':
        return MFOOffer
    elif app_name == 'кредитные_карты':
        return CreditOffer


def referrer_count(request, app_name, pk):
    offer = get_app_offer(app_name).objects.get(pk=pk)
    offer.clicked += 1
    offer.save()
    return HttpResponseRedirect(offer.link)
