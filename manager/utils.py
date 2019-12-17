import urllib.parse
from user_agents import parse

from django.conf import settings
from django.http import HttpResponseRedirect

from mfo.models import Offer as MFOOffer
from credit.models import Offer as CreditOffer
from manager.models import TeaserClick


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

    if 'r' in request.GET:
        click = TeaserClick()
        click.link = urllib.parse.unquote(request.get_full_path()) + ' / ' + offer.title
        click.banner = request.GET.get('r')
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        click.ip = ip
        user_agent = parse(request.META.get('HTTP_USER_AGENT', ''))
        click.useragent = str(user_agent)
        referer = request.META.get('HTTP_REFERER')
        if not referer:
            referer = 'Нет реферера'
        click.referer = referer
        if 'r_c' not in request.session:
            request.session['r_c'] = '1'
        else:
            request.session['r_c'] = str(int(request.session['r_c']) + 1)
        click.cookie_counter = int(request.session['r_c'])
        click.save()


    return HttpResponseRedirect(offer.link)
