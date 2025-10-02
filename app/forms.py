from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from .models import Catg,SubCatg, prodss, prod_type
from django.contrib.auth.models import User
from .models import Customer

class Registeruser(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']

class CustomerProfileForm (forms.ModelForm):
   class Meta:
        model = Customer
        fields=[ 'name', 'locality', 'city', 'mobile', 'state','zipcode' ]
        widgets={
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'locality' :forms.TextInput(attrs={'class':'form-control'}),
            'city': forms.TextInput(attrs={ 'class':'form-control'}),
            'mobile': forms.NumberInput(attrs={'class':'form-control' }),
            'state' : forms.Select(attrs={'class': 'form-control'}),
            'zipcode': forms.NumberInput(attrs={ 'class':'form-control'})}
        
class MyPasswordChangeForm (PasswordChangeForm) :
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput (attrs={'autofocus ': 'True', 'autocomplete': 'current-password', 'class': 'form-control'}))
    new_password1 = forms.CharField(label= 'New Password', widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}))
    new_password2 = forms.CharField(label= 'Confirm Password', widget=forms. PasswordInput(attrs={ 'autocomplete': 'current-password', 'class': 'form-control'}))


class SearchForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Catg.objects.all(), required=False)
    subcategory = forms.ModelChoiceField(queryset=SubCatg.objects.all(), required=False)
    product = forms.CharField(max_length=100, required=False)
    product_type = forms.ModelChoiceField(queryset=prod_type.objects.all(), required=False)
