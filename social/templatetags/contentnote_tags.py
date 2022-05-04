from tkinter import N
from django import template
from social.models import Article
from social.forms import ContentNoteForm, CommentNoteForm

register = template.Library()

@register.inclusion_tag('social/short_preview.html')
def get_short_preview_list(request, profile: bool=False):
	empty_message = 'Здесь пока нет ваших путешествий... Время пополнить список!' if profile else 'Постов нет'
	notes = Article.objects.filter(user_id=request.user) if profile else Article.objects.all() if Article.objects.all() else None
	return {
		'request': request,
		'notes': notes,
		'empty_message': empty_message
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
def create_content_note(request, action='newnote/'):
	form = ContentNoteForm(initial={'user_id': request.user})
	return {
		'request': request,
		'form': form,
		'action': action,
	}
