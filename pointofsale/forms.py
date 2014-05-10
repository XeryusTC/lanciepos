from django import forms
from pointofsale.models import Drink, Account
#from django.forms.extras.widgets import RadioSelect

class BuyDrinkForm(forms.Form):
    account = forms.ChoiceField(required=True, widget=forms.RadioSelect)
    drink = forms.ChoiceField(required=True, widget=forms.RadioSelect)
    
    def __init__(self, *args, **kwargs):
        super(BuyDrinkForm, self).__init__(*args, **kwargs)
        
        self.fields['drink'].choices = ( (drink.pk, drink.name) for drink in Drink.objects.all() )
        self.fields['account'].choices = ( (account.pk, account.pk) for account in Account.objects.order_by('user__first_name') if account.get_credits_left() > 0)
