from django import forms
from pointofsale.models import Drink, Account, DrinkOrder
#from django.forms.extras.widgets import RadioSelect

class BuyDrinkForm(forms.Form):
    account = forms.ChoiceField(required=True, widget=forms.RadioSelect)
    drink = forms.ChoiceField(required=True, widget=forms.RadioSelect)
    
    def __init__(self, *args, **kwargs):
        super(BuyDrinkForm, self).__init__(*args, **kwargs)
        
        self.fields['drink'].choices = ( (drink.pk, drink.name) for drink in Drink.objects.all() )
        self.fields['account'].choices = ( (account.pk, account.pk) for account in Account.objects.order_by('user__first_name') if account.get_credits_left() > 0)
    
    def clean(self):
        super(BuyDrinkForm, self).clean()
        
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

