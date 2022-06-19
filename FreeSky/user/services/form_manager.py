from abc import abstractclassmethod
from typing import Iterable
from django import forms
from user.models import User

class AbstractFromBehavoir:
	form: forms.ModelForm

	def __init__(self, form) -> None:
		self.__class__.form = form
	
	@classmethod
	def _input_data(cls, data=None, files=None, instance=None, initial: dict={}):
		if instance:
			return cls.form(data, files, instance=instance, initial=initial)
		else:
			return cls.form(data, files, initial=initial)

	@abstractclassmethod
	def fill_data(cls, user: User, instance_pk: str=None, data=None, files=None):
		pass


class BaseFormBehavior(AbstractFromBehavoir):
	@classmethod
	def fill_data(cls, user: User, instance_pk: str=None, data=None, files=None):
		if instance_pk:
			instance = cls.form.Meta.model.objects.get(pk=instance_pk, user=user)
			return cls._input_data(data=data, instance=instance)
		else:
			return cls._input_data(data=data, initial={'user': user})


class UserFormBehavior(AbstractFromBehavoir):
	@classmethod
	def fill_data(cls, user: User, instance_pk: str=None, data=None, files=None):
		return cls._input_data(data=data, files=files, instance=user)


class NoteFormBehavior(AbstractFromBehavoir):

	@classmethod
	def get_initial_data(cls, instance)->dict:
		values = forms.model_to_dict(instance)
		values['tags'] = ' '.join([str(i) for i in values['tags']])
		for location in values.pop('location', []):
			try:
				values['country'] = location.country.name
			except AttributeError:
				values['settlement'] = location.settlement.name
			else:
				pass
		return values
	
	@classmethod		
	def fill_data(cls, user: User, instance_pk: str=None, data=None, files=None):
		if instance_pk:
			instance = cls.form.Meta.model.objects.get(pk=instance_pk, user_id=user)
			initial = cls.get_initial_data(instance)
			return cls._input_data(data=data, files=files, instance=instance, initial=initial)
		else:
			return cls._input_data(data=data, files=files, initial={'user_id': user})


class AbstractFormBehaviorMixin:
	form_name: str
	manager: AbstractFromBehavoir


class UserFormBehavior(AbstractFormBehaviorMixin):
	form_name = 'user_form'
	manager = UserFormBehavior


class PaymentFormBehavior(AbstractFormBehaviorMixin):
	form_name = 'payment_form'
	manager = BaseFormBehavior


class DocumentFormBehavior(AbstractFormBehaviorMixin):
	form_name = 'document_form'
	manager = BaseFormBehavior

 
class NoteFormBehavior(AbstractFormBehaviorMixin):
	form_name = 'note_form'
	manager = NoteFormBehavior
		

class FormManager:

	def __init__(self, forms: Iterable[AbstractFormBehaviorMixin]) -> None:
		self.forms = {form.form_name: form for form in forms}
	
	def __getitem__(self, key):
		return self.forms[key]

	def __iter__(self):
		return self.forms.__iter__()
	
	def fill_form(self, name:str, user: User, instance_pk: str=None, data=None, files=None):
		return self.forms[name].manager(self.forms[name]).fill_data(user=user, instance_pk=instance_pk, data=data, files=files)

	def init_forms(self, user, instances: dict=None):
		res = dict()
		for form_name in self.forms:
			if instances and instances.get(form_name, ''):
				res[form_name] = self.fill_form(name=form_name, user=user, instance_pk=instances[form_name])
			else:
				res[form_name] = self.fill_form(name=form_name, user=user)
		return res






