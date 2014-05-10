from django.shortcuts import render
from django.views.generic import edit
from django.core.urlresolvers import reverse_lazy

from pointofsale.forms import BuyDrinkForm

from pointofsale.models import Drink, Account

# Create your views here.
class BuyDrinkView(edit.FormView):
    template_name = 'pointofsale/buydrink.html'
    form_class = BuyDrinkForm
    
    def get_context_data(self, **kwargs):
        context = super(BuyDrinkView, self).get_context_data(**kwargs)
        
        context['drinks'] = {}
        for drink in Drink.objects.all():
            context['drinks'][drink.name] = drink.price
        
        context['users'] = {}
        for account in Account.objects.all():
            if account.get_credits_left() > 0:
                context['users'][account.pk] = (account.credits, account.get_credits_used())
        
        return context
