from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, SingInForm
from .backend import UserBackend


# Create your views here.
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


class ProfileView(CreateView):
    success_url = '/'
    template_name = 'user/profile.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)
