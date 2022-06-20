from django.shortcuts import redirect
from django.views.generic import View
from django.shortcuts import render
from locations.forms import SearchFlightForm
from locations.models import Settlement



class IndexView(View):
	form_class = SearchFlightForm
	template = 'main/index.html'
	
	def get(self, request):
		context = {
			'search_form': self.form_class(),
			'settelments': Settlement.objects.all(),
		}
		return render(request, 'main/index.html', context)


def get_about_us(request):
	return redirect('/')
