from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, SingInForm, CustomUserChangeForm, DocumentForm, PaymentForm
from social.forms import ContentNoteForm
from .models import User
from .backend import UserBackend

# Create your views here.
class ProfileMixin:
	forms = {
		'change_form': CustomUserChangeForm,
		'document_form': DocumentForm,
		'payment_form': PaymentForm,
		'note_form': ContentNoteForm,
	}
	template_name = 'user/profile.html'
	success_url = '/user/profile'

	def get_context(self, request, **kwargs):
		context = dict()
		context.update(self.init_forms(request.user))
		context['newnote'] = bool(int(request.GET.get('newnote', 0)))
		context['addpay'] = bool(int(request.GET.get('addpay', 0)))
		context['adddoc'] = bool(int(request.GET.get('adddoc', 0)))
		return context

	def init_forms(self, user):
		res = {}
		user = User.objects.get(email__iexact=user)
		user_instance = User.objects.values(*self.forms['change_form']().fields.keys()).get(email__iexact=user)
		for form_name in self.forms:
			if form_name == 'change_form':
				res[form_name] = self.forms[form_name](initial=user_instance)
			elif form_name == 'note_form': 
				res[form_name] = self.forms[form_name](initial={'user_id': user})
			else:
				res[form_name] = self.forms[form_name](initial={'user': user})
		return res

	def get_form(self, request, form_name):

		user = User.objects.get(email__iexact=request.user)
		if form_name == 'change_form':
			return self.forms[form_name](request.POST, request.FILES, instance=user)
		elif form_name == 'note_form':
			return self.forms[form_name](request.POST, request.FILES, initial={'user_id': user})
		else: 
			return self.forms[form_name](request.POST, request.FILES, initial={'user': user})
	
class ProfileView(ProfileMixin, CreateView):

	def get(self, request):
		context = self.get_context(request)
		return render(request, self.template_name, context)

	def post(self, request):
		form_name = request.POST.get('form_name')
		form = self.get_form(request, form_name)
		if form.is_valid():
			form.save()
			return redirect(self.success_url)
		else:
			print(form.errors)
			context = self.get_context(request, **{form_name: form})
			return render(request, self.template_name, context)
	
	def form_validation(self, forms: dict)->tuple:
		for form in forms:
			for field in forms[form].fields.keys():
				print(forms[form][field].initial)
			try:
				if forms[form].has_changed():
					return form, forms[form]
			except TypeError:
				continue
			


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
