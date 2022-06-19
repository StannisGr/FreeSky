from django.views.generic import CreateView
from django.shortcuts import render
from flights.forms import SearchFlightForm
from flights.models import Settlement



class IndexView(CreateView):
	form_class = SearchFlightForm
	template = 'main/index.html'
	
	def get(self, request):
		context = {
			'search_form': self.form_class(),
			'settelments': Settlement.objects.all(),
		}
		return render(request, 'main/index.html', context)


def get_about_us(request):
	context = {
	}
	return render(request, 'main/about_us.html', context)
