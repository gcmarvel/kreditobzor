from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.utils import timezone

from django.conf import settings
from manager.utils import get_rating, get_count
from mfo.models import Comment as MFOComments
from mfo.models import UnverifiedComment as MFOUnverifiedComments
from credit.models import Comment as CreditComments
from credit.models import UnverifiedComment as CreditUnverifiedComments

from django.views.decorators.csrf import csrf_exempt


import json
from push_notifications.models import WebPushDevice
from push_notifications.webpush import WebPushError


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
                        device.send_message(json.dumps({'message': request.POST['push_body'], 'title': request.POST['push_head']}))
                    except WebPushError:
                        try:
                            device.browser = "FIREFOX"
                            device.save()
                            device.send_message(json.dumps({'message': request.POST['push_body'], 'title': request.POST['push_head']}))
                        except WebPushError:
                            try:
                                device.browser = "OPERA"
                                device.save()
                                device.send_message(json.dumps({'message': request.POST['push_body'], 'title': request.POST['push_head'], 'tag': 'https://www.кредитобзор.рф'}))
                            except WebPushError:
                                device.delete()
                                pass
                return render(request, 'push.html')
            return render(request, 'push.html')
        else:
            return render(request, 'push.html')
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

