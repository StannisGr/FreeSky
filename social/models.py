from urllib import parse
from datetime import datetime
from django.shortcuts import reverse
from django.db import models
from django.contrib.sessions.models import Session
from user.models import User
from flights.models import Location
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField


def preview_img_upload_to(instance, filename):
	return f'notes/preview_images/{datetime.now().date().strftime("%Y/%m/%d")}/{filename}'

class Tag(models.Model):
	name = models.TextField(_('Тег'), unique=True, primary_key=True)

	def unicode_value(self):
		return parse.quote(self.name)

	def __str__(self):
		return f'{self.name}'

class Note(models.Model):
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	content = RichTextUploadingField(_('Содержание'), null=True, blank=False)
	likes = models.ManyToManyField(User, related_name='like_set', blank=False)
	views = models.ManyToManyField(Session, related_name='view_set', blank=False)
	publish_date = models.DateTimeField(_('Дата публикации'), default=datetime.now())

	def __str__(self) -> str:
		return f'{self.user}, {self.publish_date}'

	def get_author(self):
		return f'{self.user_id.get_full_name()}'

	def add_view(self, session):
		self.views.add(session)
		self.save()
		return self.count_views()

	def add_like(self, user):
		self.likes.add(user)
		self.save()
		return self.count_likes()

	def count_likes(self):
		return self.likes.count()

	def count_views(self):
		return self.views.count()
	
	def count_comments(self):
		return self.post_comment_set.count()

class Article(Note):
	title = models.TextField(_('Название поста'), unique=True, max_length=80)
	preview_image = models.ImageField(_('Превью'), upload_to=preview_img_upload_to)
	tags = models.ManyToManyField(Tag, blank=True)
	location = models.ManyToManyField(Location, blank=True)

	class Meta:
		verbose_name = 'Пост'
		verbose_name_plural = 'Посты'
	
	def get_absolute_url(self):
		return reverse('note', kwargs={'note_pk':self.pk})
	
	def __str__(self) -> str:
		return f'{self.title}'

class AdminArticle(Article):
	slug = models.SlugField(_('URL-заголовок'), max_length=255, db_index=True)

	class Meta:
		verbose_name = 'Пост администратора'
		verbose_name_plural = 'Посты администраторов'
	
	def get_author(self):
		return 'FreeSky'

	def get_absolute_url(self):
		return reverse('note', kwargs={'slug': self.slug,'note_pk': self.pk})

class CommentNote(Note):
	post = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='post_comment_set')
	
	class Meta:
		verbose_name = 'Комментарий'
		verbose_name_plural = 'Комментарии'