from django import forms
from .models import *


class userForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['firstName','lastName','username', 'email', 'password']

class addressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['streetLine1', 'streetLine2', 'city', 'state', 'postalCode', 'country']

        


class userSignInForm(forms.Form):
    username = forms.CharField(max_length=50,label="", widget=forms.TextInput(attrs={'placeholder': 'username', 'class' : 'sign-in-control'}))
    password = forms.CharField(max_length=50, label="", widget=forms.TextInput(attrs={'placeholder': 'password', 'class' : 'sign-in-control'}))
    widgets= {
        'username' : forms.TextInput(attrs={'placeholder': 'username', 'class' : 'sign-in-control'}),
        'password' : forms.TextInput(attrs={'placeholder': 'password', 'class' : 'sign-in-control'})
    }


            
#CombinedForm = inlineformset_factory(User, Address, fields='__all__', can_delete=False)