from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from .models import User


class CustomUserCreationForm(UserCreationForm):
	password1 = forms.CharField(
		label=_("Password"),
		strip=False,
		widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'sign-form__input'}),
		help_text=password_validation.password_validators_help_text_html(),
	)
	password2 = forms.CharField(
		label=_("Password confirmation"),
		widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'sign-form__input'}),
		strip=False,
		help_text=_("Enter the same password as before, for verification."),
	)
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')
		widgets = {
			'first_name': forms.TextInput(attrs={'class': 'sign-form__input'}),
			'last_name': forms.TextInput(attrs={'class': 'sign-form__input'}),
			'email': forms.TextInput(attrs={'class': 'sign-form__input'}),
		}


class CustomUserChangeForm(UserChangeForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')


class SingInForm(forms.Form):
	email = forms.CharField(label=_('Email'), widget=forms.TextInput(attrs={'class': 'sign-form__input'}))
	password = forms.CharField(
		label=_('Password'),
		widget=forms.PasswordInput(attrs={'class': 'sign-form__input'}),
	)
