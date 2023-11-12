from django import forms
from .models import *
from django.forms import inlineformset_factory

class userForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['firstName','lastName','username', 'email', 'password']

class addressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['streetLine1', 'streetLine2', 'city', 'state', 'postalCode', 'country']

        


class userSignInForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

        widgets= {
            'username' : forms.TextInput(attrs={'placeholder': 'username', 'class' : 'sign-in-control'}),
            'password' : forms.TextInput(attrs={'placeholder': 'password', 'class' : 'sign-in-control'})
        }

            
#CombinedForm = inlineformset_factory(User, Address, fields='__all__', can_delete=False)