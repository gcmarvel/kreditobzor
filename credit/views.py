from django.shortcuts import redirect, reverse
from django.conf import settings
from django.views.generic import ListView, DetailView
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from manager.utils import get_rating, get_count, referrer
from .models import Offer, Comment, UnverifiedComment
from ads.models import SidebarBanner
from manager.forms import CommentForm

app_list = settings.APP_LIST
app_name = 'кредитные_карты'


class CreditHomeView (ListView):

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
        return super(CreditHomeView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        referrer(self)

        filter_list = {'народный_выбор': 'народный выбор', 'высокое_одобрение': 'высокий % одобрения', 'процентная_ставка': 'по процентной ставке',
                       'цена_обслуживания': 'по цене обслуживания', 'кредитный_лимит': 'по кредитному лимиту', 'кэшбэк': 'по величине кэшбэка'}
        context = super().get_context_data(**kwargs)
        if 's' in self.request.GET:
            for key, value in filter_list.items():
                if self.request.GET['s'] == key:
                    context['filter'] = value
        else:
            context['filter'] = 'Сортировать по ...'
        context['filter_list'] = filter_list
        context['app_name'] = 'Кредитные карты'
        context['sidebanners'] = SidebarBanner.objects.filter(reference_app=app_name).filter(enabled=True)
        return context

    def get_queryset(self):
        if 's' in self.request.GET:
            if self.request.GET['s'] == 'народный_выбор':
                return Offer.objects.all().order_by('-rating')
            if self.request.GET['s'] == 'высокое_одобрение':
                return Offer.objects.all().order_by('-high_approval_rate')
            if self.request.GET['s'] == 'процентная_ставка':
                return Offer.objects.all().order_by('min_rate')
            if self.request.GET['s'] == 'кредитный_лимит':
                return Offer.objects.all().order_by('-limit')
            if self.request.GET['s'] == 'кэшбэк':
                return Offer.objects.all().order_by('-cashback')
            if self.request.GET['s'] == 'цена_обслуживания':
                return Offer.objects.all().order_by('maintenance')
        else:
            return Offer.objects.all()


class CreditOfferView (DetailView):

    model = Offer
    template_name = 'offer.html'
    context_object_name = 'offer'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(offer=self.object)
        paginator = Paginator(comments, self.paginate_by)

        referrer(self)

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
        context['app_name'] = 'Кредитные карты'
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
            new_comment = UnverifiedComment(offer=offer, author=self.request.POST['author'], text=self.request.POST['text'], rating=self.request.POST['hidden-rating'])
            new_comment.save()
        return HttpResponseRedirect(reverse('credit:offer', kwargs={'slug': slug}))


