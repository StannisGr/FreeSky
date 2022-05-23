from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView

from django.shortcuts import render
from django.conf import settings
from flights.models import Settlement
from api.serializers import SearchInputSerializer, NoteSerializer, FormSerializer, ScheduleAdjuster
from social.forms import CommentNoteForm
from social.models import Note

class SearchAPIPaggination():
	page_size = 6
	page_size_query_param = 'page_size'
	max_page_size = 100

# TODO: SORT BY PAST AND FUTURE FLIGHTS
class SearchAPI(APIView):

	def get(self, request):
		self.serialazer_class = SearchInputSerializer
		response = self.get_response()
		response = {
			'settlements': self.serialazer_class(response, many=True).data,
		}
		return Response(response)

	def post(self, request):
		pagginator = SearchAPIPaggination
		self.serialazer_class = FormSerializer
		data = self.serialazer_class(data=request.data)
		data.is_valid(raise_exception=True)
		response = self.post_response()
		return Response(response)

	def get_response(self):
		request_param = self.request.query_params.get('text', '')
		self.queryset = Settlement.objects.filter(name__istartswith=request_param)
		return self.queryset

	def post_response(self):
		yaschedule = settings.YASHEDULE
		data = self.serialazer_class(data=self.request.data)
		data.is_valid(raise_exception=True)
		departure_city = Settlement.objects.filter(name__iexact=data.data['departure_city']).values('code')[0]
		arrive_city = Settlement.objects.filter(name__iexact=data.data['arrive_city']).values('code')[0]
		date = data.data['dates']
		response = yaschedule.get_schedule(departure_city['code'], arrive_city['code'], date, transport_types='plane')
		adjusted_data = ScheduleAdjuster(self.request, response).get_adj_data()
		return adjusted_data

class UpdateNoteAPI(APIView):
	queryset = Note.objects.all()
	serializer_class = NoteSerializer
	
	def patch(self, request, pk):
		instance = Note.objects.get(pk=pk)
		serializer = self.serializer_class(instance, data=request.data, partial=True)
		if serializer.is_valid():
			note = serializer.save()
			response = {
				'note': {
					'id': note.id,
					'views': note.count_views(),
					'likes': note.count_likes(),
				}
			}
			return Response(response)
		else:
			print(serializer.errors)
			return Response(serializer.errors)