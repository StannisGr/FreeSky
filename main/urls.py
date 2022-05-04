from django.urls import path
from .views import IndexView, get_about_us

urlpatterns = [
	path('', IndexView.as_view(), name='index'),
	path('about-us/', get_about_us, name='about-us'),
] 


