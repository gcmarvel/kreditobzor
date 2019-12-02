from django.shortcuts import render, reverse
from django.utils import timezone

from django.conf import settings
from manager.utils import get_rating, get_count
from mfo.models import Comment as MFOComments
from mfo.models import UnverifiedComment as MFOUnverifiedComments
from credit.models import Comment as CreditComments
from credit.models import UnverifiedComment as CreditUnverifiedComments

from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from webpush import send_user_notification
import json


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
        return reverse('home')


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
        return reverse('home')


def delete_comment(request, comment_id, app):
    if request.user.is_authenticated:
        if app == 'mfo':
            comment = MFOUnverifiedComments.objects.get(id=comment_id)
        elif app == 'credit':
            comment = CreditUnverifiedComments.objects.get(id=comment_id)
        comment.delete()
        return manager(request)
    else:
        return reverse('home')


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
        return reverse('home')


@csrf_exempt
def send_push(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            try:
                body = request.body
                data = json.loads(body)

                if 'head' not in data or 'body' not in data or 'id' not in data:
                    return JsonResponse(status=400, data={"message": "Invalid data format"})

                user_id = data['id']
                user = get_object_or_404(User, pk=user_id)
                payload = {'head': data['head'], 'body': data['body']}
                send_user_notification(user=user, payload=payload, ttl=1000)

                return JsonResponse(status=200, data={"message": "Web push successful"})
            except TypeError:
                return JsonResponse(status=500, data={"message": "An error occurred"})
        else:
            webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
            vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
            user = request.user
            return render(request, 'push.html', {user: user, 'vapid_key': vapid_key})
    else:
        return reverse('home')

