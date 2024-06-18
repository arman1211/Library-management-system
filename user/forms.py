from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class RegisterUserForm(UserCreationForm):
    class Meta:

        model = User
        fields = ['username','first_name','last_name','email']
        # fields = '__all__'

class DepositForm(forms.Form):
    amount = forms.IntegerField()
    