from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from flights.models import Country
from .manager import UserManager


class DocumentValidator:

	@staticmethod
	def num_validator(value):
		if not value.isdigit():
			raise ValidationError(
				_('Доступны только цифры')
			)
	
	@staticmethod
	def expiry_validator(value):
		values = value.split('/')
		for value in values:
			if len(value) == 2:
				DocumentValidator.num_validator(value)
			else:
				raise ValidationError(
				_('Неверный формат. Необходимый формат: мм/гг')
				)

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
	cc_number = models.CharField(_('card number'), max_length=16, validators=[DocumentValidator.num_validator])
	cc_expiry = models.CharField(_('expiration date'), max_length=5, validators=[DocumentValidator.expiry_validator])
	cc_code = models.CharField(_('security code'), max_length=3, validators=[DocumentValidator.num_validator])

	class Meta:
		verbose_name = 'Платежная информация'
		verbose_name_plural = 'Платежная информация'


class Document(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	citizenship = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
	pasport_series = models.CharField(null=True, blank=True, max_length=4, validators=[DocumentValidator.num_validator])
	pasport_num = models.CharField(null=True, blank=True, max_length=6, validators=[DocumentValidator.num_validator])

	def __str__(self) -> str:
		return f'{self.user} Гражданство: {self.citizenship}'
	
	class Meta:
		verbose_name = 'Документ'
		verbose_name_plural = 'Документы'

