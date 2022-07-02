from django import template
from social.models import Article
from social.forms import CommentNoteForm


register = template.Library()

@register.inclusion_tag('social/user_short_preview.html')
def get_user_preview_note_list(request):
	empty_message = 'Здесь пока нет ваших путешествий... Время пополнить список!'
	notes = Article.objects.filter(user_id=request.user)
	return {
		'request': request,
		'notes': notes,
		'empty_message': empty_message,
	}

@register.inclusion_tag('social/short_preview.html')
def get_preview_note_list(request):
	empty_message = 'Постов нет'
	notes = Article.objects.all()
	return {
		'request': request,
		'notes': notes,
		'empty_message': empty_message,
	}

@register.inclusion_tag('social/comments.html')
def get_comments(request, note, author=None, verbose_empty=None):
	return {
		'request': request,
		'note': note,
		'author': author,
		'verbose_empty': verbose_empty,
	}

@register.inclusion_tag('social/new_note.html')
def create_comment_note(request, note, action=''):
	form = CommentNoteForm(initial={'user_id': request.user, 'post': note})
	return {
		'request': request,
		'form': form,
		'action': action,
	}

@register.inclusion_tag('social/new_note.html')
def create_content_note(request, form, note_pk):
	return {
		'request': request,
		'form': form,
		'note_pk': note_pk,
	}
