from django import template
from user.models import Document, PaymentData
from user.forms import DocumentForm, PaymentForm


register = template.Library()

@register.inclusion_tag('user/profile_data.html')
def get_personal_data(user, payment_form=None, document_form=None):
	documents = Document.objects.filter(user=user)
	payments = PaymentData.objects.filter(user=user)
	context = {
		'documents': documents,
		'payments': payments,
		'document_form': document_form,
		'payment_form': payment_form,
	}
	return context
