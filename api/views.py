from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.conf import settings
from search.models import Settlement
from api.serializers import SearchInputSerializer, FormSerializer


# Create your views here.
class SearchAPIView(APIView):

	def get(self, request):
		self.serialazer_class = SearchInputSerializer
		queryset = self.get_queryset()
		response = {
			'settlements': self.serialazer_class(queryset, many=True).data,
		}
		return Response(response)

	def post(self, request):
		self.serialazer_class = FormSerializer
		data = self.serialazer_class(data=request.data)
		data.is_valid(raise_exception=True)
		response = {'response': self.post_queryset()}
		response['context'] = render(request, 'includes/main/result.html', response).content
		return Response(response)



	def get_queryset(self):
		request_param = self.request.query_params.get('text', '')
		self.queryset = Settlement.objects.filter(name__istartswith=request_param)
		return self.queryset

	def post_queryset(self):
		yaschedule = settings.YASHEDULE
		data = self.serialazer_class(data=self.request.data)
		data.is_valid(raise_exception=True)
		departure_city = Settlement.objects.filter(name__iexact=data.data['departure_city']).values('code')[0]
		arrive_city = Settlement.objects.filter(name__iexact=data.data['arrive_city']).values('code')[0]
		date = data.data['dates']
		response = yaschedule.get_schedule(departure_city['code'], arrive_city['code'], date, transport_types='plane')
		response['search']['date'] = datetime.strptime(response['search']['date'], '%Y-%M-%d').strftime('%d.%M.%Y')
		for item in response['segments']:
			item['departure'] = datetime.strptime(item['departure'].split('+')[0], '%Y-%m-%dT%H:%M:%S').strftime('%d.%m.%Y %H:%M')
			item['arrival'] = datetime.strptime(item['arrival'].split('+')[0], '%Y-%m-%dT%H:%M:%S').strftime('%d.%m.%Y %H:%M')
		return response
