from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist

from .models import Offer, Comment, UnverifiedComment

from manager.views import get_rating, get_count


class CommentInline(admin.TabularInline):
    model = Comment


class OfferAdmin(admin.ModelAdmin):
    model = Offer
    inlines = [
        CommentInline
    ]

    def save_model(self, request, obj, form, change):
        pos = form.instance.default_position
        offer_list = []
        try:
            cur_obj = Offer.objects.get(default_position=pos)
            if obj != cur_obj:
                while True:
                    try:
                        cur_obj = Offer.objects.get(default_position=pos)
                        offer_list.append(cur_obj)
                        pos += 1
                    except ObjectDoesNotExist:
                        break
                for offer in offer_list:
                    offer.default_position += 1
                    offer.save()
                    super().save_model(request, obj, form, change)
            super().save_model(request, obj, form, change)
        except ObjectDoesNotExist:
            super().save_model(request, obj, form, change)
        obj.rating = get_rating(obj)
        obj.count = get_count(obj)
        obj.save()

    def change_view(self, request, object_id, form_url='', extra_context=None):
        print(object_id)
        obj = Offer.objects.get(id=object_id)
        obj.rating = get_rating(obj)
        obj.count = get_count(obj)
        obj.save()

        return super().change_view(
            request, object_id, form_url, extra_context=None,
        )



admin.site.register(Offer, OfferAdmin)
admin.site.register(Comment)
admin.site.register(UnverifiedComment)
