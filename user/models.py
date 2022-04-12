from datetime import datetime
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .manager import UserManager




# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(_('Почта'), unique=True)
	first_name = models.CharField(_('Имя'), max_length=30)
	last_name = models.CharField(_('Фамилия'), max_length=30)
	logo = models.ImageField(_('Аватар'), null=True, blank=True)
	sex = models.CharField(
		max_length=6,
		choices={('male', 'м'), ('female', 'ж')},
		null=True
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
		return f'{self.first_name} {self.last_name}'

	def user_directory_path(self, filename):
		return f'users/{self.email[0]}/avatar/'
