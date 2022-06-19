from django.urls import path
from . import views

urlpatterns = [
	path('search', views.SearchAPI.as_view(), name='search'),
	path('notes/update/<int:pk>', views.UpdateNoteAPI.as_view(), name='notes'),
]