from django.shortcuts import render, reverse
from django.utils import timezone

from manager.utils import get_rating, get_count
from mfo.models import Comment as MFOComments
from mfo.models import UnverifiedComment as MFOUnverifiedComments
from credit.models import Comment as CreditComments
from credit.models import UnverifiedComment as CreditUnverifiedComments


def manager(request):
    if request.user.is_authenticated:
        mfo_comments = MFOUnverifiedComments.objects.all()
        credit_comments = CreditUnverifiedComments.objects.all()
        context = {
            'mfo_comments': mfo_comments,
            'credit_comments': credit_comments,
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
