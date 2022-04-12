from django.urls import path
from . import views

urlpatterns = [
	path('search', views.SearchAPIView.as_view(), name='search')
]