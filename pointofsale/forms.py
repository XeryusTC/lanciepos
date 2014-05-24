import random, string, datetime, subprocess
from django import forms
from django.core.urlresolvers import reverse
from pointofsale.models import Drink, Account, DrinkOrder
from django.contrib.auth.models import User

class BuyDrinkForm(forms.Form):
    account = forms.ChoiceField(required=True, widget=forms.RadioSelect)
    drink = forms.ChoiceField(required=True, widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super(BuyDrinkForm, self).__init__(*args, **kwargs)

        self.fields['drink'].choices = ( (drink.pk, drink.name) for drink in Drink.objects.all() )
        self.fields['account'].choices = ( (account.pk, account.pk) for account in Account.objects.order_by('user__first_name') if account.get_credits_left() > 0)

    def clean(self):
        super(BuyDrinkForm, self).clean()
        # see if all the fields are filled out
        if not 'account' in self.cleaned_data or not 'drink' in self.cleaned_data:
            raise forms.ValidationError("You must select a drink and a person before you can press the buy button")

        # Check if the account can afford the drink that it wants to buy, raise an error if this is not the case
        account = Account.objects.get(pk = self.cleaned_data['account'])
        drink = Drink.objects.get(pk = self.cleaned_data['drink'])

        if drink.price > account.get_credits_left():
            raise forms.ValidationError("%(name)s has insufficient funds to buy %(drink)s" % {'name': account.user.get_full_name(), 'drink': drink.name})
        return self.cleaned_data

    def buy_drink(self):
        account = Account.objects.get(pk = self.cleaned_data['account'])
        drink = Drink.objects.get(pk = self.cleaned_data['drink'])
        DrinkOrder.objects.create(drink = drink, account = account)


class ToolsForm(forms.Form):
    account = forms.ChoiceField(required=True, widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super(ToolsForm, self).__init__(*args, **kwargs)

        self.fields['account'].choices = ( (account.pk, account.pk) for account in Account.objects.order_by('user__first_name') )


class RegisterParticipantForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name  = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    address = forms.CharField(required=True)
    city = forms.CharField(required=True)
    iban = forms.CharField(required=True, max_length=18)
    charge = forms.IntegerField(initial=20)

    def register_participant(self):
        # create user
        username = self.cleaned_data['last_name'][:8] + ''.join(random.sample(string.ascii_letters + string.digits, 8))
        u = User.objects.create_user(username, self.cleaned_data['email'], username) # Use the username as the password
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        u.save()
        # create bar account
        a = Account(user=u, address=self.cleaned_data['address'], city=self.cleaned_data['city'], iban=self.cleaned_data['iban'])
        a.save()

        with open("templates/DirectDebitForm.tex", "r") as fin:
            # dictionaries holding static data for both forms
            data_dict = {'name': u.get_full_name(), 'address': self.cleaned_data['address'], 'city': self.cleaned_data['city'], 'iban': self.cleaned_data['iban'], 'email': self.cleaned_data['email']}
            security_dict = {'description': "Security for drinks", 'amount': 50, 'date': datetime.date.today().isoformat(), 'id': u.pk}
            security_dict.update(data_dict)
            entryfee_dict = {'description': "I LAN No English", 'amount': self.cleaned_data['charge'], 'date': datetime.date.today().isoformat(), 'id': u.pk}
            entryfee_dict.update(data_dict)

            # Read the template
            template = fin.read()
            form = string.Template(template)

            # Generate the appropriate tex files
            security_target = "generated_forms/{name}_security.tex".format(name=u.pk)
            entryfee_target = "generated_forms/{name}_entryfee.tex".format(name=u.pk)
            with open(security_target, 'w') as fout:
                fout.write(form.substitute(security_dict))
            with open(entryfee_target, 'w') as fout:
                fout.write(form.substitute(entryfee_dict))

            # TODO: generate the pdf files
            subprocess.call(["pdflatex", "-output-directory=static/pointofsale", security_target])
            subprocess.call(["pdflatex", "-output-directory=static/pointofsale", entryfee_target])
        return reverse("pos:finish_register", kwargs={'participant': u.pk})


