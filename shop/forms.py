from django import forms
from django.contrib.auth.models import User
from django.forms import fields

from account.models import UserProfile

class UpdateCartForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('cart',)