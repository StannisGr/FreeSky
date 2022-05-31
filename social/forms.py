from django import forms
from django.db.models import Q
from flights.models import Location
from flights.models import Country, Settlement
from social.models import Article, CommentNote, Tag
from social.fields import TagField, CharToObjField, ChoiceTextInput
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from user.services.form_manager import NoteFormBehavior


class SearchArticleForm(forms.Form):
	class Choice:
		date_choice = (('-publish_date', 'Сначала новое'), ('publish_date', 'Сначала старое'))
		populatity_choice = (('likes', 'Больше всего лайков'), ('views', 'Больше всего просмотров'), ('popularity', 'Наибольшая активность'))
		author_choice = (('all', 'Все посты'), ('user', 'Посты Пользователей'), ('admin', 'Посты FreeSky'))

	text = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':''}))
	author = forms.ChoiceField(choices=Choice.author_choice, required=False)
	populatity = forms.ChoiceField(choices=Choice.populatity_choice, required=False)
	publish_time = forms.ChoiceField(choices=Choice.date_choice, required=False)
	
	location = CharToObjField(
		model=Location,
		queryset=Location.objects.filter(~Q(name='NaN') & Q(country__isnull=False) | Q(settlement__isnull=False)),
		widget=ChoiceTextInput(
			datalist=Location.objects.filter(~Q(name='NaN') & Q(country__isnull=False) | Q(settlement__isnull=False)),
			attrs={'list': 'country_set'}
		),
		required=False
	)

	@classmethod
	def keys(cls):
		return cls.__dict__['base_fields'].keys()


class ContentNoteForm(forms.ModelForm, NoteFormBehavior):
	tags = TagField(queryset=Tag.objects.all(), widget=ChoiceTextInput(datalist=Tag.objects.all(), attrs={'list': 'tags_set'}), required=False)
	country = CharToObjField(model=Country, queryset=Country.objects.exclude(code='lNaN'), widget= ChoiceTextInput(datalist=Country.objects.all(), attrs={'list': 'country_set'}), required=False)
	settlement = CharToObjField(model=Settlement, queryset=Settlement.objects.all(), widget= ChoiceTextInput(datalist=Settlement.objects.all(), attrs={'list': 'settlement_set'}), required=False)
	class Meta:
		model=Article
		fields=('user_id', 'preview_image', 'title', 'content', 'tags')
		widgets = {
			'user_id': forms.HiddenInput(),
			'title': forms.TextInput(attrs={'class':'content-form'}),
			'slug': forms.TextInput(attrs={'class':'content-form', 'label': 'URL-заголовок'}),
		}
	
	def save(self, commit: bool = True):
		instance = super().save(commit)
		if self.cleaned_data['country']:
			instance.location.add(self.cleaned_data['country']) 
		if self.cleaned_data['settlement']:
			instance.location.add(self.cleaned_data['settlement'])
		return instance
	

class CommentNoteForm(forms.ModelForm):
	content = forms.CharField(label='', widget=CKEditorUploadingWidget(config_name='comment'))
	class Meta:
		model=CommentNote
		fields=('post', 'content', 'user_id')
		widgets = {
			'post': forms.HiddenInput(),
			'user_id': forms.HiddenInput(),
		}