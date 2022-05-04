from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, SingInForm, CustomUserChangeForm
from social.forms import ContentNoteForm
from .models import User
from .backend import UserBackend


# Create your views here.
class ProfileView(CreateView):
	form_class = CustomUserChangeForm
	success_url = '/user/profile'
	template_name = 'user/profile.html'

	def get(self, request):
		user = User.objects.values(*self.form_class().fields.keys()).get(email__iexact=self.request.user.email)
		form = self.form_class(initial=user)
		context = {
			'change_form': form,
			'newnote': bool(int(request.GET.get('newnote', False))),
		}
		return render(self.request, self.template_name, context)

	def post(self, request):
		user = User.objects.get(email__iexact=self.request.user.email)
		form = CustomUserChangeForm(self.request.POST, self.request.FILES, instance=user)
		if form.is_valid():
			form.save()
			return redirect(self.success_url) 
		else:
			print(form.errors)
			return redirect('/')

class ProfileViewNewPost(CreateView):
	form_class = ContentNoteForm
	success_url = '/user/profile'
	template_name = 'user/profile.html'
	
	def post(self, request):
		user = User.objects.get(email__iexact=self.request.user.email)
		form = self.form_class(request.POST, request.FILES, initial={'user_id': user})
		if form.is_valid():
			form.save()
			return redirect(self.success_url)
		else:
			print(form.errors)
			return redirect('/')

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
