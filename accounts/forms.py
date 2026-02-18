from django import forms
from django.contrib.auth.forms import UserCreationForm
from . models import Customer

class RegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)

    class Meta:
        model = Customer
        fields = ('name','email', 'phone_number', 'password1', 'password2')

