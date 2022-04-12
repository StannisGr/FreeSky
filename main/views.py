from django.shortcuts import render
from search.forms import SearchFlightForm


def get_index(request):
	search_form = SearchFlightForm()
	context = {
		'search_form': search_form,
	}
	return render(request, 'main/index.html', context)


def get_profile(request):
	context = {

	}
	return render(request, 'main/profile.html', context)


def get_about_us(request):
	context = {

	}
	return render(request, 'main/about_us.html', context)
