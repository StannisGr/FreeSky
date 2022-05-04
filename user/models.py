from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from flights.models import Country
from .manager import UserManager


# Create your models here.
def user_directory_path(instance, filename):
	return f'users/users_{instance.email[0]}/avatar/{filename}'


class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(_('Почта'), primary_key=True)
	first_name = models.CharField(_('Имя'), max_length=30)
	last_name = models.CharField(_('Фамилия'), max_length=30)
	logo = models.ImageField(_('Аватар'), upload_to=user_directory_path, null=True, blank=True)
	sex = models.CharField(
		_('Пол'),
		max_length=7,
		choices={('мужчина', 'м'), ('женщина', 'ж')},
		null=True,
		blank=True
	)
	bio = models.TextField(_('О себе'), max_length=500, null=True, blank=True)
	birth_date = models.DateField(_('День рождения'), null=True, blank=True)
	date_joined = models.DateField(_('Дата регистрации'), default=timezone.now)
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=False)

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'last_name']

	class Meta:
		verbose_name = 'Пользователь'
		verbose_name_plural = 'Пользователи'

	def __str__(self):
		return self.email

	def get_full_name(self):
		last_name = '' if self.last_name is None else self.last_name
		return f'{self.first_name} {last_name}'

class PaymentData(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	cc_number = models.IntegerField(_('card number'))
	cc_expiry = models.DateField(_('expiration date'))
	cc_code = models.SmallIntegerField(_('security code'))

class Document(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	citizenship = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
	pasport_series = models.SmallIntegerField(null=True, blank=True)
	pasport_num = models.SmallIntegerField(null=True, blank=True)
