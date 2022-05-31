from django import template
from user.models import Document, PaymentData
from user.forms import DocumentForm, PaymentForm


register = template.Library()

@register.inclusion_tag('user/payment_list.html')
def get_payment_list(user, redirect_url):
	payments = PaymentData.objects.filter(user=user)
	context = {
		'payments': payments,
		'redirect_url': redirect_url,
	}
	return context

@register.inclusion_tag('user/document_list.html')
def get_document_list(user, redirect_url):
	documents = Document.objects.filter(user=user)
	context = {
		'documents': documents,
		'redirect_url': redirect_url,
	}
	return context

@register.simple_tag
def define(value=None):
	return value
	