from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.conf import settings
from manager.utils import get_rating, get_count
from mfo.models import Comment as MFOComments
from mfo.models import UnverifiedComment as MFOUnverifiedComments
from credit.models import Comment as CreditComments
from credit.models import UnverifiedComment as CreditUnverifiedComments
from .models import TeaserClick

from django.views.decorators.csrf import csrf_exempt

import json
from push_notifications.models import WebPushDevice
from push_notifications.webpush import WebPushError

import datetime
from urllib.parse import urlparse
from collections import Counter


def manager(request):
    if request.user.is_authenticated:
        mfo_comments = MFOUnverifiedComments.objects.all()
        credit_comments = CreditUnverifiedComments.objects.all()
        webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
        context = {
            'mfo_comments': mfo_comments,
            'credit_comments': credit_comments,
            'vapid_key': webpush_settings.get('VAPID_PUBLIC_KEY'),
            'user': request.user,
        }
        return render(request, 'manager.html', context)
    else:
        return redirect('home')


def accept_comment(request, comment_id, app):
    if request.user.is_authenticated:
        if app == 'mfo':
            comment = MFOUnverifiedComments.objects.get(id=comment_id)
            new_comment = MFOComments(offer=comment.offer, author=comment.author, text=comment.text, rating=comment.rating, date_created=comment.date_created)
        elif app == 'credit':
            comment = CreditUnverifiedComments.objects.get(id=comment_id)
            new_comment = CreditComments(offer=comment.offer, author=comment.author, text=comment.text, rating=comment.rating, date_created=comment.date_created)
        comment.delete()
        new_comment.save()
        comment.offer.rating = get_rating(comment.offer)
        comment.offer.count = get_count(comment.offer)
        comment.offer.save()
        return manager(request)
    else:
        return redirect('home')


def delete_comment(request, comment_id, app):
    if request.user.is_authenticated:
        if app == 'mfo':
            comment = MFOUnverifiedComments.objects.get(id=comment_id)
        elif app == 'credit':
            comment = CreditUnverifiedComments.objects.get(id=comment_id)
        comment.delete()
        return manager(request)
    else:
        return redirect('home')


def edit_comment(request, comment_id, app):
    if request.user.is_authenticated:
        if app == 'mfo':
            comment = MFOUnverifiedComments.objects.get(id=comment_id)
        elif app == 'credit':
            comment = CreditUnverifiedComments.objects.get(id=comment_id)
        if request.method == "POST":
            author = request.POST['author']
            text = request.POST['text']
            rating = request.POST['rating']
            date = request.POST['date']
            comment.author = author
            comment.text = text
            comment.rating = rating
            comment.date_created = date
            comment.save()
            return manager(request)
        else:
            isodate = comment.date_created.astimezone(timezone.get_current_timezone()).strftime("%Y-%m-%dT%H:%M")
            context = {
                'app': app,
                'comment': comment,
                'isodate': isodate,
            }
            return render(request, 'edit_comment.html', context)
    else:
        return redirect('home')


def send_push(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if 'push_body' in request.POST:
                for device in WebPushDevice.objects.all():
                    try:
                        device.send_message(json.dumps({'message': request.POST['push_body'], 'title': request.POST['push_head'], 'tag': request.POST['push_url']}))
                    except WebPushError:
                        try:
                            device.browser = "FIREFOX"
                            device.save()
                            device.send_message(json.dumps({'message': request.POST['push_body'], 'title': request.POST['push_head'], 'tag': request.POST['push_url']}))
                        except WebPushError:
                            try:
                                device.browser = "OPERA"
                                device.save()
                                device.send_message(json.dumps({'message': request.POST['push_body'], 'title': request.POST['push_head'], 'tag': request.POST['push_url']}))
                            except WebPushError:
                                device.delete()
                                pass
                return render(request, 'push.html')
            return render(request, 'push.html')
        else:
            return render(request, 'push.html')
    else:
        return redirect('home')


def referals(request):
    if request.user.is_authenticated:
        referals = TeaserClick.objects.all()
        filter_list = {'netloc': 'Площадки', 'ip': 'IP', 'ua': 'Юзер агент'}

        if 'r_m_d' not in request.session:
            request.session['r_m_d'] = '7'
        if 'r_m_d' in request.GET:
            request.session['r_m_d'] = request.GET['r_m_d']

        referals_date = TeaserClick.objects.filter(timestamp__lte=datetime.datetime.now(), timestamp__gt=datetime.datetime.now() - datetime.timedelta(days=int(request.session['r_m_d'])))

        if 's' in request.GET:
            if request.GET['s'] == 'ip':
                ip_list = []
                referals_list = {}
                for referal in referals_date:
                    ip_list.append(referal.ip)
                    referals_list.update({referal.timestamp.strftime("%Y-%m-%d %H:%M:%S"): referal.ip})
                referals_stat = dict(Counter(ip_list).most_common())
            elif request.GET['s'] == 'ua':
                ua_list = []
                referals_list = {}
                for referal in referals_date:
                    ua_list.append(referal.useragent)
                    referals_list.update({referal.timestamp.strftime("%Y-%m-%d %H:%M:%S"): referal.useragent})
                referals_stat = dict(Counter(ua_list).most_common())
            else:
                netloc_list = []
                referals_list = {}
                for referal in referals_date:
                    if urlparse(referal.referer)[1] not in ('', 'clickscloud.net', 'cloudfastads.ru', 'clients.clickscloud.net'):
                        netloc_list.append(urlparse(referal.referer)[1])
                    if urlparse(referal.referer)[1] == '':
                        referals_list.update({referal.timestamp.strftime("%Y-%m-%d %H:%M:%S"): 'Нет реферера'})
                    else:
                        referals_list.update({referal.timestamp.strftime("%Y-%m-%d %H:%M:%S"): urlparse(referal.referer)[1]})
                referals_stat = dict(Counter(netloc_list).most_common())
        else:
            netloc_list = []
            referals_list = {}
            for referal in referals_date:
                if urlparse(referal.referer)[1] not in ('', 'clickscloud.net', 'cloudfastads.ru', 'clients.clickscloud.net'):
                    netloc_list.append(urlparse(referal.referer)[1])
                if urlparse(referal.referer)[1] == '':
                    referals_list.update({referal.timestamp.strftime("%Y-%m-%d %H:%M:%S"): 'Нет реферера'})
                else:
                    referals_list.update({referal.timestamp.strftime("%Y-%m-%d %H:%M:%S"): urlparse(referal.referer)[1]})
            referals_stat = dict(Counter(netloc_list).most_common())

        paginator = Paginator(referals, 100)
        page = request.GET.get('page')
        try:
            referals_page = paginator.page(page)
        except PageNotAnInteger:
            referals_page = paginator.page(1)
        except EmptyPage:
            referals_page = paginator.page(paginator.num_pages)

        context = {
            'filter_list': filter_list,
            'referals_stat': referals_stat,
            'referals_list': referals_list,
            'referals_page': referals_page,
        }
        return render(request, 'referals.html', context)
    else:
        return redirect('home')


@csrf_exempt
def subscription(request):
    if request.method == "POST":
        if 's' not in request.session:
            request.session['s'] = 'subscribed'
            browser = request.POST['browser']
            WebPushDevice.objects.get_or_create(name=request.POST['name'], browser=browser, p256dh=request.POST['p256dh'], auth=request.POST['auth'], registration_id=request.POST['registration_id'])
        return HttpResponse('200')

