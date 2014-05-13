from django.shortcuts import render
from django.views.generic import edit
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect

from pointofsale.forms import BuyDrinkForm

from pointofsale.models import Drink, Account, DrinkOrder

# Create your views here.
class BuyDrinkView(edit.FormView):
    template_name = 'pointofsale/buydrink.html'
    form_class = BuyDrinkForm
    success_url = reverse_lazy('pos:buy_drink')
    
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
        
        return context

    #@method_decorator(login_required)
    #@method_decorator(require_POST)
    def form_valid(self, form):
        form.buy_drink()
        return super(BuyDrinkView, self).form_valid(form)
