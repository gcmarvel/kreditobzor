from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from django.conf import settings
from manager.utils import get_rating, get_count
from mfo.models import Offer as MFOOffer
from mfo.models import Comment as MFOComment
from mfo.models import UnverifiedComment as MFOUnverifiedComment
from mfo.models import StashedComment as MFOStashedComment
from credit.models import Offer as CreditOffer
from credit.models import Comment as CreditComment
from credit.models import UnverifiedComment as CreditUnverifiedComment
from credit.models import StashedComment as CreditStashedComment
from .models import TeaserClick, TeaserLead

from django.views.decorators.csrf import csrf_exempt

import json
from push_notifications.models import WebPushDevice
from push_notifications.webpush import WebPushError

import datetime
import random
from urllib.parse import urlparse
from collections import Counter


def manager(request):
    if request.user.is_authenticated:
        mfo_comments = MFOUnverifiedComment.objects.all()
        credit_comments = CreditUnverifiedComment.objects.all()
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
            comment = MFOUnverifiedComment.objects.get(id=comment_id)
            new_comment = MFOComment(offer=comment.offer, author=comment.author, text=comment.text, rating=comment.rating, date_created=comment.date_created)
        elif app == 'credit':
            comment = CreditUnverifiedComment.objects.get(id=comment_id)
            new_comment = CreditComment(offer=comment.offer, author=comment.author, text=comment.text, rating=comment.rating, date_created=comment.date_created)
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
            comment = MFOUnverifiedComment.objects.get(id=comment_id)
            comment.delete()
        elif app == 'mfo_verified':
            comment = MFOComment.objects.get(id=comment_id)
            comment.delete()
            comment.offer.rating = get_rating(comment.offer)
            comment.offer.count = get_count(comment.offer)
            comment.offer.save()
            return redirect('mfo:offer', comment.offer.slug)
        elif app == 'mfo_stashed':
            comment = MFOStashedComment.objects.get(id=comment_id)
            comment.delete()
            return redirect('comments')
        elif app == 'credit':
            comment = CreditUnverifiedComment.objects.get(id=comment_id)
            comment.delete()
        elif app == 'credit_verified':
            comment = CreditComment.objects.get(id=comment_id)
            comment.delete()
            comment.offer.rating = get_rating(comment.offer)
            comment.offer.count = get_count(comment.offer)
            comment.offer.save()
            return redirect('credit:offer', comment.offer.slug)
        elif app == 'credit_stashed':
            comment = CreditStashedComment.objects.get(id=comment_id)
            comment.delete()
            return redirect('comments')
        return manager(request)
    else:
        return redirect('home')


def edit_comment(request, comment_id, app):
    if request.user.is_authenticated:
        if app == 'mfo':
            comment = MFOUnverifiedComment.objects.get(id=comment_id)
        elif app == 'mfo_verified':
            comment = MFOComment.objects.get(id=comment_id)
        elif app == 'mfo_stashed':
            comment = MFOStashedComment.objects.get(id=comment_id)
        elif app == 'credit':
            comment = CreditUnverifiedComment.objects.get(id=comment_id)
        elif app == 'credit_verified':
            comment = CreditComment.objects.get(id=comment_id)
        elif app == 'credit_stashed':
            comment = CreditStashedComment.objects.get(id=comment_id)
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
            if app == 'mfo_stashed' or app == 'credit_stashed':
                return redirect('comments')
            if app == 'mfo_verified' or app == 'credit_verified':
                comment.offer.rating = get_rating(comment.offer)
                comment.offer.save()
                if app == 'mfo_verified':
                    return redirect('mfo:offer', comment.offer.slug)
                if app == 'credit_verified':
                    return redirect('credit:offer', comment.offer.slug)
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
        filter_list = {'netloc': 'Площадки', 'ip': 'IP', 'ua': 'Юзер агент', 'id': 'Идентификатор'}

        if 'r_m_d' not in request.session:
            request.session['r_m_d'] = '7'
        if 'r_m_d' in request.GET:
            request.session['r_m_d'] = request.GET['r_m_d']

        referals_date = TeaserClick.objects.filter(timestamp__gt=datetime.datetime.now() - datetime.timedelta(days=int(request.session['r_m_d'])))
        referals_lead = TeaserLead.objects.filter(timestamp__gt=datetime.datetime.now() - datetime.timedelta(days=int(request.session['r_m_d'])))

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
            elif request.GET['s'] == 'id':
                id_list = []
                referals_list = {}
                for referal in referals_date:
                    id_list.append(referal.banner)
                    referals_list.update({referal.timestamp.strftime("%Y-%m-%d %H:%M:%S"): referal.useragent})
                referals_stat = dict(Counter(id_list).most_common())
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
            'referals_lead': referals_lead,
            'referals_page': referals_page,
        }
        return render(request, 'referals.html', context)
    else:
        return redirect('home')


