from django.urls import path
from . import views

urlpatterns = [
	path('', views.get_index, name='index'),
	path('about-us/', views.get_about_us, name='about-us'),
] 


