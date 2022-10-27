from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from user.models import Document, PaymentData
from user.forms import CustomUserCreationForm, SingInForm, CustomUserChangeForm, DocumentForm, PaymentForm
from social.forms import ContentNoteForm
from user.backend import UserBackend
from user.services.form_manager import FormManager


class CustomLoginRequiredMixin(LoginRequiredMixin):
	login_url = '/user/signin/'


class ProfileView(CustomLoginRequiredMixin, View):
	template_name = 'user/profile.html'
	success_url = 'user/profile'
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

	def get_context_data(self, *args, **kwargs):
		context = super(SingUpView, self).get_context_data(*args, **kwargs)
		context['next'] = self.request.GET.get('next',  self.success_url)
		return context
		
	def get_success_url(self):
		next_url = self.request.GET.get('next')
		succes_url = reverse('sign_in') + f'?next={next_url}'
		return succes_url


class SingInView(View):
    form_class = SingInForm
    success_url = '/'
    template_name = 'user/signin.html'

    standart_redirect = {'/user/signin/', '/user/signup/'}

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.GET)
        return render(request, self.template_name, context={'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        auth = UserBackend()
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                login(request, user, 'user.backend.UserBackend')
                return redirect(self.get_success_url())
            else:
                return self.error_form_response(request, form)
        else:
            return self.error_form_response(request, form)
        
    def get_success_url(self):
        success_url = self.request.GET.get('next', self.success_url)
        return success_url if success_url not in self.standart_redirect else self.success_url

    def error_form_response(self, request, form):
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

class DeleteDocumentView(LoginRequiredMixin, CreateView):
	success_url = '/'
	model = Document

	def get(self, request, document_pk):
		model = get_object_or_404(self.model, pk=document_pk, user_id=request.user)
		model.delete()
		success_url = request.GET.get('next', '')
		if success_url:
			self.success_url = success_url
		return redirect(request.GET.get('next', self.success_url))


class DeletePaymentView(LoginRequiredMixin, CreateView):
	success_url = '/'
	model = PaymentData

	def get(self, request, payment_pk):
		model = get_object_or_404(self.model, pk=payment_pk, user_id=request.user)
		model.delete()
		success_url = request.GET.get('next', '')
		if success_url:
			self.success_url = success_url
		return redirect(self.success_url)