from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DeleteView
from user.models import Document, PaymentData
from user.forms import CustomUserCreationForm, SingInForm, CustomUserChangeForm, DocumentForm, PaymentForm
from social.forms import ContentNoteForm
from user.backend import UserBackend
from user.services.form_manager import FormManager
from django.shortcuts import get_object_or_404


class ProfileView(CreateView):

	template_name = 'user/profile.html'
	success_url = '/user/profile'

	forms = FormManager([CustomUserChangeForm, DocumentForm, PaymentForm, ContentNoteForm])

	def get_context(self, request, **kwargs):
		context = dict()
		context['newnote'] = bool(int(request.GET.get('newnote', 0)))
		context['addpay'] = bool(int(request.GET.get('addpay', 0)))
		context['adddoc'] = bool(int(request.GET.get('adddoc', 0)))
		context['edit_user'] = bool(int(request.GET.get('edit_user', 0)))
		context['edit_document'] = request.GET.get('edit_document','')
		context['edit_payment'] = request.GET.get('edit_payment', '')
		context['edit_note'] = request.GET.get('edit_note', '')
		context.update(
			self.forms.init_forms(
				request.user,
				{'document_form': context['edit_document'],
				'payment_form': context['edit_payment'],
				'note_form': context['edit_note']}
				)
			)
		return context

	def get(self, request):
		context = self.get_context(request)
		return render(request, self.template_name, context)

	def post(self, request):
		form_data = request.POST.get('form', '')
		if form_data:
			name, instanse_pk = form_data.split('?')
			form = self.forms.fill_form(name=name, user=request.user, data=request.POST, files=request.FILES, instance_pk=instanse_pk)
			if form.is_valid():
				form.save()
				return redirect(self.success_url)
			else:
				context = self.get_context(request, **{name: form})
				return render(request, self.template_name, context)
		return redirect(self.success_url)

class SingUpView(CreateView):
	form_class = CustomUserCreationForm
	success_url = '/'
	template_name = 'user/signup.html'

	def post(self, request, *args, **kwargs):
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.save()
			return redirect(self.success_url)
		else:
			context = {
				'form': form
			}
			return render(request, self.template_name, context=context)

class SingInView(CreateView):
	form_class = SingInForm
	success_url = '/'
	template_name = 'user/signin.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class(request.GET)
		return render(request, self.template_name, context={'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		auth = UserBackend()
		if form.is_valid():
			user = auth.authenticate(request, email=form.cleaned_data['email'], password=form.cleaned_data['password'])
			if user is not None:
				login(request, user)
				return redirect(self.success_url)
		else:
			context = {
				'form': form
			}
			return render(request, self.template_name, context=context)


class DeleteDocumentView(CreateView):
	success_url = '/'
	model = Document

	def get(self, request, document_pk):
		model = get_object_or_404(self.model, pk=document_pk, user_id=request.user)
		model.delete()
		success_url = request.GET.get('next', '')
		if success_url:
			self.success_url = success_url
		return redirect(request.GET.get('next', self.success_url))


class DeletePaymentView(CreateView):
	success_url = '/'
	model = PaymentData

	def get(self, request, payment_pk):
		model = get_object_or_404(self.model, pk=payment_pk, user_id=request.user)
		model.delete()
		success_url = request.GET.get('next', '')
		if success_url:
			self.success_url = success_url
		return redirect(self.success_url)