from csv import list_dialects
from django.contrib import admin
from social.models import Article, CommentNote
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
# Register your models here.

class ContentAdminForm(forms.ModelForm):
	content = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())
	tags = forms.CharField(required=False)
	class Meta:
		model = Article
		fields='__all__'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	list_display = ('title', 'user_id', 'publish_date')
	ordering = ('-publish_date',)
	search_fields = ('user', 'tags', 'title')
	form = ContentAdminForm
	fieldsets = (
		(None, {'fields': ('preview_image', 'title', 'content')}),
		('Дополнительная информация', {'fields': ('user_id', 'tags')})
		)
		
@admin.register(CommentNote)
class CommentNoteAdmin(admin.ModelAdmin):
	list_display = ('post' ,'user_id', 'publish_date')
