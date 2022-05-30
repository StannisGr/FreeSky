from django import template
from user.models import Document, PaymentData
from user.forms import DocumentForm, PaymentForm


register = template.Library()

@register.inclusion_tag('user/payment_list.html')
def get_payment_list(user):
	payments = PaymentData.objects.filter(user=user)
	context = {
		'payments': payments,
	}
	return context

@register.inclusion_tag('user/document_list.html')
def get_document_list(user):
	documents = Document.objects.filter(user=user)
	context = {
		'documents': documents,
	}
	return context