def comments(request):
    if request.user.is_authenticated:
        mfo_list = MFOOffer.objects.filter(active=True)
        mfo_dict = {}
        credit_list = CreditOffer.objects.filter(active=True)
        credit_dict = {}
        mfo_stashed = MFOStashedComment.objects.all()
        credit_stashed = CreditStashedComment.objects.all()
        for offer in mfo_list:
            try:
                mfo_dict[offer.title] = offer.comments.latest('date_created').date_created.strftime("%Y-%m-%d %H:%M:%S")
            except ObjectDoesNotExist:
                mfo_dict[offer.title] = 'Нет комментариев'
        for offer in credit_list:
            try:
                credit_dict[offer.title] = offer.comments.latest('date_created').date_created.strftime("%Y-%m-%d %H:%M:%S")
            except ObjectDoesNotExist:
                credit_dict[offer.title] = 'Нет комментариев'

        if request.method == 'POST':
            if request.POST['app_name'] == 'mfo':
                if request.POST['offer'] == "Пул":
                    stashed_comment = MFOStashedComment(author=request.POST['author'], text=request.POST['text'], rating=request.POST['rating'])
                    stashed_comment.save()
                else:
                    new_comment = MFOComment(offer=MFOOffer.objects.get(title=request.POST['offer']), author=request.POST['author'], text=request.POST['text'], rating=request.POST['rating'])
                    new_comment.save()
                    new_comment.offer.rating = get_rating(new_comment.offer)
                    new_comment.offer.count = get_count(new_comment.offer)
                    new_comment.offer.save()
            elif request.POST['app_name'] == 'credit':
                if request.POST['offer'] == "Пул":
                    stashed_comment = CreditStashedComment(author=request.POST['author'], text=request.POST['text'], rating=request.POST['rating'])
                    stashed_comment.save()
                else:
                    new_comment = CreditComment(offer=CreditOffer.objects.get(title=request.POST['offer']), author=request.POST['author'], text=request.POST['text'], rating=request.POST['rating'])
                    new_comment.save()
                    new_comment.offer.rating = get_rating(new_comment.offer)
                    new_comment.offer.count = get_count(new_comment.offer)
                    new_comment.offer.save()

        context = {
            'mfo_dict': mfo_dict,
            'credit_dict': credit_dict,
            'mfo_stashed': mfo_stashed,
            'credit_stashed': credit_stashed,
            'mfo_options': MFOOffer.objects.filter(active=True),
            'credit_options': CreditOffer.objects.filter(active=True),
        }
        return render(request, 'comments.html', context)
    else:
        return redirect('home')


def distribute_stashed(request, app):
    if app == 'mfo':
        offer_list = MFOOffer.objects.filter(active=True).exclude(Q(default_position__lt=5, comments__date_created__gt=datetime.datetime.now() - datetime.timedelta(days=3)) | Q(default_position__lt=10, default_position__gte=5, comments__date_created__gt=datetime.datetime.now() - datetime.timedelta(days=5)) | Q(default_position__gt=10, comments__date_created__gt=datetime.datetime.now() - datetime.timedelta(days=7)))

        stashed_comments = MFOStashedComment.objects.all()
        offers_and_comments = zip(offer_list, stashed_comments)
        for offer, comment in offers_and_comments:
            try:
                new_comment = MFOComment(offer=offer, author=comment.author, text=comment.text, rating=comment.rating, date_created=datetime.datetime.now() - datetime.timedelta(seconds=random.randrange(1, 86401)))
                new_comment.save()
                offer.rating = get_rating(offer)
                offer.count = get_count(offer)
                offer.save()
                comment.delete()
            except ObjectDoesNotExist:
                return redirect('comments')
        return redirect('comments')
    if app == 'credit':
        offer_list = CreditOffer.objects.filter(active=True).exclude(Q(default_position__lt=5, comments__date_created__gt=datetime.datetime.now() - datetime.timedelta(days=3)) | Q(default_position__lt=10, default_position__gte=5, comments__date_created__gt=datetime.datetime.now() - datetime.timedelta(days=5)) | Q(default_position__gt=10, comments__date_created__gt=datetime.datetime.now() - datetime.timedelta(days=7)))
        stashed_comments = CreditStashedComment.objects.all()
        offers_and_comments = zip(offer_list, stashed_comments)
        for offer, comment in offers_and_comments:
            try:
                new_comment = MFOComment(offer=offer, author=comment.author, text=comment.text, rating=comment.rating, date_created=datetime.datetime.now() - datetime.timedelta(seconds=random.randrange(1, 86401)))
                new_comment.save()
                offer.rating = get_rating(offer)
                offer.count = get_count(offer)
                offer.save()
                comment.delete()
            except ObjectDoesNotExist:
                return redirect('comments')
        return redirect('comments')


@csrf_exempt
def subscription(request):
    if request.method == "POST":
        if 's' not in request.session:
            request.session['s'] = 'subscribed'
            browser = request.POST['browser']
            WebPushDevice.objects.get_or_create(name=request.POST['name'], browser=browser, p256dh=request.POST['p256dh'], auth=request.POST['auth'], registration_id=request.POST['registration_id'])
        return HttpResponse('200')

