from django import forms
from pyparsing import col
from social.models import Article, CommentNote
from ckeditor.widgets import CKEditorWidget



class ContentNoteForm(forms.ModelForm):
	class Meta:
		model=Article
		fields=('user_id', 'preview_image', 'title', 'content', 'tags')
		widgets = {
			'user_id': forms.HiddenInput(),
			'title': forms.TextInput(attrs={'class':'content-form'}),
			'slug': forms.TextInput(attrs={'class':'content-form', 'label': 'URL-заголовок'}),
			'tags': forms.TextInput(attrs={'class':'content-form'}),
		}

class CommentNoteForm(forms.ModelForm):
	class Meta:
		model=CommentNote
		fields=('post', 'content', 'user_id')
		widgets = {
			'post': forms.HiddenInput(),
			'user_id': forms.HiddenInput(),
		}