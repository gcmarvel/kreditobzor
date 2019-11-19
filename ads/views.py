from django.http import HttpResponseRedirect
from .models import SidebarBanner


def sidebaner_count(request, pk):
    add = SidebarBanner.objects.get(pk=pk)
    add.clicked += 1
    add.save()
    return HttpResponseRedirect(add.link)
