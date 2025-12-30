from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password', 'username')

class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = ('name',)

class RegistartionForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ('mobile',)

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('state', 'cityname',)

class RtoForm(forms.ModelForm):
    class Meta:
        model = Rto
        fields = ('state', 'city', 'address', 'nodalname',)

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact2
        fields = ('name', 'mobile', 'email', 'message',)

