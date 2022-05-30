from django.db.models import Count

class PopularitySort:
	@staticmethod
	def like_sorting(queryset):
		return queryset.annotate(pop_order = Count('likes')).order_by('pop_order')

	@staticmethod
	def views_sorting(queryset):
		return queryset.annotate(pop_order = Count('views')).order_by('pop_order')

	@staticmethod
	def popularity_sorting(queryset):
		queryset = queryset.annotate(pop_order = (Count('views') + Count('likes') + Count('post_comment_set'))).order_by('-pop_order')
		return queryset