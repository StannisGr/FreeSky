from typing import Optional, Any
from django import forms


class NormilizedCharField(forms.CharField):
	def to_python(self, value: Optional[Any]) -> Optional[str]:
		value = value.replace(' ', '')
		return super().to_python(value)
