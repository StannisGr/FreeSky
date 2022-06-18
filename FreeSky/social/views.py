from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404
from django.http.request import QueryDict
from django.views.generic import CreateView, ListView
from user.models import User
from social.models import Article, Note
from social.forms import CommentNoteForm, SearchArticleForm
from social.services.notes_sort import PopularitySort


class ContentPreviewsView(ListView):
	model = Article
	paginate_by = 8
	pop_strategy = {
		'likes': PopularitySort.like_sorting,
		'views': PopularitySort.views_sorting,
		'popularity': PopularitySort.popularity_sorting,
	}
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['search_form'] = SearchArticleForm(initial=self.search_params)
		return context

	def get_text_filter(self, text, queryset):
		text_set = text.strip().split(';')
		for i in text_set:
			if i[0] == '#':
				queryset = queryset.filter(tags=i)
			else:
				queryset = queryset.filter(title__icontains=i)
		return queryset

	def get_queryset(self):
		self.search_params = {key: self.request.GET.get(key, '').strip() for key in SearchArticleForm.keys()}
		queryset = Article.objects.all()
		if self.search_params['author'] == 'all':
			pass
		elif self.search_params['author'] == 'user':
			queryset = queryset.exclude(adminarticle__isnull=False)
		elif self.search_params['author'] == 'admin':
			queryset = queryset.filter(adminarticle__isnull=False)
		if self.search_params['text']:
			queryset = self.get_text_filter(self.search_params['text'], queryset)
		if self.search_params['location']:
			queryset = queryset.filter(location__name=self.search_params['location'])
		if self.search_params['publish_time']:
			queryset = queryset.order_by(self.search_params['publish_time'])
		if self.search_params['populatity']:
			queryset = self.pop_strategy[self.search_params['populatity']](queryset)
		return queryset

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
		user = User.objects.values('email').get(pk=request.user)
		form = self.form_class(initial={'user': user['email']})
		context = {
			'form': form,
		}
		return render(request, 'social/new_note.html', context)


class DeleteContentNote(CreateView):
	success_url = '/'
	# form_class = DeletionCheckForm

	def get(self, request, note_pk):
		note = get_object_or_404(Note, pk=note_pk, user_id=request.user)
		note.delete()
		return redirect(request.GET.get('next', self.success_url))
