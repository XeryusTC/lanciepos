from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import edit, TemplateView, ListView

from routing.forms import RequestAccessForm

from django.contrib.auth.models import User
from routing.models import Client

class RequestAccessView(edit.FormView):
	template_name = 'routing/request_access.html'
	form_class = RequestAccessForm
	success_url = reverse_lazy('routing:request_success')
	
	def form_valid(self, form):
		u = User.objects.get(email=form.cleaned_data['email']) # Get the user
		u.set_password('test')
		u.save()
		
		ip = self.request.META.get('REMOTE_ADDR')
		c = Client.objects.create(user=u, ipaddress=ip)
		c.save()
		
		return super(RequestAccessView, self).form_valid(form)

class RequestSuccessView(TemplateView):
	template_name='routing/request_success.html'

class GrantAccessOverviewView(ListView):
	template_name='routing/grant_access.html'
	error_message = ""
	
	def get_queryset(self):
		"""Return all of the people who have not been granted access yet"""
		if len(self.args) > 0:
			self.error_message = self.args[0]
		return Client.objects.filter(access_granted=False)
	
	def get_context_data(self, **kwargs):
		context = super(GrantAccessOverviewView, self).get_context_data(**kwargs)
		context['error_message'] = self.error_message
		return context
	
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(GrantAccessOverviewView, self).dispatch(*args, **kwargs)

@login_required
@require_POST
def grant_access(request, client_id):
	import Pyro4
	from routing import access

	client = get_object_or_404(Client, pk=client_id)
	
	try:
		iptables = Pyro4.Proxy("PYRONAME:access.manager")
		iptables.add_to_whitelist(client.ipaddress)
	except Exception as ex:
		if ex.args[0]:
			error_message = ex.args[0]
		else:
			error_message = ex
		return HttpResponseRedirect(reverse('routing:grant_access_overview_error', args=(error_message,)))
	else:
		client.rule_signed = True
		client.access_granted = True
		client.save()
		return HttpResponseRedirect(reverse('routing:grant_access_overview'))
