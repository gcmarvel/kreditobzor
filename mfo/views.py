from django.shortcuts import redirect, reverse
from django.contrib import messages
from django.conf import settings
from django.views.generic import ListView, DetailView
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from user_agents import parse

from manager.utils import get_rating, get_count
from .models import Offer, Comment, UnverifiedComment
from ads.models import SidebarBanner
from manager.forms import CommentForm

app_list = settings.APP_LIST
app_name = 'мфо'


class MFOHomeView (ListView):

    model = Offer
    context_object_name = 'offers'
    paginate_by = 9
    template_name = 'home.html'

    def dispatch(self, request, *args, **kwargs):
        if 'h' in self.request.GET:
            if self.request.GET['h'] != app_name:
                for app in app_list:
                    if self.request.GET['h'] == app:
                        self.request.session['h'] = app
                        return redirect('home')
        return super(MFOHomeView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        filter_list = {'народный_выбор': 'народный выбор', 'высокое_одобрение': 'высокий % одобрения', 'процентная_ставка': 'по процентной ставке',
                       'величина_суммы': 'по величине суммы', 'акция_займ': 'акция займ под 0%', 'самые_обсуждаемые': 'самые обсуждаемые'}
        webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
        vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
        context = super().get_context_data(**kwargs)
        if 's' in self.request.GET:
            for key, value in filter_list.items():
                if self.request.GET['s'] == key:
                    context['filter'] = value
        else:
            context['filter'] = 'Сортировать по ...'
        context['filter_list'] = filter_list
        context['app_name'] = 'Займы'
        context['sidebanners'] = SidebarBanner.objects.filter(reference_app=app_name).filter(enabled=True)
        context['user'] = self.request.user
        context['vapid_key'] = vapid_key
        return context

    def get_queryset(self):
        if 's' in self.request.GET:
            if self.request.GET['s'] == 'народный_выбор':
                return Offer.objects.all().order_by('-rating')
            if self.request.GET['s'] == 'высокое_одобрение':
                return Offer.objects.all().order_by('-high_approval_rate')
            if self.request.GET['s'] == 'процентная_ставка':
                return Offer.objects.all().order_by('min_rate')
            if self.request.GET['s'] == 'величина_суммы':
                return Offer.objects.all().order_by('-max_sum')
            if self.request.GET['s'] == 'акция_займ':
                return Offer.objects.all().order_by('-special_offer')
            if self.request.GET['s'] == 'самые_обсуждаемые':
                return Offer.objects.all().order_by('-count')
        else:
            return Offer.objects.all()


class MFOOfferView (DetailView):

    model = Offer
    template_name = 'offer.html'
    context_object_name = 'offer'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(offer=self.object)
        paginator = Paginator(comments, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)

        context['comments'] = comments
        context['page_obj'] = comments
        context['form'] = CommentForm
        context['app_name'] = 'Займы'
        context['sidebanners'] = SidebarBanner.objects.filter(reference_app=app_name).filter(enabled=True)
        context['promoted_offers'] = Offer.objects.filter(promoted=True)
        return context

    def post(self, request, **kwargs):
        slug = self.request.POST['organization']
        offer = Offer.objects.get(slug=slug)
        if self.request.user.is_authenticated:
            new_comment = Comment(offer=offer, author=self.request.POST['author'], text=self.request.POST['text'], rating=self.request.POST['hidden-rating'])
            new_comment.save()
            offer.rating = get_rating(offer)
            offer.count = get_count(offer)
            offer.save()
        else:
            messages.add_message(request, messages.SUCCESS, 'Спасибо за Ваш отзыв! Комментарий будет опубликован в течение 24 часов после проверки на спам и накрутку рейтинга')
            x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = self.request.META.get('REMOTE_ADDR')
            user_agent = parse(self.request.META.get('HTTP_USER_AGENT', ''))
            new_comment = UnverifiedComment(offer=offer, author=self.request.POST['author'], text=self.request.POST['text'], rating=self.request.POST['hidden-rating'], ip=ip, user_agent=str(user_agent))
            new_comment.save()
        return HttpResponseRedirect(reverse('mfo:offer', kwargs={'slug': slug}))


