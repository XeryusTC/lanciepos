from django.shortcuts import render
from django.views.generic import base, edit, ListView
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings

from pointofsale.forms import BuyDrinkForm, RegisterParticipantForm
from pointofsale.models import Drink, Account, DrinkOrder

from django.contrib.auth.models import User

import datetime, string, subprocess

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
        proper_id = int(kwargs['participant'])
        if proper_id < 17:
                proper_id += 1
        context['entryfee_form'] = "pointofsale/" + str(proper_id) + "_entryfee.pdf"
        context['security_form'] = "pointofsale/" + str(proper_id) + "_security.pdf"

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

@login_required
def generate_csv(request):
    csv_entryfee = ['''"id", "description", "committee", "amount", "name", "address", "place of residence", iban", "email", "date"''']
    csv_drinks = ['''"id", "description", "committee", "amount", "name", "address", "place of residence", "iban", "email", "date"''']
    csv_row = '''{id}, "{desc}", "{committee}", "{amount}", "{name}", "{address}", "{city}", {iban}, "{email}", "{date}"'''
    for a in Account.objects.all():
        # add data to csv
        csv_entryfee.append(csv_row.format(id=a.user.pk, desc="I LAN no English entry", committee="LanCie", amount="",
            name=a.user.get_full_name(), address=a.address, city=a.city, iban=a.iban, email=a.user.email,
            date=datetime.date.today().isoformat()))
        csv_drinks.append(csv_row.format(id=a.user.pk, desc="I LAN no English drinks", committee="LanCie", amount=a.get_credits_used()/100.0,
            name=a.user.get_full_name(), address=a.address, city=a.city, iban=a.iban, email=a.user.email,
            date=datetime.date.today().isoformat()))

        # generate drink direct debit forms
        with open("templates/DirectDebitForm.tex", "r") as ftempl:
            template = ftempl.read()
            form = string.Template(template)
            target = "generated_forms/{name}_drinks.tex".format(name=a.pk)
            with open(target, 'w') as fout:
                fout.write(form.substitute({'description': "I LAN no English drinks", 'amount': a.get_credits_used()/100.0,
                    'date':datetime.date.today().isoformat(), 'id': a.user.pk, 'name': a.user.get_full_name(), 'address': a.address,
                    'city': a.city, 'iban': a.iban, 'email': a.user.email}))
                subprocess.call(["pdflatex", "-output-directory=static/pointofsale", target])

    # write csv files
    with open("entryfee.csv", "w") as fentry:
        fentry.write('\n'.join(csv_entryfee))
    with open("drinks.csv", "w") as fdrink:
        fdrink.write('\n'.join(csv_drinks))
    return HttpResponse("Done generating...<br /><br />{0}<br /><br />{1}".format('<br/>'.join(csv_entryfee), '<br />'.join(csv_drinks)));
