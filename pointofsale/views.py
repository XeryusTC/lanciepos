from django.shortcuts import render
from django.views.generic import base, edit, ListView
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.conf import settings

from pointofsale.forms import BuyDrinkForm, RegisterParticipantForm
from pointofsale.models import Drink, Account, DrinkOrder

from django.contrib.auth.models import User

# Create your views here.
class BuyDrinkView(edit.FormView):
    template_name = "pointofsale/buydrink.html"
    form_class = BuyDrinkForm
    success_url = reverse_lazy("pos:buy_drink")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BuyDrinkView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BuyDrinkView, self).get_context_data(**kwargs)

        context['drinks'] = {}
        for drink in Drink.objects.all():
            context['drinks'][drink.name] = drink.price

        context['accounts'] = {}
        for account in Account.objects.all():
            if account.get_credits_left() > 0:
                context['accounts'][account.pk] = {'credits': account.credits, 'used': account.get_credits_used(),
                        'left': account.get_credits_left(), 'name': account.user.get_full_name() }

        context['log'] = DrinkOrder.objects.order_by('-time')[:10]

        return context

    #@method_decorator(login_required)
    #@method_decorator(require_POST)
    def form_valid(self, form):
        form.buy_drink()
        return super(BuyDrinkView, self).form_valid(form)


class RegisterParticipantView(edit.FormView):
    template_name = "pointofsale/register.html"
    form_class = RegisterParticipantForm
    success_url = reverse_lazy("pos:finish_register")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RegisterParticipantView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RegisterParticipantView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        self.success_url = form.register_participant()
        return super(RegisterParticipantView, self).form_valid(form)


class RegisterDoneView(base.TemplateView):
    template_name = "pointofsale/register_done.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RegisterDoneView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RegisterDoneView, self).get_context_data(**kwargs)
        context['entryfee_form'] = "pointofsale/" + kwargs['participant'] + "_entryfee.pdf"
        context['security_form'] = "pointofsale/" + kwargs['participant'] + "_security.pdf"

        context['account'] = Account.objects.get(pk=kwargs['participant'])

        return context


class OverviewView(ListView):
    model = Account

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(OverviewView, self).dispatch(*args, **kwargs)


@login_required
def add_credits(request, participant):
    a = Account.objects.get(pk=participant)
    a.credits += 5000
    a.save()
    return HttpResponseRedirect(reverse('pos:finish_register', kwargs={'participant': participant}))
