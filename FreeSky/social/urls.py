"""FreeSky URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .views import CreateContentNote, ContentPreviewsView, ContentView, DeleteContentNote


urlpatterns = [
    path('', ContentPreviewsView.as_view(), name='content-list'),
	path('note/<int:note_pk>/', ContentView.as_view(), name='note'),
	path('note/<slug:slug>/<int:note_pk>/', ContentView.as_view()),
	# path('note/<slug:slug>/',ContentView.as_view(), name='note'),
	# path('new/', CreateContentNote.as_view(), name='new-post'),
	path('note/settings/delete/note/<int:note_pk>/', DeleteContentNote.as_view(), name='delete_note'),
]