import datetime
from django import forms


class SearchFlightForm(forms.Form):
    departure_city = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'id':'departure_city', 'class': 'search_ui'}))
    arrive_city = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'id':'arrive_city', 'class': 'search_ui'}))
    dates = forms.DateField(initial=datetime.date.today(), widget=forms.TextInput(attrs={'id':'date_field','class': 'search_ui', 'type':'date',}))