from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import CreateView, ListView
from user.models import User
from .models import Article
from .forms import ContentNoteForm, CommentNoteForm

# Create your views here.
class ContentPreviewsView(ListView):
	model = Article
	paginate_by = 8

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context

class ContentView(CreateView):
	template_name = 'social/note.html'

	def get(self, request, note_pk):
		back_url = request.GET.get('next', '/')
		note = get_object_or_404(Article, pk=note_pk)
		context = {
			'note':note,
			'back_url': back_url,
		}
		return render(request, self.template_name, context)
	
	def post(self, request, note_pk):
		form = CommentNoteForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
		return redirect(f'{request.get_full_path()}#{form.data["post"]}')

class CreateContentNote(CreateView):
	form_class = CommentNoteForm
	success_url = 'social/'
	template_name = ''

	def get(self, request):
		user = User.objects.values('email').get(email__iexact=request.user.email)
		form = self.form_class(initial={'user': user['email']})
		context = {
			'form': form,
		}
		return render(request, 'social/new_note.html', context)