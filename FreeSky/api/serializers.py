from django.shortcuts import render
from rest_framework import serializers
from django.contrib.sessions.models import Session
from flights.models import Settlement
from social.models import Note
from user.models import User
from datetime import datetime, timezone
import pytz


class NoteSerializer(serializers.ModelSerializer):

	class Meta:
		model = Note
		fields = ['likes', 'views']
		extre_fields ={
			'likes': {'required': False},
		}

class SearchInputSerializer(serializers.Serializer):
	
	name = serializers.CharField(max_length=30)
	code = serializers.CharField(max_length=30)

class FormSerializer(serializers.Serializer):
	departure_city = serializers.CharField(max_length=30)
	arrive_city = serializers.CharField(max_length=30)
	dates = serializers.DateField()

class ScheduleAdjuster:

	def __init__(self, request, data: dict, page_size: int=6):
		self.data = data
		self.past_schedule = self.sort_by_date()
		self.request = request
		self.page_size = page_size
		self.pages_num = self.get_pages_num()

	def get_adj_data(self):
		self.adjust_dates()
		self.get_rendered_pages()
		return self.data

	def sort_by_date(self):
		result = []
		data = self.data['segments']
		i = 0
		while i < len(data):
			flight_datetime = datetime.fromisoformat(data[i]['departure'])
			if flight_datetime <= datetime.now().astimezone():
				result.append(data.pop(i))
			else:
				i+=1
		return result


	def adjust_dates(self):
		self.data['search']['date'] = datetime.strptime(self.data['search']['date'], '%Y-%M-%d').strftime('%d.%M.%Y')
		for item in self.data['segments']:
			item['thread']['number'] = item['thread']['number'].replace(' ', '-')
			item['departure'] = datetime.fromisoformat(item['departure']).strftime('%d.%m.%Y %H:%M')
			item['arrival'] = datetime.fromisoformat(item['arrival']).strftime('%d.%m.%Y %H:%M')

	def get_rendered_pages(self):
		self.data['context'] = []
		for page in range(self.pages_num+1):
			max_index = page+1*self.page_size
			min_index =	max_index - self.page_size
			context = {
				'search': self.data['search'],
				'segments': {
					'old': self.past_schedule,
					'current': self.data['segments'][min_index:max_index],
				},
				'pages': [x for x in range(1,self.pages_num+1)],
				'current_page': page+1,
			}
			self.data['context'].append(render(self.request, 'includes/main/result.html', context).content)
	
	def get_pages_num(self):
		try:
			response_size = len(self.data['segments'])
		except KeyError:
			print(self.data)
			return None
		pages = response_size/self.page_size
		if int(pages) < pages:
			pages = int(pages) + 1
		return int(pages)