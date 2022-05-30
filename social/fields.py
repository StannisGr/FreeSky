from typing import Any, Dict
from django import forms
from social.models import Tag


class ChoiceTextInput(forms.TextInput):
	template_name = 'social/widgets/choicetext_widget.html'

	def __init__(self, datalist, attrs) -> None:
		self.datalist = datalist
		super().__init__(attrs)

	def get_context(self, name: str, value: Any, attrs) -> Dict[str, Any]:
		widget =  super().get_context(name, value, attrs)
		if widget.get('widget').get('attrs').get('list', False):
			widget['widget']['datalist'] = self.datalist
		else:
			raise AttributeError(
				'ChoiceTextWidget must have "list" attr'
			)
		return widget

class CharToObjField(forms.ModelChoiceField):

	def __init__(self, queryset, model, **kwargs) -> None:
		self.model = model
		super().__init__(queryset=queryset, empty_label=None,  **kwargs)

	def to_python(self, value: str):
		if value:
			value = self.model.objects.get(name=value)
		return value

	def clean(self, value: Any):
		value = self.to_python(value)
		return super().clean(value)

class TagField(forms.ModelMultipleChoiceField):

	def __init__(self, model=Tag, *args, **kwargs) -> None:
		self.model = model
		super(forms.ModelMultipleChoiceField, self).__init__(*args, **kwargs)

	def to_python(self, value):
		object_array = []
		value = value.replace(',', '')
		value = value.replace(';', '')
		for name in value.strip().split(' '):
			name = name if name[0] == '#' else f'#{name}'
			obj, created = self.model.objects.get_or_create(name=name)
			object_array.append(obj)
		return object_array

	def clean(self, value: Any):
		value = self.to_python(value)
		return super().clean(value)