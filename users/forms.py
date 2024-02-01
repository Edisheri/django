from django import forms
from django.contrib.auth.forms import UserCreationForm

from catalog.forms import StileFormMixin
from users.models import User


class UserRegisterForm(StileFormMixin, UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class NewPasswordForm(StileFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)