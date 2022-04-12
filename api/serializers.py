from rest_framework import serializers
from search.models import Settlement


class SearchInputSerializer(serializers.Serializer):
	
	name = serializers.CharField(max_length=30)
	code = serializers.CharField(max_length=30)

class FormSerializer(serializers.Serializer):
	departure_city = serializers.CharField(max_length=30)
	arrive_city = serializers.CharField(max_length=30)
	dates = serializers.DateField()