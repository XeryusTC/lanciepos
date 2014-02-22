from django.shortcuts import render
from django.views import generic
from django.core.serializers import serialize
from django.http import HttpResponse

from notify.models import Notification

class IndexView(generic.TemplateView):
    template_name = 'notify/overview.html'

class UpdateView(generic.base.View):
    def get(self, request, *args, **kwargs):
        # Return the last updates, limit to the last 5
        notifications = Notification.objects.filter(id__gt=request.GET['id'])[:5]
        return HttpResponse(serialize('json', notifications))
