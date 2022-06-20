from django import forms
from django.utils import timezone
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from locations.models import Country
from user.models import User, Document, PaymentData
from user.fields import NormilizedCharField
from social.fields import CharToObjField, ChoiceTextInput
from user.services.form_manager import UserFormBehavior, DocumentFormBehavior, PaymentFormBehavior


class DocumentForm(forms.ModelForm, DocumentFormBehavior):
	pasport_num = NormilizedCharField(widget=forms.TextInput(attrs={'class': 'change-form__input', 'data-mask':'000 000', 'placeholder': '000 000'}))
	citizenship = CharToObjField(
		model=Country,
		queryset=Country.objects.exclude(name='NaN'),
		widget=ChoiceTextInput(
			datalist=Country.objects.exclude(name='NaN'),
			attrs={'list': 'country_set'}
		),
		required=False
	)
	class Meta:
		model = Document
		fields = '__all__'
		widgets = { 
			'user': forms.HiddenInput(),
			'citizenship': forms.Select(attrs={'class': 'change-form__input'}),
			'pasport_series': forms.TextInput(attrs={'class': 'change-form__input'}),
		}

class PaymentForm(forms.ModelForm, PaymentFormBehavior):
	cc_number = NormilizedCharField(widget=forms.TextInput(attrs={'class': 'change-form__input', 'data-mask':'0000 0000 0000 0000', 'placeholder': '0000 0000 0000 0000'}),)
	class Meta:
		model = PaymentData
		fields = '__all__'
		widgets = { 
			'user': forms.HiddenInput(),
			'cc_expiry': forms.TextInput(attrs={'class': 'change-form__input', 'data-mask':'00/00', 'placeholder': 'дд/гг'}),
			'cc_code': forms.TextInput(attrs={'class': 'change-form__input'}),
		}

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

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user


class CustomUserChangeForm(forms.ModelForm, UserFormBehavior):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].required = False
		self.fields['sex'].empty_values = 'Укажите пол'

	class Meta:
		model = User
		fields = ('logo', 'first_name', 'last_name', 'sex', 'birth_date', 'bio')
		widgets = {
			'first_name': forms.TextInput(attrs={'class': 'change-form__input', 'placeholder': 'Укажите имя'}),
			'last_name': forms.TextInput(attrs={'class': 'change-form__input', 'placeholder': 'Укажите фамилию'}),
			'logo': forms.FileInput(attrs={'class': 'change-form__input'}),
			'birth_date': forms.SelectDateWidget(years=range(1930, timezone.now().date().year), attrs={'class': 'change-form__input'}),
			'bio': forms.Textarea(attrs={'class': 'change-form__input', 'placeholder': 'Расскажите о себе', 'cols': 40, 'rows': 10}),
		}

class SingInForm(forms.Form):
	email = forms.CharField(label=_('Email'), widget=forms.TextInput(attrs={'class': 'sign-form__input'}))
	password = forms.CharField(
		label=_('Password'),
		widget=forms.PasswordInput(attrs={'class': 'sign-form__input'}),
	)
